import tweepy
import requests
import os
import json
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords
import re
from collections import Counter
import nltk

consumer_key = 
consumer_secret = 
Bearer_Token = 
access_token = 
access_token_secret = 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_list_details(list_id):
  pm_list = api.get_list_members(list_id = list_id)
  list_details = []
  for val in pm_list:
    list_details.append([val.id, val.screen_name])
  return list_details

list_id = 1628808372102520833
list_details = get_list_details(list_id)

for (id, name) in list_details:
  print(str(id) + " " + name)

def create_url(user_id, max_results):
    # user_id = 3222018178
    return "https://api.twitter.com/2/users/{}/tweets?max_results={}".format(user_id, max_results)

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"exclude" : "replies,retweets",
            "tweet.fields": "conversation_id"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {Bearer_Token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweet_url(tweet_id, id_name):
  tweet_url = f"https://twitter.com/{id_name}/status/{tweet_id}"
  return tweet_url

def get_tweet_likes(tweet_id):
  tweet = api.get_status(tweet_id)
  num_likes = tweet.favorite_count
  return num_likes

def get_tweet_lists(list_details):
  tweet_list = []
  for (id, name) in list_details:
    user_id = id
    max_results = 30
    max_likes = 30
    url = create_url(user_id, max_results)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    cnt = 0
    for tweet in json_response["data"]:
      if cnt == max_results:
        break
      cnt = cnt + 1
      tweet_list.append([name, tweet['text'], get_tweet_url(tweet['id'], name), tweet['id'], tweet['conversation_id']])
  print("cnt is ---> ", cnt)
  return tweet_list

list_of_tweet = []
list_of_tweet = get_tweet_lists(list_details)
df = pd.DataFrame(list_of_tweet, columns=['User', 'Tweets', 'URL', 'Tweet_id', 'conversation_id'])

def thread_to_single_tweet(list_of_tweet):
  mp = {}
  for i in list_of_tweet:
    if i[4] in mp:
      mp[i[4]].append(i[1])
    else:
      mp[i[4]] = []
      mp[i[4]].append(i[1])
  aggregate_list = []
  for i in mp:
    lists = mp[i]
    reversed_list = lists[::-1]
    cnt = 0
    string = ""
    for j in reversed_list:
      if cnt == 0:
        if filter_tweets_by_link(j) == False:
          string = string + j
          cnt = cnt + 1
      else:
        if filter_tweets_by_link(j) == False:
          string = string + "\n"
          string = string + j
  aggregate_list.append(string)
  return aggregate_list
    
def filter_tweets_by_link(text):
  if 'http://' in text or 'https://' in text:
    return True
  return False

aggregate_list = thread_to_single_tweet(list_of_tweet)

for i in aggregate_list:
  print(i)
  print("------------------")

for index, row in df.iterrows():
    print(index, row['User'], row['Tweets'], row['URL'], row['Tweet_id'])

payload = {"records": df.to_dict(orient="records")}

def get_top_keywords(tweets_list):
    tweets_new = []
    for (name, twt) in tweets_list:
      tweets_new.append(twt)
    # Clean the tweets
    cleaned_tweets = [clean_tweet(tweet) for tweet in tweets_new]
    # Tokenize the tweets
    tokens = [tweet.split() for tweet in cleaned_tweets]
    # Flatten the list of tokens
    flat_tokens = [token for sublist in tokens for token in sublist]
    # Remove stop words (you may need to download the NLTK stop words)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in flat_tokens if token not in stop_words]
    # Count the frequency of each token
    counts = Counter(filtered_tokens)
    # Sort the tokens by frequency
    sorted_counts = counts.most_common()
    # Print the top 10 tokens
    for token, count in sorted_counts[:10]:
        print(token, count)

def clean_tweet(tweet):
    # Remove URLs
    tweet = re.sub(r'http\S+', '', tweet)
    # Remove special characters and punctuation
    tweet = re.sub(r'[^\w\s]', '', tweet)
    # Convert to lowercase
    tweet = tweet.lower()
    return tweet
nltk.download('stopwords')

tweets = api.user_timeline(screen_name="adcock_brett", count=100)

tweets

filtered_tweets = [tweet for tweet in tweets if tweet.in_reply_to_status_id is None]

type(filtered_tweets)

for i in filtered_tweets:
  print(i.text)

"""Air Table Connection

Get the records
"""

import requests
base_id = 'appojV2J7yhqqLwXB'
table_name = 'MyTweets'
url = 'https://api.airtable.com/v0/{}/{}'.format(base_id, table_name)
# url = 'https://api.airtable.com/v0/appojV2J7yhqqLwXB/MyTweets?fields%5B%5D=fldjcCnyZtEGAymxR'
auth_token = 'pat3R8xNVxP3MHta5.360d2be6b70e8e8fd59204bc719b83d485bf91f5a91362d13ad1a3f97eca299c'
headers = {
    "Authorization": f"Bearer {auth_token}"
}
response = requests.get(url, headers=headers)
data = response.json()

data

for item in data['records']:
    fields = item['fields']
    print(fields['URL'], ' ---- ' ,fields['Tweet Text'], ' ---- ' ,fields['Username'], ' ---- ' ,fields['ID'])

"""Create records"""

payload

url = 'https://api.airtable.com/v0/{}/{}'.format(base_id, table_name)
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}
field_map = {
    'User': 'Username',
    'Tweets': 'Tweet Text',
    'URL': 'URL',
    'Tweet_id': 'ID'
}
payloadss = {
    "records":[
        {
            "fields": {field_map[column]: str(row[column]) for column in df.columns}
        } for _, row in df.iterrows()
    ]
}
response = requests.post(url, headers=headers, json=payloadss)
data = response.json()

"""Connect to ChatGPT API"""

import os
import openai
openai.api_key = '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'

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message.content)

messages=[
    {"role": "system", "content": "You are an expert who summarizes a tweet and provides important keywords"}
  ]

content = """hi! Summarize and give important keywords for this tweet 
  Take job 1 level above what you're ready for

If you took a job that's comfortable on day 1, you took the wrong job.

Only accept new challenges, not new jobs.


"""
messages.append({"role": "user", "content": content})
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages
)

print(completion.choices[0].message.content)

