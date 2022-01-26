import notion
import twitter
import json
from config import config
logger = config.logging_config()

def main():
    tweets_in_notion = notion.get_tweets_in_notion()
    logger.info(
        {
            'status': 'success',
            'action': 'get tweets in notion'
        }
    )

    tweets = twitter.main()
    logger.info(
        {
            'status': 'success',
            'action': 'get tweets from twitter'
        }
    )

    for tweet in tweets:
        if tweet['tweet_id'] in tweets_in_notion:
            continue
        notion.main(tweet)
    logger.info(
        {
            'status': 'success',
            'action': 'create page on notion'
        }
    )


if __name__ == "__main__":
    main()