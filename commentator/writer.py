import random
from commentator.templates import load_templates, random_template, snippet
from pystache import render


def match_report(match_data):
    m = match(match_data)
    return ' '.join(
        filter(
            None,
            map(lambda a: a(m), [
                competition,
                score
            ])
        )
    )


def match(match_data):
    home = match_data['teams'][0]
    visitor = match_data['teams'][1]
    winner = home if home['score'] >= visitor['score'] else visitor
    loser = home if home['score'] < visitor['score'] else visitor

    if winner['score'] == loser['score']:
        result = 'draw'
    elif winner['score'] > (loser['score'] + 3):
        result = 'big-win'
    else:
        result = 'win'

    return {
        'league': match_data['leaguename'],
        'competition': match_data['competitionname'],
        'result': result,
        'home': home['teamname'],
        'home-score': home['score'],
        'visitor': visitor['teamname'],
        'visitor-score': visitor['score'],
        'winner': winner['teamname'],
        'winner-score': winner['score'],
        'loser': loser['teamname'],
        'loser-score': loser['score'],
        'match-categorization': match_categorization(match_data)
    }


def match_categorization(match_data):
    home = match_data['teams'][0]
    visitor = match_data['teams'][1]
    winner = home if home['score'] >= visitor['score'] else visitor
    loser = home if home['score'] < visitor['score'] else visitor

    def violence():
        deaths = winner['inflicteddead'] + loser['inflicteddead']
        casualties = winner['inflictedinjuries'] + loser['inflictedinjuries']
        if deaths > 3:
            return {'value': 'deadly', 'weight': 5}
        elif deaths + casualties > 5:
            return {'value': 'brutal', 'weight': 3}
        elif deaths + casualties == 0:
            return {'value': 'gentle', 'weight': 1}
        return None

    def scoring():
        if winner['score'] + loser['score'] > 6:
            return {'value': 'td-frenzy', 'weight': 5}
        elif winner['score'] + loser['score'] > 4:
            return {'value': 'lot-of-td', 'weight': 2}
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

        print(f'ANALYZE: event-count: {winner_count + loser_count}, winner-count: {winner_count}, loser-count: {loser_count}')
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


def competition(match):
    return render(
        template=random_template(load_templates('competition')),
        context=match
    )


def score(match):
    return render(
        template=random_template(load_templates('score')[match['result']]),
        context=match,
        match_description=snippet('match-description', match['match-categorization'])
    )
