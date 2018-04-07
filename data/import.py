import os
import config

from datetime import datetime, timedelta
from bb2api import Client
from util import decrypt_env_json

api = Client(decrypt_env_json('BB2_API_SECRETS')['apikey'])
schedule_hours = int(os.environ['SCHEDULE_HOURS'])


def import_config(event, context):
    return list(map(lambda a: a['value'], config.load('import')))


def import_matches(event, context):
    for target in event:
        return api.matches(
            league=target['league'],
            competition=target.get('competition'),
            start=datetime.now() - timedelta(hours=schedule_hours)
        )
