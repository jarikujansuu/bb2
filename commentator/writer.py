import json
import os
import random
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
        'loser-score': loser['score']
    }


def load_templates(group):
    script_dir = os.path.dirname(__file__)
    return json.loads(open(f'{script_dir}/templates/{group}.json', encoding='utf-8').read())


def random_template(templates):
    total = sum(map(lambda a: a.get('weight') or 1.0, templates))
    selected = random.uniform(0, total)
    current = 0.0
    for template in templates:
        weight = template.get('weight') or 1
        if selected <= current + weight:
            return template['template']
        current += weight


def competition(match):
    return render(
        template=random_template(load_templates('competition')),
        context=match
    )


def score(match):
    return render(
        template=random_template(load_templates('score')[match['result']]),
        context=match
    )
