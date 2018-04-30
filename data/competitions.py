import boto3
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import And, Attr, Key
from datetime import datetime

os.environ['COMPETITIONS_TABLE'] = 'bb2-dev-CompetitionTable-3ZDVWAZFMHA3'
db = boto3.resource('dynamodb').Table(os.environ['COMPETITIONS_TABLE'])


def add_contests(contests):
    for contest in contests:
        home = contest['opponents'][0]['team']['id']
        visitor = contest['opponents'][1]['team']['id']
        round = contest['round']

        try:
            db.put_item(
                Item={
                    'id': contest['competition_id'],
                    'entry': contest_id(home, visitor, round),
                    'league_name': contest['league'],
                    'competition_name': contest['competition'],
                    'teams': teams_id(home, visitor),
                    'home': home,
                    'visitor': visitor,
                    'round': round
                },
                ConditionExpression=Attr('id').not_exists()
            )
        except ClientError as e:
            # Ignore the ConditionalCheckFailedException, bubble up other exceptions.
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise


def add_match_data(contest):
    db.update_item(
        Key={
            'id': contest['id'],
            'entry': contest['entry']
        },
        UpdateExpression='SET #match = :match',
        ExpressionAttributeNames={'#match': 'match'},
        ExpressionAttributeValues={':match': {'uuid': contest['match']['uuid']}}
    )


def first_unplayed_match(match):
    items = db.query(
        KeyConditionExpression=And(
            Key('id').eq(match['idcompetition']),
            Key('entry').begins_with(
                contest_id_prefix(
                    match['teams'][0]['idteamlisting'],
                    match['teams'][1]['idteamlisting']
                )
            )
        ),
        FilterExpression=Attr('match').not_exists()
    )['Items']

    return next(iter(items), None)


def update_ranking(competition, rankings):
    def simplify_coach(team):
        team['coach'] = {
            'id': team['coach'].get('id') or '--',
            'name': team['coach'].get('name') or '--'
        }
        return team

    if rankings:
        db.put_item(Item={
            'id': competition['id'],
            'entry': ranking_id(competition['round']),
            'round': competition['round'],
            'rounds_count': competition['rounds_count'],
            'teams_count': competition['teams_count'],
            'rankings': list(map(simplify_coach, rankings))
        })


def get_ranking(competition, round):
    return db.get_item(
        Key={
            'id': competition,
            'entry': ranking_id(round)
        }
    ).get('Item')


def update_competition(competition):
    competition['id'] = competition['id']
    competition['entry'] = 'competition'
    competition['updated'] = timestamp()
    try:
        db.put_item(
            Item=competition,
            ConditionExpression=And(
                Attr('status').ne(competition['status']),
                Attr('round').ne(competition['round'])
            )
        )
        return True
    except ClientError as e:
        # Ignore the ConditionalCheckFailedException, bubble up other exceptions.
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        return False


def get_competition(id):
    db.get_item(Key={
        'id': id,
        'entry': 'competition'
    }).get('Item')


def teams_id(a, b):
    ids = [a,b]
    return f'{min(ids)}-{max(ids)}'


def contest_id(home, visitor, round):
    return f'c-{home}-{visitor}-{round}'


def contest_id_prefix(home, visitor):
    return f'c-{home}-{visitor}-'


def ranking_id(round):
    return f'ranking-{round}'


def timestamp():
    return datetime.utcnow().isoformat()