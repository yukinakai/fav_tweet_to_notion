from dotenv import load_dotenv
import os

load_dotenv()

# Twitter
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
TWITTER_USER_ID = os.getenv('TWITTER_USER_ID')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

TWITTER_FIELDS_CONFIG = {
    'max_results': 5,
    'expansions': 'attachments.media_keys,author_id',
    'tweet.fields': 'attachments,author_id,created_at,id,referenced_tweets,text',
    'user.fields': 'name,username,profile_image_url',
    'media.fields': 'url'
}

# notion
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
