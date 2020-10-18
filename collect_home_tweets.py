from text_mining import TextCleaner
import tweepy
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def get_top_tweets(min_freq=1):
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    public_tweets = api.home_timeline(count=20)
    users = []
    all_tweets = []
    for i in public_tweets:
        if i.user.screen_name not in users and i.user.screen_name != 'bitxt':
            users.append(i.user.screen_name)
            text = i.text.lower()
            text = " ".join(list(set(text.split())))
            all_tweets.append(text)
    all_tweets = " ".join(all_tweets)
    all_tweets = " ".join([i for i in all_tweets.split() if '@' not in i])
    all_tweets = " ".join([i for i in all_tweets.split() if '_' not in i])

    cleaner = TextCleaner()
    clean_df = cleaner.get_clean_text(text=all_tweets)
    clean_df = clean_df[clean_df['count'] > min_freq]

    now = datetime.now()
    time = f"{now.year}{now.strftime('%m')}{now.strftime('%d')}"

    clean_df['date'] = time
    clean_df['hour'] = now.hour
    return clean_df