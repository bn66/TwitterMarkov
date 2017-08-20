"""This Library will
"""
import argparse
from pdb import set_trace

import twitter

directory = 'database/'

def tweets_to_txt(status):
    with open(directory + status.user.screen_name + '.txt', 'a') as f:
        f.write(str(status.id))
        f.write(', ')
        temp = status.text.encode('ascii', 'ignore').replace('\n', '')
        temp = temp.replace('&amp;', '&')
        f.write(temp)
        f.write('\n')

def get_all_tweets(user, last_id = None):
    user_obj = api.GetUser(screen_name = user)

    first_status = api.GetUserTimeline(screen_name = user, count = 1)
    if last_id == None:
        last_id = first_status[0].id

    # print([s.text for s in statuses])

    # 3200 tweet retrieval limit for Twitter Rest API
    total_tweets = user_obj.statuses_count
    mx = total_tweets // 200 + 1
    for i in range(0, mx):
        statuses = api.GetUserTimeline(screen_name = user,
                        count = 200, max_id = last_id)
        if statuses == []:
            break
        for tweet in statuses:
            tweets_to_txt(tweet)
        last_id = statuses[-1].id - 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--consumerkey', dest = 'ck',
                        type = str, help = 'Consumer Key (API Key)')
    parser.add_argument('-b', '--consumersecret', dest = 'cs',
                        type = str, help = 'Consumer Secret (API Secret)')
    parser.add_argument('-c', '--accesstokenkey', dest = 'at',
                        type = str, help = 'Access Token')
    parser.add_argument('-d', '--accesstokensecret', dest = 'ats',
                        type = str, help = 'Access Token Secret')
    parser.add_argument('-u', '--user', dest = 'user',
                        type = str, help = 'User twitter handle')

    args = parser.parse_args()

    # print args.ck,args.cs,args.at,args.ats

    api = twitter.Api(consumer_key=args.ck,
                      consumer_secret=args.cs,
                      access_token_key=args.at,
                      access_token_secret=args.ats)
    api.VerifyCredentials()

    set_trace()
    # get_all_tweets(args.user)
