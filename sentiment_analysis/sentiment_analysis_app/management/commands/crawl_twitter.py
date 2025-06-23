from django.core.management.base import BaseCommand
from sentiment_analysis_app.models import Posts, Brands, Platforms
from django.utils.timezone import now
from decouple import config
import tweepy
import re
from utils.clean_data import clean_tweet
from utils.sentiment import analyze_sentiment

class Command(BaseCommand):
    help = 'Crawl Twitter posts using Tweepy and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('--brand', type=str, required=True, help='Brand name to associate posts with')
        parser.add_argument('--keywords', type=str, required=True, help='Keywords to search on Twitter')
        parser.add_argument('--limit', type=int, default=10, help='Number of tweets to fetch')

    def handle(self, *args, **options):
        brand_name = options['brand']
        keywords = options['keywords']
        tweet_limit = options['limit']

        # Load Twitter credentials from .env
        auth = tweepy.OAuth1UserHandler(
            config('TWITTER_API_KEY'),
            config('TWITTER_API_SECRET'),
            config('TWITTER_ACCESS_TOKEN'),
            config('TWITTER_ACCESS_TOKEN_SECRET')
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)

        try:
            brand = Brands.objects.get(name__icontains=brand_name)
            platform = Platforms.objects.get(name__iexact='Twitter')
        except (Brands.DoesNotExist, Platforms.DoesNotExist):
            self.stderr.write(self.style.ERROR("Brand or Platform 'Twitter' not found. Add them first."))
            return

        for tweet in tweepy.Cursor(api.search_tweets, q=keywords, lang='en', tweet_mode='extended').items(tweet_limit):
            # Skip retweets
            if hasattr(tweet, 'retweeted_status'):
                continue

            raw_text = tweet.full_text
            cleaned = clean_tweet(raw_text)
            sentiment, confidence = analyze_sentiment(cleaned)

            post = Posts.objects.create(
                brand=brand,
                platform=platform,
                platform_0=platform.name,
                raw_text=raw_text,
                cleaned_text=cleaned,
                user_id=str(tweet.user.screen_name),
                posted_at=tweet.created_at,
                original_post_url=f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
                language='en',
                reach_estimate=tweet.user.followers_count,
                view_count=0,  # Twitter API does not give views
                like_count=tweet.favorite_count,
                comment_count=0,  # Not available in standard API
                share_count=tweet.retweet_count,
                followers_count=tweet.user.followers_count,
                state='',
                country=''
            )

            post.sentimentresults_set.create(
                sentiment_label=sentiment,
                sentiment_score=confidence,
                processed_at=now()
            )

            self.stdout.write(self.style.SUCCESS(f"Inserted Tweet: {cleaned[:60]}..."))
