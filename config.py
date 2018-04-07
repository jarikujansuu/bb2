import boto3
import uuid
from boto3.dynamodb.conditions import And, Key


db = boto3.resource('dynamodb')
table = db.Table('bb2-config')


def add(category, value, subset=None):
    item = {
        'category': category,
        'id': f'{subset}:{uuid.uuid4().hex}' if subset else uuid.uuid4().hex,
        'value': dict(value)
    }
    table.put_item(Item=item)
    return item


def delete(entry):
    if 'value' in entry:
        del entry['value']

    table.delete_item(Key=entry)


def load(category, subset=None):
    hash_key = Key('category').eq(category)
    expression = And(hash_key, Key('id').begins_with(f'{subset}:')) if subset else hash_key

    return table.query(KeyConditionExpression=expression)['Items']
