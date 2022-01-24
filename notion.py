import requests
import json
from config import config
import twitter
import sys


def create_url():
    url = "https://api.notion.com/v1/pages"
    return url

def create_header():
    NOTION_API_KEY = config.NOTION_API_KEY
    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
    return headers

def body_params_create_block_external_image(url):
    return {'object': 'block',
            'type': 'image',
            'image': {
                'type': 'external',
                'external': {
                    'url': url
                }
            }
            }

def body_params_create_block_external_video(url):
    return {'object': 'block',
            'type': 'heading_2',
            'heading_2': {
                'text': [{'type': 'text', 'text': {'content': url}}]
            }
            }

def body_params_create_block_embed(url):
    return {'object': 'block',
            'type': 'embed',
            'embed': {
                'url': url
            }
            }

def body_params_create_page(data):
    return {
        'icon': {
            'external': {
                'url': data['author_profile_image_url']
            }
        },
        'properties': {
            'ID': {
                'title': [
                    {
                        'text': {
                            'content': data['author_name']
                        }
                    }
                ]
            },
            'Tweeted_at': {
                'date': {'start': data['tweeted_at']}
            },
            'URL': {
                'url': "https://twitter.com/{author_id}/status/{tweet_id}".format(author_id=data['author_id'],tweet_id=data['tweet_id'])
            },
            'Text': {
                "rich_text": [
                    {
                        "text": {
                            "content": data['text']
                        }
                    }
                ]
            },
            'Author_username': {
                "rich_text": [
                    {
                        "text": {
                            "content": data['author_username']
                        }
                    }
                ]
            },
            'Tweet_id': {
                "rich_text": [
                    {
                        "text": {
                            "content": data['tweet_id']
                        }
                    }
                ]
            },
        }
    }

def format_data(data):
    database_id = config.NOTION_DATABASE_ID
    body_params = body_params_create_page(data)
    body_params['parent'] = {'database_id': database_id}

    children = list()
    if 'attached_media_url' in data:
        for media_url in data['attached_media_url']:
            if media_url == 'video':
                children.append(body_params_create_block_external_video(media_url))
            else:
                children.append(body_params_create_block_external_image(media_url))
    if 'referenced_tweets' in data:
        for referenced_tweet in data['referenced_tweets']:
            children.append(body_params_create_block_embed(referenced_tweet))
    body_params['children'] = children

    return body_params

def connect_to_endpoint(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def main():
    url = create_url()
    headers = create_header()
    data = twitter.main()
    for datum in data:
        body_params = format_data(datum)
        json_response = connect_to_endpoint(url, headers, body_params)
        print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
