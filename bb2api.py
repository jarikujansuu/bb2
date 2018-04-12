import requests


pc = 'pc'
ps4 = 'ps4'
xbox1 = 'xb1'


class Client(object):
    apikey = None

    def __init__(self, apikey):
        self.apikey = apikey

    def fetch(self, path, params=None):
        if not params:
            params = {}
        params['key'] = self.apikey

        result = requests.get(f'http://web.cyanide-studio.com/ws/bb2{path}/', params).json()
        return result if result else {'matches': []}  # matches endpoints return just false

    def coaches(self, league=None, competition=None, platform=None, limit=None):
        return self.fetch(
            path='/coaches',
            params={
                'league': league,
                'competition': competition,
                'platform': platform,
                'limit': limit
            }
        ).get('coaches') or []

    def teams(self, league=None, competition=None, platform=None, limit=None):
        return self.fetch(
            path='/teams',
            params={
                'league': league,
                'competition': competition,
                'plaform': platform,
                'limit': limit
            }
        ).get('teams') or []

    def team(self, name=None, id=None):
        return self.fetch(
            path='/team',
            params={
                'name': name,
                'id': id
            }
        ).get('team')

    def matches(self, league=None, competition=None, platform=None, limit=None, start=None, end=None, version=2):
        return self.fetch(
            path='/matches',
            params={
                'league': league,
                'competition': competition,
                'platform': platform,
                'limit': limit,
                'start': start,
                'end': end,
                'bb': version
            }
        ).get('matches') or []

    def match(self, uuid, platform=None,version=2):
        return self.fetch(
            path='/match',
            params={
                'match_id': uuid,
                'platform': platform,
                'bb': version
            }
        ).get('match')

    def hall_of_fame(self, league=None, competition=None, platform=None,limit=None,exact_league_name=True):
        return self.fetch(
            path='/halloffame',
            params={
                'league': league,
                'competition': competition,
                'platform': platform,
                'limit': limit,
                'exact': int(exact_league_name)
            }
        )

    def contests(self, league=None, competition=None, status=None, round=None, platform=None,limit=None,exact_league_name=True):
        return self.fetch(
            path='/contests',
            params={
                'league': league,
                'competition': competition,
                'status': status,
                'round': int(round) if round else None,
                'platform': platform,
                'limit': limit,
                'exact': int(exact_league_name) if exact_league_name else None
            }
        ).get('upcoming_matches') or []

    def ladder(self, league=None, competition=None, platform=None, ladder_size=None):
        return self.fetch(
            path='/ladder',
            params={
                'league': league,
                'competition': competition,
                'platform': platform,
                'ladder_size': ladder_size
            }
        ).get('ranking') or []

