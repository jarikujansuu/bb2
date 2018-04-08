import base64
import boto3
import json
import os

kms = boto3.client('kms')


def decrypt_env_json(name):
    return json.loads(decrypt_env(name))


def decrypt_env(name):
    return kms.decrypt(CiphertextBlob=base64.b64decode(os.environ[name]))[u'Plaintext']
