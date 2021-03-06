from commentator.templates import load_templates, random_template, snippet, deep_get
from pystache import render


def match_report(match_data):
    about_match = combine(map(
        lambda a: a(match_data),
        [
            competition,
            score
        ]
    ))

    if match_data.get('ranking'):
        ranking_texts = [
            ranking(match_data, match_data.get('ranking', {}).get('home')),
            ranking(match_data, match_data.get('ranking', {}).get('visitor'))
        ]
    else:
        ranking_texts = []

    return filter(None, [about_match] + ranking_texts)


def combine(texts):
    return ' '.join(filter(None, texts))


def competition(match):
    return render(
        template=random_template(load_templates('competition')),
        context=match
    )


def score(match):
    return render(
        template=random_template(load_templates('score')[match['result']]),
        context=match,
        match_description=snippet('match_description', match['match_categorization'])
    )


def ranking(match, team_ranking):
    if team_ranking:
        templates = deep_get(
            load_templates('ranking'),
            team_ranking.get('position'),
            team_ranking.get('result'),
            team_ranking.get('chances')
        )
        if templates:
            return render(
                template=random_template(templates),
                context={**match, **team_ranking}
            )
        return None

