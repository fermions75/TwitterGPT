from twitter_api import get_userid, get_users_tweets
from filter_tweets import exclude_tweets_with_url, thread_to_single_tweet

id = get_userid("adcock_brett")
print(id)
tweets = get_users_tweets(id,100)
print(len(tweets))
print(tweets)
urls_removed = exclude_tweets_with_url(tweets)

print(len(urls_removed))
print(urls_removed)

thread_aggregated = thread_to_single_tweet(urls_removed)

print(thread_aggregated)

for thread in thread_aggregated:
  print(thread)
  print("------------------")