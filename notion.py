import requests
import json
from config import config


def create_url():
    url = "https://api.notion.com/v1/pages"
    return url

def create_params():
    NOTION_API_KEY = config.NOTION_API_KEY
    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
    return headers

def create_data():
    database_id = config.NOTION_DATABASE_ID
    return {
        'parent': {'database_id': database_id},
        'properties': {
            'Name': {
                'title': [
                    {
                        'text': {
                            'content': 'created by API'
                        }
                    }
                ]
            }
        }
    }

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
    headers = create_params()
    data = create_data()
    json_response = connect_to_endpoint(url, headers, data)
    # paginationのハンドリングが必要
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
