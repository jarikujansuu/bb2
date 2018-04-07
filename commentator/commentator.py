import base64
import boto3
import json
import os
from commentator.writer import match_report
from birdy.twitter import UserClient

kms = boto3.client('kms')
secrets = json.loads(kms.decrypt(CiphertextBlob=base64.b64decode(os.environ['TWITTER']))[u'Plaintext'])

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
