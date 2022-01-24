import requests
import json
from config import config


def create_url():
    id = config.TWITTER_USER_ID
    url = "https://api.twitter.com/2/users/{}/liked_tweets".format(id)
    return url

def create_params(pagination_token=None):
    bearer_token = config.TWITTER_BEARER_TOKEN
    headers = {
        'Authorization': f"Bearer {bearer_token}",
    }
    params = config.TWITTER_FIELDS_CONFIG
    if pagination_token is not None:
        params['pagination_token'] = pagination_token
    return headers, params

def connect_to_endpoint(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
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
            ## 別途リツイート対応が必要
            row['referenced_tweets'] = datum['referenced_tweets']
        if 'attachments' in datum:
            media_url_list = list()
            for media_key in datum['attachments']['media_keys']:
                try:
                    attached_media_url =  media[media_key]['url']
                except:
                    ## 別途動画対応が必要
                    attached_media_url = 'video'
                media_url_list.append(attached_media_url)
            row['attached_media_url'] = media_url_list
        data.append(row)
    return data

def main():
    url = create_url()
    data = list()
    pagination_token = None
    result_count = 1
    i = 0
    while result_count > 0:
        # Twitter APIから任意のデータを取得する
        headers, params = create_params(pagination_token)
        json_response = connect_to_endpoint(url, headers, params)
        _data = format_data(json_response)
        data = data + _data
        # 次のループのために必要なデータを取得
        pagination_token = json_response['meta']['next_token']
        result_count = json_response['meta']['result_count']
        # テスト用
        i = i + 1
        if i == 2:
            break
    return data


if __name__ == "__main__":
    main()