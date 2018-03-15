import tweepy
from tweepy import OAuthHandler
from twitter_codes import consumer_secret, consumer_key, access_secret, access_token
import pandas as pd
from tqdm import tqdm

auth = OAuthHandler(consumer_secret, consumer_key)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


try:
  redirect_url = auth.get_authorization_url(signin_with_twitter=True)
except tweepy.TweepError:
  print('Error! Failed to get request token.')


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


all_comps = []
for company in tqdm(rest_names):
  list_tweets = []
  for tweet in tweepy.Cursor(api.search, q=company, retry_delay=5, wait_on_rate_limit=True, lang="en").items(250):
    if not tweet.retweeted:
      if not tweet.is_quote_status:
        if not tweet.user.screen_name == company[1:]:
          twitter_dic = {}
          twitter_dic['Company'] = company
          twitter_dic['text'] = tweet.text
          twitter_dic['retweet_count'] = tweet.retweet_count
          twitter_dic['favorite_count'] = tweet.favorite_count
          twitter_dic['user_followers_count'] = tweet.author.followers_count
          twitter_dic['user_name'] = tweet.author.name
          twitter_dic['user_location'] = tweet.author.location
          twitter_dic['user_coordinates'] = tweet.coordinates
          twitter_dic['number_of_user_tweets'] = tweet.author.statuses_count
          twitter_dic['user_is_verified'] = tweet.author.verified
          twitter_dic['user_profile_text'] = tweet.author.description
          twitter_dic['number_of_people_they_follow'] = tweet.author.friends_count
          twitter_dic['time_tweeted'] = tweet.created_at
          twitter_dic['unique_code'] = tweet.id_str
          list_tweets.append(twitter_dic)
  all_comps.extend(list_tweets)


df = pd.DataFrame(all_comps)


with open('fastfood.csv', 'a') as f:
  df.to_csv(f, header=False)
