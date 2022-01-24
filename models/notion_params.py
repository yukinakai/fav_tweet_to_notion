class NotionPage:
    def page(self, data):
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
                    'url': "https://twitter.com/{author_id}/status/{tweet_id}".format(author_id=data['author_id'],
                                                                                      tweet_id=data['tweet_id'])
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

    def child_external_image(self, url):
        return {'object': 'block',
            'type': 'image',
            'image': {
                'type': 'external',
                'external': {
                    'url': url
                }
            }
            }

    def child_external_video(self, url):
        return {'object': 'block',
            'type': 'heading_2',
            'heading_2': {
                'text': [{'type': 'text', 'text': {'content': url}}]
            }
            }

    def child_embed(self, url):
        return {'object': 'block',
            'type': 'embed',
            'embed': {
                'url': url
            }
            }
