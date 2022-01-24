import requests
import json
from config import config
import twitter
import sys
from models import notion_params

notion_page_prams = notion_params.NotionPage()

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

def format_data(data):
    database_id = config.NOTION_DATABASE_ID
    body_params = notion_page_prams.page(data)
    body_params['parent'] = {'database_id': database_id}

    children = list()
    if 'attached_media_url' in data:
        body_params['properties']['With_media'] = {"type": "checkbox", "checkbox": True}
        for media_url in data['attached_media_url']:
            if media_url == 'video':
                children.append(notion_page_prams.child_external_video(media_url))
            else:
                children.append(notion_page_prams.child_external_image(media_url))
    if 'referenced_tweets' in data:
        for referenced_tweet in data['referenced_tweets']:
            children.append(notion_page_prams.child_embed(referenced_tweet))
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
