from django.core.management.base import BaseCommand
from sentiment_analysis_app.models import Posts, Brands, Platforms
from utils.sentiment import analyze_sentiment
from utils.clean_data import clean_text
from django.utils.timezone import now
import requests
from decouple import config

class Command(BaseCommand):
    help = 'Crawl Facebook Page posts and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('--brand', type=str, required=True)
        parser.add_argument('--page_id', type=str, required=True)
        parser.add_argument('--limit', type=int, default=10)

    def handle(self, *args, **options):
        brand_name = options['brand']
        page_id = options['page_id']
        limit = options['limit']
        access_token = config('FACEBOOK_ACCESS_TOKEN')

        url = f"https://graph.facebook.com/v18.0/{page_id}/posts"
        params = {
            'access_token': access_token,
            'limit': limit,
            'fields': 'message,created_time,id,permalink_url'
        }

        try:
            brand = Brands.objects.get(name__icontains=brand_name)
            platform = Platforms.objects.get(name__iexact='Facebook')
        except (Brands.DoesNotExist, Platforms.DoesNotExist):
            self.stderr.write(self.style.ERROR("Brand or Platform 'Facebook' not found. Add them first."))
            return

        response = requests.get(url, params=params)
        data = response.json()

        for post_data in data.get('data', []):
            raw_text = post_data.get('message', '')
            cleaned_text = clean_text(raw_text)

            sentiment, confidence = analyze_sentiment(cleaned_text)

            post = Posts.objects.create(
                brand=brand,
                platform=platform,
                platform_0=platform.name,
                raw_text=raw_text,
                cleaned_text=cleaned_text,
                user_id=page_id,
                posted_at=post_data.get('created_time'),
                original_post_url=post_data.get('permalink_url'),
                language='en',
                reach_estimate=0,
                view_count=0,
                like_count=0,
                comment_count=0,
                followers_count=0,
                state='',
                country=''
            )

            post.sentimentresults_set.create(
                sentiment_label=sentiment,
                sentiment_score=confidence,
                processed_at=now()
            )

            self.stdout.write(self.style.SUCCESS(f"Inserted Facebook post: {cleaned_text[:60]}..."))
