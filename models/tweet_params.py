class Tweet:
    def tweet_fields_config(self):
        return {
            'max_results': 100,
            'expansions': 'attachments.media_keys,author_id,referenced_tweets.id,referenced_tweets.id.author_id',
            'tweet.fields': 'attachments,author_id,created_at,id,text,referenced_tweets',
            'user.fields': 'name,username,profile_image_url',
            'media.fields': 'url'
        }