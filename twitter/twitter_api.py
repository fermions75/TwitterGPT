import os
from dotenv import load_dotenv
import tweepy
load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
Bearer_Token = os.getenv("Bearer_Token")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=Bearer_Token)

"""
    Get Users ID
"""
# returns twitter userid

def get_userid(username):
    user = client.get_user(username=username)
    return user.data.id

# max_results should be <=800
"""
    Get Twitter Account Name
"""
def get_twitter_account_name(username):
    user = client.get_user(username=username)
    return user.data.name


"""
    Get Users Tweets
"""
def get_users_tweets(userid, max_results=800):
    responses = []
    pagination_token = None
    remaining = max_results
    tweet_fields = ["id", "text", "conversation_id", "created_at"]
    excluded_fields = ["retweets", "replies"]
    while (remaining > 0):
        nxt_cnt = min(max(remaining, 5), 100)
        if pagination_token == None:  # first time
            users_tweets = client.get_users_tweets(
                userid, tweet_fields=tweet_fields, exclude=excluded_fields, max_results=nxt_cnt)
        else:
            users_tweets = client.get_users_tweets(
                userid, tweet_fields=tweet_fields, exclude=excluded_fields, max_results=nxt_cnt, pagination_token=pagination_token)
        # print(users_tweets)
        if (users_tweets.meta["result_count"] == 0):  # no more tweets
            break
        # take only remaining tweets
        take_tweets = min(len(users_tweets.data), remaining)
        for j in range(take_tweets):
            remaining -= 1
            responses.append(users_tweets.data[j])
        pagination_token = users_tweets.meta["next_token"]  # get next token
    return responses


# id = get_userid("elonmusk")
# print(id)
# tweets = get_users_tweets(id,10)
# print(len(tweets))
# print(tweets)

# print(get_twitter_account_name('naval'))
# twitter_img_url('naval')

