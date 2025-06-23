from django.core.management.base import BaseCommand
from sentiment_analysis_app.models import Posts, Brands, Platforms
from django.utils.timezone import now
from decouple import config
import praw
import re
from utils.sentiment import analyze_sentiment

class Command(BaseCommand):
    help = 'Crawl Reddit posts and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('--brand', type=str, required=True, help='Brand name to associate posts with')
        parser.add_argument('--keywords', type=str, required=True, help='Keywords to search on Reddit')
        parser.add_argument('--limit', type=int, default=10, help='Number of Reddit posts to fetch')

    def handle(self, *args, **options):
        brand_name = options['brand']
        keywords = options['keywords']
        post_limit = options['limit']

        reddit = praw.Reddit(
            client_id=config('REDDIT_CLIENT_ID'),
            client_secret=config('REDDIT_CLIENT_SECRET'),
            user_agent=config('REDDIT_USER_AGENT')
        )

        try:
            brand = Brands.objects.get(name__icontains=brand_name)
            platform = Platforms.objects.get(name__iexact='Reddit')
        except (Brands.DoesNotExist, Platforms.DoesNotExist):
            self.stderr.write(self.style.ERROR("Brand or Platform 'Reddit' not found. Add them first."))
            return

        subreddit = reddit.subreddit("all")
        results = subreddit.search(keywords, limit=post_limit)

        for submission in results:
            raw_text = submission.title + "\n" + submission.selftext
            cleaned_text = re.sub(r"http\S+", "", raw_text)

            sentiment, confidence = analyze_sentiment(cleaned_text)

            post = Posts.objects.create(
                brand=brand,
                platform=platform,
                platform_0=platform.name,
                raw_text=raw_text,
                cleaned_text=cleaned_text,
                user_id=str(submission.author) if submission.author else "Unknown",
                posted_at=now(),
                original_post_url=submission.url,
                language='en',
                reach_estimate=submission.score,
                view_count=0,
                like_count=submission.score,
                comment_count=submission.num_comments,
                followers_count=0,
                state='',
                country=''
            )

            post.sentimentresults_set.create(
                sentiment_label=sentiment,
                sentiment_score=confidence,
                processed_at=now()
            )

            self.stdout.write(self.style.SUCCESS(f"Inserted Reddit post: {cleaned_text[:60]}..."))
