# Fast Food and Twitter
## Mapping Consumer Sentiment to Better Understand and Target Customers

NOTE: This README is a work in progress 

The intersection of fast food consumers and Twitter users is surprisingly wide. Contrary to conventional wisdom, the vast majority of fast food consumers are middle class- in fact, even the most affluent are only [marginally less likely](https://www.cnn.com/2017/07/12/health/poor-americans-fast-food-partner/index.html) (80% vs. 73%) than the poorest to eat fast food on a regular basis. Fast food consumption also trends young, peaking in the 18-29 age group. Likewise, *Twitter* trends young and affluent. Of its ~69 million regular users in the United States, [36% are in the 18-29 age group]   (https://blog.hootsuite.com/twitter-statistics/) (its largest demographic) and these users are more likely than not to have some college education. Equally, if not more important, 74% of Twitter users get at least some of their news on Twitter (more than the 68% of *Facebook* users) and a similar number follow brands for product updates and promotions. 

With numbers like these, building and maintaining a strong brand presence on Twitter is vital to stay competitive. In that light, I collected 418,000 customer (and ~20,000 company) tweets over six weeks (March 9- April 19) to evaluate brand favorability and consumer behavior for 11 fast food chains (targeting tweets that used the company's handle, ex. 'I love @McDonalds!'). With scripts collecting data four times per day on an Amazon Web Service EC2, I sought to use customer profiles and behavior to predict favorability toward a brand, hierarchically clustered consumers by company to aid customer acquisition, identified the best times and days for marketing, and looked at the relationship between brand favorability and stock price over time (targeting the following publicly traded companies for that reason: *McDonald's, Chipotle, Starbucks, Denny's, Wendy's, Dunkin Donuts, Domino's, Sonic, Shake Shack, Wingstop, Cracker Barrel*). 

## #The Data

This project presented a number of challenges. First, Twitter's API limits the number of tweets you can capture per day (without paying), preventing comprehensive collection and making the analysis reliant on Twitter's algorithm for randomizing sample tweets. Second, I conducted the majority of the analysis on a three week subset (due to external academic constraints) and at fixed hours, introducing likely time and seasonal bias in the data collection (although I have rerun most of the code on the full dataset with only very small variations in result). Third, there is no way to ensure that tweets are from genuine customers/consumers and not purchased endorsements or automated accounts ([some estimates suggest 15% of Twitter 'users' are actually bots](https://www.cnbc.com/2017/03/10/nearly-48-million-twitter-accounts-could-be-bots-says-study.html)). Fourth, using natural language processing to assess consumer preference is an error prone process (I tested prebuilt NLTK & TextBlob sentiment analyzers); I manually assessed a randomized subset of tweets and identified a misclassification rate of ~20% across three dummy categories (positive, negative, neutral).  

Facing these challenges, I tested various solutions (detailed throughout this README) and do my best to be fully transparent where results might be biased. For example, of the 418,000+ tweets collected, I had to eliminate nearly 240,000 due to missing or incomplete data. Likewise, I  dropped two companies from the dataset (*Potbelly & Red Robin*) due to insufficient observations. Still, the datasets were rich for exploration. Before any feature creation/transformation, the scraped customer dataset included 14 features and the scraped company dataset included 11 features (including: tweet & profile text, time, retweets, favorites, user verification, followers, total tweets, etc.; I also scraped for geographic location, but most users don't report it or report it imprecisely). 

## #Brand Positivity

I measured brand positivity using the mean [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) sentiment score (also referred to here as *polarity*)- a floating number between -1 (totally negative) & 1 (totally positive) per tweet.  TextBlob's polarity score is robust to negation (ex. 'not great', is scored -1, 'great' 1 ), can interpret emoticon sentiment (ex. 😀 1 and 😒 -1), and is built off of the academic work of the [respected *pattern* library](https://www.clips.uantwerpen.be/pages/pattern-web). Overall, polarity skewed positive- 44% of tweets were positive, 15% were negative, and 43% were neutral.

The graphic below shows brand positivity, company by company, as a measure of the polarity of customer mentions:

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/Mean_Positivity.png" height="460" width="500">
</p>

In addition to showing substantial variation in brand performance (all, on average, more positive than negative), the results are reassuring of the validity of the metric based on prior knowledge of brand popularity. The top performer, Shake Shack, is renowned for its carefully crafted branding and the (generally positive) hype surrounding [its burgers](https://www.investors.com/research/the-new-america/how-shake-shacks-growth-may-catch-up-to-its-hype/). In contrast, the worst performer, Domino's, has had its brand repeatedly battered by scandal and, despite what the [*Harvard Business Review* suggests](https://hbr.org/2016/11/how-dominos-pizza-reinvented-itself), has not completely rebounded. 

However, including a measure of only unique tweets (the orange bars below)- eliminating retweets and multiple tweets by the same user- shows a clear decline in overall sentiment and a reordering of the companies' comparative scores. 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/polarity.png" height="420" width="560">
</p>

Starbucks and Shake Shack both see 6% declines in overall favorability, while Wendy's favorability increases by 2%. The mechanism for the decrease is not only through fewer positive tweets, but also a proportional increase in negative tweets. That the change in favorability score varies widely across companies can lend itself to various interpretations. It could be purely random variation (although the likelihood from a two-sided t-test that the group's share a mean is only ~2.6%). Some companies could be paying for trend-setters to create more 'retweetable' content (NOTE: these are NOT retweets of the company's tweets- I purposely did not include those in this analysis) or it could indicate that some companies are purchasing retweets- [a common strategy](http://www.businessinsider.com/fake-twitter-followers-test-2012-8). 

## #New Customer Acquisition & Company Clustering

In a mature and competitive market like fast food in the US, capturing a competitor's customers is key to growing market share. However, it is important to know *which* company's customers you should target. I analyzed the profiles of each company's customers (transforming text profiles (grouped into a corpus by company) into a numeric TF-IDF matrix) to identify company clusters based on customer similarities.

The heatmap below shows the cosine similarities between company customers(**larger numbers/lighter colors** indicate **more** similarity between company customers. *Cosine similarity* is a measure of the directional similarity of vectors). In other words, how much in common each company's customers have with the customers of every other company as a function of their written profiles.  

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/heatmap.png" height="420" width="560">
</p>

By this metric, Chipotle and Wendy's have the most similar customers while Wingstop and Starbucks customers are the most dissimilar. Overall, McDonald's has the most in common with the other companies (narrowly edging out Dunkin Donuts) and Wingstop has the least in common with other companies (by a wide margin- and it is not a function of company size, Wingstop's market cap is bigger than Denny's & Sonic's). 

Another method I used to assess customer similarity was hierarchical clustering (a method that iterates through data points and identifies the 'nearest' similar data points- I locally optimized with 'Ward's method' which seeks to minimize variance between clusters, still using the TF-IDF vectors). The graphic below, called a *dendrogram*, shows the clustering of companies (the *lower* on the chart two companies are connected, the more similar their customers are).

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/dendrogram.png" height="420" width="560">
</p>

Just as with cosine similarities, Chipotle and Wendy's customers share the most profile information in common, trailed closely by the pairings of Dunkin Donuts & Sonic and Domino's & McDonald's. Again, Wingstop customers are markedly different from all other company groupings. 

The graphic below shows customer Twitter activity (the *median* customer's number of followers and number of tweets). Additionally, I chose to vary the colors by the percentage of company customers that are verified (i.e. a public figure- 2% of all unique customers in the dataset are verified vs. 0.06% of twitter users overall) from **red** (more verified customers) to **black** (fewer verified customers). 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/consumer_popularity.png" height="420" width="560">
</p>

Shake Shack customers are the most popular (most followers) and second most active (behind Wingstop). 4% of them are also verified (the most in the group as a percentage, and second behind Dunkin Donuts in absolute number). Interestingly, however, this is not driving their brand favorability. Non-verified Shake Shack customers are 20% *more* positive about the company than their verified customers (of course, verified users are more likely to be paid influencers or official partners than unverified users). In the same vein, verified customers are only 7% more positive than non-verified across all companies. 

Domino's and McDonalds are exceptions with regard to the verification effect. Verified customers are 52% more positive (than non-verified customers) about Domino's and 38% more positive about McDonald's. This may be an indication of the emphasis these companies place on purchasing positive endorsements. 

## #Building Popularity & Positivity

Another measure of brand favorability is the 'favorite count' (the equivalent of 'liking' a post on *Facebook*). In the sample, favorite count is heavily skewed (84% of tweets have 0 favorites, while the top tweet has 857). Below you can see the mean sentiment score contrasted with the mean favorite count. 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/company_pops.png" height="420" width="560">
</p>

As you can see above, there is no obvious visual (or quantitative for that matter) correlation between mean favorite count and mean sentiment. This runs against the influence of [hypercriticism](http://bigthink.com/ideafeed/is-negative-content-more-likely-to-go-viral) (the idea that the public perceives negative statements to be more intelligent, making them more popular) and instead suggests that, at least in this sample, neither positivity nor negativity drive the popularity of a tweet. Therefore, it may be no fool's errand to encourage positive customer tweeting (ex. through clever hashtags) in the hopes of virility and boosting sales/favorability. 

This is in marked contrast to the favorite count of a company's own tweets, which has a positive correlation with overall brand favorability  (0.31 Pearson correlation). This is not a contradiction. It makes intuitive sense that having more customers willing to favorite company tweets (inevitably positive or neutral in sentiment) would indicate more customers willing to tweet their own positive reaction to the brand. 

The likelihood to tweet positively or favorite company tweets is, unsurprisingly, not uniformly distributed across customers. The graphic below shows the percentage of unique words and percentage of correctly spelled words in customer profiles (averaged by companies) to demonstrate how a customer's attention to detail/public presentation affects tweet sentiment. 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/sentiment_vocab.png" height="460" width="700">
</p>

In both cases, there are positive correlations with sentiment (0.31 for unique, 0.30 for correctly spelled). The more conscientious the profile creator, measured by a more diverse vocabulary and accurately spelled profile, the more likely to tweet positively. On the margin, this might be a factor to consider when targeting new customers. 

## #Marketing by Day & Time

Over the six weeks of data collected, Tuesday narrowly edged out Thursday for the highest overall volume of tweets (with nearly 3x Sunday's tweet volume- the slowest day). Tuesday also had the highest overall positive sentiment, while Thursday fell to 4th behind Monday and Wednesday. Undoubtedly, running ads when Twitter is heavily trafficked with positive consumers is an advantageous strategy for customer retention marketing. 

Below, you can see the sentiment of customer tweets by company across each day of the week (the width of the line being a measure of the mean favorite count by day):

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/weekdaysentiment.png" height="420" width="560">
</p>

The peak in Tweet positivity on Tuesday is unmistakable, although there is substantial cross-company variation (Cracker Barrel peaks Thursday, Domino's Wednesday). Likewise, Saturday and Sunday clearly trail the weekdays in positive sentiment. This is not to say that these days shouldn't be a focus of online engagement. Targeting dissatisfied customers with direct messages or targeting other companies' dissatisfied customers could both be winning strategies.    

The graphic below shows the average daily mentions by company. In contrast to the large differences in daily sentiment across companies, there is high covariance in tweet volume. Unfortunately, however, it can't be ruled out that this isn't at least somewhat biased by the artificial limits Twitter put on the number of Tweets I could scrape per day. 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/mentions_by_day.png" height="365" width="630">
</p>

Identifying the optimal time of day to target customers was trickier. At any given collection time, Twitter returns a 'randomized' subset for a given query- not necessarily uniformly distributed across time. Likewise, I automated the script to collect customer tweets at 5pm and 12am EST daily (9am & 2pm EST for company tweets), scattering the times to account for scrape limits. To solve this problem, I looked at the negativity *rate* (i.e. the number of negative tweets as a percentage of all tweets at a given hour). 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/negrate2.png" height="460" width="1000">
</p>

From the graphic above, 4pm and 9am jump out as times with high tweet volume and low negativity rate- ideal for targeting large numbers of satisfied customers. On the other hand, and perhaps unsurprisingly, negativity tends to peak overnight when there are also fewer customers tweeting.

## #Company Behavior and Effectiveness

The graphic below shows the companies ordered by their market capitalization alongside each company's total number of Twitter followers and total number of tweets. Alongside each figure is a visual representation of brand favorability (the **larger** and **redder** the square, the *more popular* the brand).

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/comp_behav.png" height="320" width="560">
</p>

Brand favorability on Twitter is not a function of the market valuation or a measure of its total followers/tweets (in fact the latter have small negative correlations with favorability, while market cap has only a small positive correlation). However, as you can see in the next graphic, *tweets per follower* does have a strong positive correlation with overall brand favorability.

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/per_user_sent.png" height="380" width="620">
</p>

Looking at a basic 2-degree polynomial OLS model, ~50% of company variation in sentiment was captured looking only at company tweets per follower. This is a strong indication that actively tweeting *directly* to your customers (and reaching a higher percentage of them) will pay dividends in reputation and favorability. Companies, to varying degrees, seem to already understand this. Of the ~20,000 company tweets I collected, 90.8% were direct customer outreach (i.e. they started with "@CustomerName"). 

Given that the vast majority of tweets in the sample were direct customer outreach, rather than general marketing tweets, an analysis of company hashtag use is likely unreliable (i.e. I can't assume that I captured all company hashtag campaigns and therefore can't assume to capture customer reuse rates accurately). However, in so far as companies use their hashtags regularly in direct customer outreach, the graphic below shows company hashtag use and their effectiveness in eliciting reuse.

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/hash_use.png" height="225" width="640">
</p>

Again, before any interpretation, it is worth reiterating that this sample is small and likely biased (companies may differ in when they use hashtags (i.e. for/not for direct customer outreach), but not in overall use- here, we disproportionately see use in direct outreach). Having said that, there is a strong positive correlation between the volume of company hashtag use and customer reuse (even after controlling for Cracker Barrel- an obvious outlier in the sample). Likewise, there is a strong positive correlation between customer hashtag reuse and tweet sentiment. It stands to reason that using more hashtags, specifically more *unique* hashtags (the more diverse the collection of company hashtags the stronger the positive correlation with sentiment), can help drive brand favorability. 

## #Interplay of Sentiment & Stock Price

When a customer tweets positively about a company, it bodes well for their future brand loyalty and perhaps that of their followers and friends. While this may be reflected in future quarterly sales numbers, it is not obvious if changes in customer feedback/sentiment will be reflected in the stock market in the short-term. Working with such a short window (limited to a 3 week subset of the data), I was interested in identifying whether there was enough evidence of an interplay to justify further research. The graphic below shows daily sentiment scores (top), daily change in stock price (middle), and daily volume of trades (bottom). 

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/stock_sentiment_2.png" height="420" width="740">
</p>

To the naked eye, there clearly seems to be some interplay between change in stock price and sentiment, but it might not be daily (Pearson correlations with daily sentiment were 0.059 for stock and -0.04 for volume- both insignificant at the 10% level). To account for the possible presence of delayed impacts, I looked at the day to day *change* in sentiment and experimented with some lagged indicators. There was a negligible negative correlation (-0.05) without a time adjustment as well as with change in stock price lagged by one day, but a sizable positive correlation with change in sentiment lagged by one day (0.147- likely what we are seeing in the graphic and significant at the 1% level from a permutation test). These relationships are not, if you were curious, being driven by Twitter discussion of company stocks (only 184 of the 66,542 Tweets in the sample include any mention of 'stock' or 'market'). 

While a longer time-series and a robust accounting of market noise are required to reach any serious conclusions, there is  evidence of a short-term interplay between change in Twitter sentiment and stock price. However, the direction of the interplay is unclear. In fact, the evidence suggests that we need to be cautious for two-way or reverse causality. Rather than changes in sentiment driving stock price (what we might expect/hope to find), changes in the market might be driving customer tweet sentiment through elevated/deflated investor moods. Controlling for overall market direction, and/or identifying a workable instrumental variable, could help parse this out. 

## #Predicting Tweet Sentiment from a Customer's Profile

Finally, I was interested to see if it was possible to predict tweet sentiment (positive or negative- I removed 'neutral' tweets) based purely on written profiles (or 'bio'- which Twitter limits to 160 characters). Given an approximate 20% error rate in the initial tweet sentiment classification (a rought estimate I calculated by personally scoring a random subset of 100 tweets), this process imposed a maximum accuracy of 80% (even if I had a reported accuracy of 100%, I would have to assume that ~20% were originally misclassified and thus incorrectly classified in the report). Additionally, I assumed a baseline accuracy of 75%, rather than random guessing and 50%, because of class imbalance (in the training data, 75% of tweets were positive, 25% negative). 

Initially, and in the graphic below, I looked to predict tweet sentiment across all companies (using the 3 week data subset). The graphic below shows various model performances (for this graphic, using only default hyperparameters).

<p align="left">
  <img src="https://github.com/slevin886/twitter_fast_food_analysis/blob/master/images/classifier%20performance.png" height="420" width="640">
</p>

The initial results weren't encouraging. Recall (*correctly classified positive / (correctly classified positive + incorrectly classified negative*) is alarmingly high and reflects the tendency of several models to classify too few profiles as likely to tweet negatively. As a result, precision (*percentage of correctly classified positive / total classified positive*) tends to hover around the baseline (the models are predicting positive far too often).
