from django.core.management.base import BaseCommand
from sentiment_analysis_app.models import Posts, Brands, Platforms
from utils.sentiment import analyze_sentiment
from utils.clean_data import clean_text
from django.utils.timezone import now
import requests
from decouple import config

class Command(BaseCommand):
    help = 'Crawl Instagram Business account posts and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('--brand', type=str, required=True)
        parser.add_argument('--limit', type=int, default=10)

    def handle(self, *args, **options):
        brand_name = options['brand']
        limit = options['limit']
        access_token = config('INSTAGRAM_ACCESS_TOKEN')
        ig_user_id = config('INSTAGRAM_USER_ID')

        url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
        params = {
            'access_token': access_token,
            'limit': limit,
            'fields': 'caption,timestamp,permalink,id'
        }

        try:
            brand = Brands.objects.get(name__icontains=brand_name)
            platform = Platforms.objects.get(name__iexact='Instagram')
        except (Brands.DoesNotExist, Platforms.DoesNotExist):
            self.stderr.write(self.style.ERROR("Brand or Platform 'Instagram' not found. Add them first."))
            return

        response = requests.get(url, params=params)
        data = response.json()

        for media_data in data.get('data', []):
            raw_text = media_data.get('caption', '')
            cleaned_text = clean_text(raw_text)

            sentiment, confidence = analyze_sentiment(cleaned_text)

            post = Posts.objects.create(
                brand=brand,
                platform=platform,
                platform_0=platform.name,
                raw_text=raw_text,
                cleaned_text=cleaned_text,
                user_id=ig_user_id,
                posted_at=media_data.get('timestamp'),
                original_post_url=media_data.get('permalink'),
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

            self.stdout.write(self.style.SUCCESS(f"Inserted Instagram post: {cleaned_text[:60]}..."))
