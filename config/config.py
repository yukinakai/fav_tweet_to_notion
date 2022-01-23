from dotenv import load_dotenv
import os

load_dotenv()
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
TWITTER_USER_ID = os.getenv('TWITTER_USER_ID')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

TWITTER_FIELDS_CONFIG = {
    'max_results': 5,
    'expansions': 'attachments.media_keys',
    'tweet.fields': 'attachments,author_id,created_at,id,referenced_tweets,text',
    'media.fields': 'url'
}