from twitter.twitter_api import *
from twitter.filter_tweets import *


def customize_thread_tweets_for_gpt(tweet_threads):
  cnt = 1
  customized_tweets = []
  for thread in tweet_threads:
    tweet_no = 'Tweet ' + str(cnt) + ':\n'
    cnt = cnt + 1
    main_tweet = tweet_no + thread
    customized_tweets.append(main_tweet)

  return customized_tweets

def tweet_to_string(tweet_list):
  string = ""
  for tweets in tweet_list:
      string = string + tweets + '\n\n'
  return string

def get_tweets(handle):
  id = get_userid(handle)
  tweets = get_users_tweets(id, 10)
  urls_removed = exclude_tweets_with_url(tweets)
  thread_aggregated = thread_to_single_tweet(urls_removed)
  thread_aggregated_for_gpt = customize_thread_tweets_for_gpt(thread_aggregated)
  string_of_tweets = tweet_to_string(thread_aggregated_for_gpt)
  return string_of_tweets

# curr_list = get_tweets("naval")
# print(curr_list)
# for tweets in curr_list:
#     print(tweets)
#     print("------------------")





