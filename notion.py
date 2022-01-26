import requests
import json
from config import config
from models import notion_params
logger = config.logging_config()

notion_page_prams = notion_params.NotionPage()
NOTION_DATABASE_ID = config.NOTION_DATABASE_ID

def create_header():
    NOTION_API_KEY = config.NOTION_API_KEY
    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
    return headers

def format_data(data):
    body_params = notion_page_prams.page(data)
    body_params['parent'] = {'database_id': NOTION_DATABASE_ID}

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
        logger.error(
            {
                'action': 'post notion endpoint',
                'statud_code': response.status_code,
                'message': response.text,
                'data': data
            }
        )
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweets_in_notion():
    headers = create_header()
    url = "https://api.notion.com/v1/databases/{}/query".format(NOTION_DATABASE_ID)
    payload = {"page_size": 5}
    has_more = True
    tweets_in_notion = list()
    while has_more:
        json_response = connect_to_endpoint(url, headers, payload)
        for result in json_response['results']:
            tweets_in_notion.append(result['properties']['Tweet_id']['rich_text'][0]['plain_text'])
        has_more = json_response['has_more']
        payload['start_cursor'] = json_response['next_cursor']
    tweets_in_notion = list(set(tweets_in_notion))
    return tweets_in_notion

def main(data):
    headers = create_header()
    url = "https://api.notion.com/v1/pages"
    body_params = format_data(data)
    json_response = connect_to_endpoint(url, headers, body_params)
    return json_response


if __name__ == "__main__":
    main()
