import base64
import boto3
import json
import os
import config

from datetime import datetime, timedelta
from bb2api import Client

kms = boto3.client('kms')
secrets = json.loads(kms.decrypt(CiphertextBlob=base64.b64decode(os.environ['BB2']))[u'Plaintext'])

api = Client(secrets['apikey'])
schedule_hours = int(os.environ['SCHEDULE_HOURS'])


def import_config(event, context):
    return map(lambda a: a['value'], config.load('import'))


def import_matches(event, context):
    for target in event:
        return api.matches(
            league=target['league'],
            competition=target.get('competition'),
            start=datetime.now() - timedelta(hours=schedule_hours)
        )
