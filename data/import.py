import config
import os

from datetime import datetime, timedelta, timezone
from bb2api import Client
from util.encryption import decrypt_env_json
from util.time import datetime_utc

api = Client(decrypt_env_json('BB2_API_SECRETS')['apikey'])
schedule_hours = int(os.environ['SCHEDULE_HOURS'])


def import_config(event, context):
    return list(map(lambda a: a['value'], config.load('import')))


def import_matches(event, context):
    endtime = datetime.now(timezone.utc) - timedelta(hours=schedule_hours)
    for target in event:
        return list(filter(
            lambda a: datetime_utc(a['finished']) > endtime,
            api.matches(
                league=target['league'],
                competition=target.get('competition'),
                start=endtime - timedelta(hours=3)
            )
        ))
