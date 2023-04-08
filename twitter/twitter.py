from twitter_api import get_userid, get_users_tweets
from filter_tweets import exclude_tweets_with_url, thread_to_single_tweet

def get_formated_tweets(handle, num_tweets):
  id = get_userid(handle)
  print(id)
  tweets = get_users_tweets(id, num_tweets)
  print(len(tweets))
  urls_removed = exclude_tweets_with_url(tweets)
  print(len(tweets))
  thread_aggregated = thread_to_single_tweet(urls_removed)
  print(len(thread_aggregated))
  return thread_aggregated