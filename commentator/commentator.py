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


def tweet(event, context):
    matches = event['matches']

    for match in matches:
        twitter.api.statuses.update.post(status=match_report(match))

    return {
        'matches': list(map(lambda a: a['uuid'], matches))
    }
