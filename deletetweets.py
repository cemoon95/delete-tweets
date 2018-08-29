#!/usr/bin/env python

import argparse
from backports import csv
import sys
import time
import os
import twitter
import io
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1.1"

#Remove the "#" in the next four lines and insert the keys
#os.environ["TWITTER_CONSUMER_KEY"]=""
#os.environ["TWITTER_CONSUMER_SECRET"]=""
#os.environ["TWITTER_ACCESS_TOKEN"]=""
#os.environ["TWITTER_ACCESS_TOKEN_SECRET"]=""

def delete(api, start, date, r):
    with io.open("tweets.csv", encoding='utf-8') as file:
        count = 0

        for row in csv.DictReader(file):
            tweet_id = int(row["tweet_id"])
            tweet_date = parse(row["timestamp"], ignoretz=True).date()
            if start != "" and tweet_date < parse(start).date():
                continue
            if date != "" and tweet_date >= parse(date).date():
                continue

            if (r == "retweet" and row["retweeted_status_id"] == "" or
                    r == "reply" and row["in_reply_to_status_id"] == ""):
                continue

            try:
                print("Deleting tweet #{0} ({1})".format(tweet_id, tweet_date))

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(0.2)

            except twitter.TwitterError as err:
                print("Exception: %s\n" % err.message)

    print("Number of deleted tweets: %s\n" % count)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    TWITTER_CONSUMER_KEY="4ABmBMart6NrG9oTduBEwfPcw"
    TWITTER_CONSUMER_SECRET="GjPqhlMBdSR95C4EejQ5WLbGmvWmvcQ5mTreFLtFjxInuvyCpD"
    TWITTER_ACCESS_TOKEN="251897908-naZSS05dSvSu7jsHVWE5CxhcFfMyPwSbnCmBdR2p"
    TWITTER_ACCESS_TOKEN_SECRET="OKBwzczaogKMBZwUaX06q8jcGMk2FAecuqMh2EmSes1wl"
	
	
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-s", dest="start", required=True,
                        help="Delete tweets after this date")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")

    args = parser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
                "TWITTER_CONSUMER_SECRET" in os.environ and
                "TWITTER_ACCESS_TOKEN" in os.environ and
                "TWITTER_ACCESS_TOKEN_SECRET" in os.environ):
        error("No consumer key/secret and/or access token/secret set.")

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    delete(api, args.start, args.date, args.restrict)

if __name__ == "__main__":
    main()
