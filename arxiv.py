#!/usr/bin/env python

import argparse
import re
import urllib.request

import feedparser


def title_relevance(title, keywords):
    """
    Return a float denoting the relevance of a string given keywords

    Parameters
    ----------
    title : string
        The string to determine a relevance for
    keywords : dictionary of string:int pairs
        The keywords to search the string for and the weights given to them

    Returns
    -------
    float
        The sum of the weights of all keywords in the string
    """
    relevance = 0
    relevant_keywords = []
    for keyword in keywords:
        if re.search(keyword.lower(), title.lower()) is not None:
            relevance += keywords[keyword]
            relevant_keywords.append(keyword)
    return float(relevance) / len(title.split()), relevant_keywords
        

def main():
    parser = argparse.ArgumentParser(description="Query arXiv for the latest "
                                                 "extragalactic and cosmology "
                                                 "papers and display the most "
                                                 "relevant")
    parser.add_argument('--keywords', action='store_true',
                        help='Display the keywords matched in each title')
    args = parser.parse_args()

    # List the keywords and weights
    keywords = {r'\b' 'smg' r'\b': 10,
                'millimet': 8,
                r'\b' 'ism' r'\b': 8,
                'herschel': 6,
                r'\b' 'sed' r'\b': 4,
                'spectra': 4,
                'pdbi': 4,
                r'\b' 'lens': 4,
                'cii': 4,
                'emission': 4,
                'molecular': 4,
                'j=': 4,
                r'\b' 'dust': 4,
                'starburst': 4,
                r'\b' 'agn' r'\b': 4,
                'quasar': 4,
                'qso': 4,
                'sub': 4,
                'formation': 4,
                'forming': 4,
                'medium': 4,
                'luminosit': 2,
                'active': 2,
                r'\b' 'gala': 2,
                'gravitational': 2,
                'redshift': 2,
                'source': 2,
                'number': 2,
                'star': 2,
                #'cluster': 2,
                'simulation': 2,
                'distribution': 2,
                'energy': 2,
                'massive': 2,
                r'[\bfmn]' 'ir' r'\b': 2,
                'infra' '-?' 'red': 2,
                'propert': 2,
                'observ': 2,
                r'\b' 'inter': 2,
                'relation': 2,
                'grow': 2,
                'gas': 2,
                'high': 2,
               }
    # Query arXiv
    url = ('http://export.arxiv.org/api/query?search_query='
           'cat:astro-ph.CO'
           '&start=0'
           '&max_results=500'
           #sortBy can be "relevance", "lastUpdatedDate", "submittedDate"
           '&sortBy=submittedDate'
           '&sortOrder=descending')
    data = urllib.request.urlopen(url).read()
    page = feedparser.parse(data)

    # Sort titles by relevance
    articles = [[-1, entry['id'][21:], entry['title'], []]
                for entry in page['entries']              ]
    for article in articles:
        article[0], article[3] = title_relevance(article[2], keywords)
    articles.sort(key=lambda article: article[0], reverse=False)

    for article in articles:
        if article[0] > 0.7:
            if args.keywords is True:
                print("{0:.1f}  {1} {2} {3}".format(article[0], article[1],
                                                    article[2], article[3]))
            else:
                print("{0:.1f}  {1} {2}".format(article[0], article[1],
                                                article[2])            )


if __name__ == '__main__':
    main()

