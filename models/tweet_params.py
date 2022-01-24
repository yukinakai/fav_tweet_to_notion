class Tweet:
    def tweet_fields_config(self):
        return {
            'max_results': 5,
            # 'start_time': '2019-01-01T17:00:00Z',
            # 'end_time': '2020-12-12T01:00:00Z',
            # 'pagination_token': '7140w',
            'expansions': 'attachments.media_keys,author_id,referenced_tweets.id,referenced_tweets.id.author_id',
            'tweet.fields': 'attachments,author_id,created_at,id,text,referenced_tweets',
            'user.fields': 'name,username,profile_image_url',
            'media.fields': 'url'
        }