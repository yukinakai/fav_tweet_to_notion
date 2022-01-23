import requests
import json
from config import config


def create_url():
    id = config.TWITTER_USER_ID
    url = "https://api.twitter.com/2/users/{}/liked_tweets".format(id)
    return url

def create_params():
    bearer_token = config.TWITTER_BEARER_TOKEN
    headers = {
        'Authorization': f"Bearer {bearer_token}",
    }
    params = config.TWITTER_FIELDS_CONFIG
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

def main():
    url = create_url()
    headers, params = create_params()
    json_response = connect_to_endpoint(url, headers, params)
    # paginationのハンドリングが必要
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()