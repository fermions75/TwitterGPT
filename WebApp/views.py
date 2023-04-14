from django.shortcuts import render
from dotenv import load_dotenv
from twitter.test import get_tweets
from twitter.twitter_api import get_twitter_account_name
load_dotenv()
import os
import openai

'''
redirects to landing page
'''
def index(request):
    return render(request, 'index.html')

'''
returns the generated tweets from openai api to UI
'''
def get_generated_tweets(request):
    openai_api = os.getenv("openai_api_key")
    openai.api_key = openai_api
    twitter_handle = request.POST.get("handle")
    tweets_from_api = get_tweets(twitter_handle)
    prompt = '''
        Generate 3 tweets with examples based on the given tweets below and your training data. Write tweets in details. Generate a thread consisting of multiple tweets based on the given tweets.
        While writing, please follow the following format so that I can distinguish different tweets. Before writing every tweet, Write the tweet number like this: Tweet #(Tweet no.)
        Here are the tweets:
    '''
    msg_to_gpt = prompt + '\n\n' + tweets_from_api
    messages = [
        {"role": "assistant", "content": '''Assume you are a helpful assistant who analyzes some given tweets and writes new tweets based on the given tweets and your training data. 
    '''}
    ]

    messages.append({"role": "user", "content": msg_to_gpt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    generated_tweets = completion.choices[0].message.content
    print(generated_tweets)
    split_tweets = generated_tweets.split("\n\n")
    print(split_tweets)
    param = {
        'name' : get_twitter_account_name(twitter_handle),
        'handle' : twitter_handle,
        'tweets' :  split_tweets
    }
    return render(request, 'index.html', param)