from data import competitions
from util.util import grouped


def extend_matches_with_rank(matches, context=None):
    if matches:
        def team_ranking(id, rankings):
            ranking = next((a for a in rankings if a['team']['id'] == id), None)
            return ranking['team']

        extended = []
        for competition_id, by_competition in grouped(matches, lambda a: a['idcompetition']):
            for round, by_round in grouped(by_competition, lambda a: a['round']):
                if round > 1:
                    rankings_data = competitions.get_ranking(competition_id, round - 1)
                    if rankings_data:
                        rankings = rankings_data['rankings']
                        for match in by_round:
                            home = match['teams'][0]['idteamlisting']
                            visitor = match['teams'][1]['idteamlisting']
                            home_ranking = team_ranking(home, rankings)
                            visitor_ranking = team_ranking(visitor, rankings)

                            match['ranking'] = {
                                'home': {
                                    'rank': int(home_ranking['rank']),
                                    'score': int(home_ranking['score'])
                                },
                                'visitor': {
                                    'rank': int(visitor_ranking['rank']),
                                    'score': int(visitor_ranking['score'])
                                },
                                'rounds_count': int(rankings_data['rounds_count']),
                                'teams_count': int(rankings_data['teams_count']),
                                'top_score': int(rankings[0]['team']['score'])
                            }
                            extended.append(match)
                    else:
                        extended.extend(by_round)
                else:
                    extended.extend(by_round)
        return extended

