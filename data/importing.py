import config
import logging
import os

from bb2api import Client
from data import competitions
from datetime import datetime, timedelta, timezone
from util.encryption import decrypt_env_json
from util.util import grouped, unique
from util.time import datetime_utc

log = logging.getLogger()

api = Client(decrypt_env_json('BB2_API_SECRETS')['apikey'])
schedule_hours = int(os.environ['SCHEDULE_HOURS'])


def import_config(event, context=None):
    return list(map(lambda a: a['value'], config.load('import')))


def import_matches(to_import, context=None):
    endtime = datetime.now(timezone.utc) - timedelta(hours=schedule_hours)
    buffer = timedelta(hours=3)  # because get works on start time, but matches appear after they are finished

    matches = []
    for entry in to_import:
        matches.extend(list(filter(
            lambda a: datetime_utc(a['finished']) > endtime,
            api.matches(
                league=entry['league'],
                competition=entry.get('competition'),
                start=endtime - buffer
            )
        )))
    return matches


def add_round_to_matches(matches, context=None):
    extended = []

    for league, for_league in grouped(matches, lambda a: a['leaguename']):
        for competition, for_competition in grouped(for_league, lambda a: a['competitionname']):
            played = api.contests(
                league=league,
                competition=competition,
                status='played'
            )
            for match in for_competition:
                contest = next(contest for contest in played if contest['match_uuid'] == match['uuid'])
                match['round'] = contest['round']
                extended.append(match)
    return extended


def import_competitions(to_import, context=None):
    loaded = []
    for league, entries in grouped(to_import, lambda a: a['league']):
        for_league = api.competitions(league=league)
        competitions_to_import = list(map(lambda a: a.get('competition'), entries))
        if None not in competitions_to_import:
            included = filter(
                lambda a: True if a['name'] in competitions_to_import else False,
                for_league
            )
            loaded.extend(included)
        else:
            loaded.extend(for_league)

    updated = list(filter(competitions.update_competition, loaded))
    active = list(filter(lambda a: a['status'] == 1, loaded))
    return list(unique(updated + active))


def import_rankings(loaded, context=None):
    for competition in loaded:
        competitions.update_ranking(
            competition=competition,
            rankings=api.ladder(
                league=competition['league']['name'],
                competition=competition['name']
            )
        )


