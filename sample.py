import requests
from config import config
import json

NOTION_API_KEY = config.NOTION_API_KEY
headers = {
    'Authorization': f"Bearer {NOTION_API_KEY}",
    'Content-Type': 'application/json',
    'Notion-Version': '2021-08-16',
}
page_id = "9e7fd8b3a7a045c2ad536c7d2a5fcff7"
url = "https://api.notion.com/v1/pages/{}".format(page_id)

response = requests.get(url, headers=headers)

print(json.dumps(response.json()))



#
# block_id = "d69b3e4baae24f13857ce41078e3e6e8"
# url = "https://api.notion.com/v1/blocks/{}".format(block_id)
# response = requests.request("GET", url, headers=headers)
#
# print(response.text)
