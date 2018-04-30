from commentator.writer import match_report
from birdy.twitter import UserClient
from util.encryption import decrypt_env_json

secrets = decrypt_env_json('TWITTER_API_SECRETS')

twitter = UserClient(
    secrets['consumer_key'],
    secrets['consumer_secret'],
    secrets['access_token'],
    secrets['access_secret']
)


def tweet(matches, context=None):
    if matches:
        for match in matches:
            previous = None
            for text in match_report(match):
                previous = twitter.api.statuses.update.post(
                    status=text,
                    in_reply_to_status_id=previous
                ).data['id']

        return {
            'matches': list(map(lambda a: a['uuid'], matches))
        }
    else:
        return {'matches': []}
