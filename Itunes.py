import json
import requests
import pandas as pd
import sqlite3 as db

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def getJson(url):
    response = urlopen(url)
    data = str(response.read())
    return json.loads(data)


def store_reviews(reviews):

    try:
        conn = db.connect('test.db')

        reviews.to_sql('ITUNES_REVIEWS', conn, if_exists='replace')

    except Exception as e:

        print "Error : %s:" % (e.args[0])

    finally:

        if conn:
            conn.close()


def getReviews(appID, page=1):
    url = 'https://itunes.apple.com/rss/customerreviews/id=%s/page=%d/sortby=mostrecent/json' % (appID, page)
    data = getJson(url).get('feed')

    if data.get('entry') == None:
       getReviews(appID, page+1)
       return

    ReviewDataList = pd.DataFrame()

    for entry in data.get('entry'):
        if entry.get('im:name'): continue

        ReviewDataList = ReviewDataList.append({'ID': entry.get('id').get('label'),
                                                'TITLE': entry.get('title').get('label').replace('"', '""'),
                                                'AUTHOR_NAME': entry.get('author').get('name').get('label'),
                                                'AUTHOR_URL':entry.get('author').get('uri').get('label'),
                                                'VERSION':entry.get('im:version').get('label'),
                                                'RATING':entry.get('im:rating').get('label'),
                                                'REVIEW_TEXT':entry.get('content').get('label').replace('"', '""'),
                                                'VOTECOUNT':entry.get('im:voteCount').get('label')}, ignore_index=True)

    store_reviews(ReviewDataList)


def main():
    getReviews(appID="407358186")


if __name__ == "__main__":
    main()
