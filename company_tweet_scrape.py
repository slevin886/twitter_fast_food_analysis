
# coding: utf-8

# In[1]:


import pandas as pd
import tweepy
from tweepy import OAuthHandler
from twitter_codes import consumer_secret, consumer_key, access_secret, access_token
from tqdm import tqdm


# In[2]:


auth = OAuthHandler(consumer_secret, consumer_key)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# In[3]:


try:
    redirect_url = auth.get_authorization_url(signin_with_twitter=True)
except tweepy.TweepError:
    print('Error! Failed to get request token.')


# In[4]:


rest_names = ['@McDonalds', 
             '@sonicdrivein', 
             '@wingstop',
             '@Starbucks',
             '@shakeshack',
             '@redrobinburgers',
             '@Potbelly',
             '@dominos',
             '@DennysDiner',
             '@CrackerBarrel',
             '@ChipotleTweets',
             '@Wendys',
             '@dunkindonuts']


# In[5]:


all_comps = []

for company in tqdm(rest_names):
    twitter_comp = []
    for tweet in api.user_timeline(id=company, wait_on_rate_limit=True):
        comp = {}
        comp['name'] = company
        comp['time_tweeted'] = tweet.created_at
        comp['favorite_count'] = tweet.favorite_count
        comp['retweet_count'] = tweet.retweet_count
        comp['text'] = tweet.text
        comp['unique_code'] = tweet.id_str
        comp['company_followers_count'] = tweet.author.followers_count
        comp['is_quote_status'] = tweet.is_quote_status
        comp['is_a_retweet'] = tweet.retweeted
        comp['favorite_count'] = tweet.author.favourites_count
        comp['followers_count'] = tweet.author.followers_count
        comp['number_of_tweets_total'] = tweet.author.statuses_count      
        twitter_comp.append(comp)
    all_comps.extend(twitter_comp)  


# In[6]:


df = pd.DataFrame(all_comps)


# In[7]:


with open('./company_tweets.csv', 'a') as f:
    df.to_csv(f, header=False)

