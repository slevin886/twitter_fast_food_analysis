# Fast Food and Twitter
## Mapping Consumer Sentiment to Better Understand and Target Customers

NOTE: This README is a work in progress 

Fast food consumers and Twitter users overlap more than you may think. Contrary to the conventional wisdom, the vast majority of fast food consumers are middle class- in fact, even the most affluent are only [marginally less likely](https://www.cnn.com/2017/07/12/health/poor-americans-fast-food-partner/index.html) (80% vs. 73%) than the poorest to eat fast food on a regular basis. Fast food consumption also trends young, peaking in the 18-29 age group. Likewise, *Twitter* trends young and affluent. Of its ~69 million regular users in the United States, [36% are in the 18-29 age group](https://blog.hootsuite.com/twitter-statistics/) and they are more likely than not to have some college education. Equally if not more important, 74% of users get at least some of their news on Twitter (more than the 68% of *Facebook* users) and a similar number follow brands for product updates and promotions. 

With numbers like these, building and maintaining a strong brand presence on Twitter is vital to stay competitve. In that light, I collected 170,000 customer (and ~10,000 company) tweets over three weeks (March 9-30) to evaluate brand favorability and consumer behavior for 11 fast food chains (targeting tweets that used the companies handle, ex.'@McDonalds'). With scripts collecting data four times per day on an Amazon Web Service EC2, I used customer profiles and behavior to predict favorability toward a brand, identified the best times and days for marketing, and examined the interplay of favorability and stock price (targeting the following independent, publicly traded companies for that reason: *McDonald's, Chipotle, Starbucks, Denny's, Wendy's, Dunkin Donuts, Domino's, Sonic, Shake Shack, Wingstop, Cracker Barrel*). 

## #Limitations 

This project presented a number of challenges- some surmountable, others not. First, Twitter's API limits the number of tweets you can capture per day (without paying), making a comprehensive analysis impossible and introducing likely bias in data collection (only 3 weeks of data, likely artificial concentrations at certain times of day). Second, there is no way to ensure that tweets are from customers or even people for that matter ([some estimates suggest 15% of Twitter 'users' are actually bots](https://www.cnbc.com/2017/03/10/nearly-48-million-twitter-accounts-could-be-bots-says-study.html)), therefore, measuring brand favorability based-on an (largely) indiscriminate collection of company mentions may be inherently flawed. Third, natural langauge processing for favorability is an error prone process (I tested prebuilt NLTK & textblob sentiment analyzers- manually scoring ) which only adds to the complexity of prediction and clustering. 

Facing these challenges, I tested various solutions (detailed throughout this README) and do my best to be fully transparent where results may be biased by flaws in the methodology.  

## #Brand Positivity

I measured brand positivity by taking the mean [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) polarity score (a floating number between -1 (totally negative) & 1 (totally positive) of each tweet on a company-by-company basis.  TextBlob's polarity score is robust to negation (ex. 'not great', is scored ~-1, 'great' ~1 ),can interpret emoticon sentiment :), and is built off of the academic work of the [respected *pattern* library](https://www.clips.uantwerpen.be/pages/pattern-web). Overall, and including retweets and multiple tweets from individual users,  44% of tweets were positive, 15% were negative, and 43% were neutral.

The graphic below shows brand positivity as a measure of the polarity of customer mentions:

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/Mean_Positivity.png" height="460" width="500">
</p>

In addition to showing substantial variation in brand performance (all, on average, more positive than negative), the results are reassuring of the validity of the metric based on prior knowledge of brand popularity. The top performer, Shake Shack, is renown for its carefully crafted branding and the (generally positive) hype surrounding [its burgers and market expansion](https://www.investors.com/research/the-new-america/how-shake-shacks-growth-may-catch-up-to-its-hype/). In contrast, the worst performer, Domino's, has had its brand repeatedly battered by scandal and, despite what the [*Harvard Business Review* suggests](https://hbr.org/2016/11/how-dominos-pizza-reinvented-itself), has not completely rebounded. 

#Positivity & Popularity

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/company_pops.png" height="420" width="560">
</p>

#Consumer Satisfaction by Day

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/weekdaysentiment.png" height="420" width="560">
</p>

#Negativity Rate & Time of Day

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/negrate2.png" height="460" width="1000">
</p>

#Company Tweet Characteristics & Customer Reuse

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/comp_tweet_behav.png" height="500" width="640">
</p>

#Company Behavior on Twitter

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/comp_twit_use.png" height="420" width="560">
</p>

#Consumer Behavioral Profiles

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/consumer_behavior.png" height="400" width="950">
</p>

#Sentiment & Stock Price

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/stock_sentiment_2.png" height="420" width="740">
</p>

#Vocabulary & Sentiment

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/sentiment_vocab.png" height="460" width="700">
</p>
