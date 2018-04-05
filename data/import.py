import base64
import boto3
import json
import os

from datetime import datetime, timedelta
from bb2api import Client

kms = boto3.client('kms')
secrets = json.loads(kms.decrypt(CiphertextBlob=base64.b64decode(os.environ['BB2']))[u'Plaintext'])

api = Client(secrets['apikey'])
schedule_hours = int(os.environ['SCHEDULE_HOURS'])


def import_matches(event, context):
    return api.matches(league=os.environ['LEAGUE'], start=datetime.now() - timedelta(hours=schedule_hours))