def match(match_data):
    home = match_data['teams'][0]
    visitor = match_data['teams'][1]
    winner = home if home['score'] >= visitor['score'] else visitor
    loser = home if home['score'] < visitor['score'] else visitor

    def team_ranking(rankings, team):
        result = {}
        if team['rank'] == 1:
            result['position'] = 'leader'
        else:
            position_value = team['rank'] / rankings['teams_count']
            if position_value < 3/6:
                result['position'] = 'top'
            elif position_value < 4/6:
                result['position'] = 'near_top'
            elif position_value > 5/6:
                result['position'] = 'bottom'
            else:
                result['position'] = 'middle'

            score_per_round = (rankings['rounds_count'] - match_data['round']) / (rankings['top_score'] - team['score'])
            if score_per_round <= 1:
                result['chances'] = 'ok'
            elif score_per_round <= 2:
                result['chances'] = 'bad'
            elif score_per_round <= 3:
                result['chances'] = 'theoretical'
            else:
                result['chances'] = 'none'
        return result

    if winner['score'] == loser['score']:
        result = 'draw'
    elif winner['score'] > (loser['score'] + 3):
        result = 'big_win'
    else:
        result = 'win'

    def team_result(team):
        if result == 'win' or 'big_win':
            return 'win' if team == winner else 'loss'
        else:
            return 'draw'

    rankings = match_data.get('ranking')
    if rankings:
        ranking = dict()
        ranking['home'] = team_ranking(rankings, rankings['home'])
        ranking['home']['result'] = team_result(home)
        ranking['home']['name'] = home['teamname']
        ranking['home']['other'] = visitor['teamname']
        ranking['visitor'] = team_ranking(rankings, rankings['visitor'])
        ranking['visitor']['result'] = team_result(visitor)
        ranking['visitor']['name'] = visitor['teamname']
        ranking['visitor']['other'] = home['teamname']
    else:
        ranking = None

    return {
        'league': match_data['leaguename'],
        'competition': match_data['competitionname'],
        'result': result,
        'home': home['teamname'],
        'home_score': home['score'],
        'visitor': visitor['teamname'],
        'visitor_score': visitor['score'],
        'winner': winner['teamname'],
        'winner_score': winner['score'],
        'loser': loser['teamname'],
        'loser_score': loser['score'],
        'match_categorization': match_categorization(match_data),
        'ranking': ranking
    }


def match_categorization(match_data):
    home = match_data['teams'][0]
    visitor = match_data['teams'][1]
    winner = home if home['score'] >= visitor['score'] else visitor
    loser = home if home['score'] < visitor['score'] else visitor

    def violence():
        deaths = winner['inflicteddead'] + loser['inflicteddead']
        casualties = winner['inflictedcasualties'] + loser['inflictedcasualties']
        if deaths > 2:
            return {'value': 'deadly', 'weight': 5}
        elif deaths + casualties > 5:
            return {'value': 'brutal', 'weight': 3}
        elif deaths + casualties == 0:
            return {'value': 'gentle', 'weight': 1}
        return None

    def scoring():
        if winner['score'] + loser['score'] > 6:
            return {'value': 'td_frenzy', 'weight': 5}
        elif winner['score'] + loser['score'] > 4:
            return {'value': 'lot_of_td', 'weight': 2}
        return None

    def events():
        event_types = [
            'inflictedpasses',
            'inflictedinterceptions',
            'inflictedtouchdowns',
            'inflictedcasualties',
            'inflictedtackles',
            'inflictedko',
            'inflictedinjuries',
            'inflicteddead',
            'inflictedpushouts',
        ]
        winner_count = 0
        loser_count = 0
        for _, count in filter(lambda a: a[0] in event_types, winner.items()):
            winner_count += count
        for _, count in filter(lambda a: a[0] in event_types, loser.items()):
            loser_count += count
        return None

    def weighted_random(values):
        total = sum(map(lambda a: a['weight'], values))
        selected = random.uniform(0, total)

        current = 0.0
        for value in values:
            weight = value.get('weight') or 1
            if selected <= current + weight:
                return value['value']
            current += weight

    return weighted_random(list(filter(None, [violence(), scoring(), events()])))
