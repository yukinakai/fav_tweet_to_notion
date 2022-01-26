import requests
import sys
from config import config
from models import tweet_params
logger = config.logging_config()

tweet_params = tweet_params.Tweet()
def create_url():
    user_id = config.TWITTER_USER_ID
    url = "https://api.twitter.com/2/users/{}/liked_tweets".format(user_id)
    return url

def create_params(pagination_token=None):
    bearer_token = config.TWITTER_BEARER_TOKEN
    headers = {
        'Authorization': f"Bearer {bearer_token}",
    }
    params = tweet_params.tweet_fields_config()
    if pagination_token is not None:
        params['pagination_token'] = pagination_token
    return headers, params

def connect_to_endpoint(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(
            {
                'action': 'post notion endpoint',
                'statud_code': response.status_code,
                'message': response.text,
                'data': params
            }
        )
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def format_data(json_response):
    users = dict()
    for user in json_response['includes']['users']:
        user_id = user['id']
        user.pop('id')
        users[user_id] = user

    media = dict()
    if 'media' in json_response['includes']:
        for file in json_response['includes']['media']:
            media_key = file['media_key']
            file.pop('media_key')
            media[media_key] = file

    tweets = dict()
    if 'tweets' in json_response['includes']:
        for tweet in json_response['includes']['tweets']:
            tweet_id =  tweet['id']
            tweet.pop('id')
            tweets[tweet_id] = tweet

    data = list()
    for datum in json_response['data']:
        row = dict()
        row['tweeted_at'] = datum['created_at']
        row['tweet_id'] = datum['id']
        row['text'] = datum['text']

        author_id = datum['author_id']
        user_profiles = users[author_id]
        row['author_id'] = author_id
        row['author_name'] = user_profiles['name']
        row['author_username'] = user_profiles['username']
        row['author_profile_image_url'] = user_profiles['profile_image_url']

        if 'referenced_tweets' in datum:
            referenced_tweets = list()
            for referenced_tweet in datum['referenced_tweets']:
                tweet_id = referenced_tweet['id']
                author_id = tweets[tweet_id]['author_id']
                referenced_tweets.append('https://twitter.com/{author_id}/status/{tweet_id}'.format(author_id=author_id,tweet_id=tweet_id))
            row['referenced_tweets'] = referenced_tweets
        if 'attachments' in datum:
            attachments = list()
            for media_key in datum['attachments']['media_keys']:
                try:
                    attached_media_url =  media[media_key]['url']
                except:
                    ## temp code
                    attached_media_url = 'video'
                attachments.append(attached_media_url)
            row['attached_media_url'] = attachments

        data.append(row)
    return data

def main():
    url = create_url()
    data = list()
    pagination_token = None
    result_count = 1
    while result_count > 0:
        # get tweet data via twitter api
        headers, params = create_params(pagination_token)
        json_response = connect_to_endpoint(url, headers, params)
        result_count = json_response['meta']['result_count']
        # formatting data
        if result_count == 0:
            break
        try:
            _data = format_data(json_response)
        except KeyError as e:
            logger.error({
                'error': 'KeyError',
                'key': e,
                'url': url,
                'params': params,
                'data': json_response
            })
            sys.exit()
        data = data + _data
        # set token for next loop
        pagination_token = json_response['meta']['next_token']
        break # need to delete to get more than 100 tweet
    return data


if __name__ == "__main__":
    main()