
"""
    Exclude Tweets with URL
"""
import re
def text_contains_url(text):
    # Regular expression pattern to match URLs
    url_pattern = re.compile(r'https?://\S+')

    # Check if the text contains a URL
    if url_pattern.search(text):
        return True
    else:
        return False

# print(tweet_contains_url("hello"))
def exclude_tweets_with_url(tweets):
    filtered_tweets = []
    for tweet in tweets:
        if text_contains_url(tweet.text) is False:
            filtered_tweets.append(tweet)
    return filtered_tweets

def thread_to_single_tweet(tweets):
  mp = {}
  for tweet in tweets:
    if tweet.conversation_id in mp:
      mp[tweet.conversation_id].append(tweet.text)
    else:
      mp[tweet.conversation_id] = []
      mp[tweet.conversation_id].append(tweet.text)
  aggregate_list = []
  for id in mp:
    lists = mp[id]
    reversed_list = lists[::-1]
    cnt = 0
    string = ""
    for j in reversed_list:
      if cnt == 0:
        string = string + j
        cnt = cnt + 1
      else:
        string = string + "\n"
        string = string + j
    aggregate_list.append(string)
  return aggregate_list
