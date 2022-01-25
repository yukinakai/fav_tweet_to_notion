import notion
import twitter
import json

def main():
    tweets_in_notion = notion.get_tweets_in_notion()
    tweets = twitter.main()
    for tweet in tweets:
        if tweet['tweet_id'] in tweets_in_notion:
            continue
        json_response = notion.main(tweet)
        print(json.dumps(json_response, indent=4, sort_keys=True))



if __name__ == "__main__":
    main()