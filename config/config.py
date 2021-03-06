from dotenv import load_dotenv
import os
import logging
import logging.handlers
load_dotenv()

# Twitter
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
TWITTER_USER_ID = os.getenv('TWITTER_USER_ID')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')


# notion
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')


# logging
def logging_config():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        fmt = logging.Formatter(
            '%(asctime)s:' \
            '%(levelname)s:' \
            '%(filename)s:' \
            '%(lineno)s:' \
            '%(message)s'
        )
        handler = logging.handlers.RotatingFileHandler(
            filename='config/logs.log',
            maxBytes=100000,
            backupCount=3
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        handler = logging.StreamHandler()
        handler.setFormatter(fmt)
        logger.addHandler(handler)


    return logger

if __name__ == "__main__":
    logging_config()