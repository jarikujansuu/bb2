import json
import os
import random
from pystache import render


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


def snippet(group, key):
    templates = load_templates(f'snippets/{group}')
    if key in templates:
        return render(random_template(templates[key]))
    return ''
