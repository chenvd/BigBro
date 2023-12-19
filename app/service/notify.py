import json

import requests

from app import schema
from app.db.models import Rule, RuleHistory


def send(rule: Rule, history: RuleHistory):
    for notify in rule.notifies:
        payload = json.loads(notify.payload)
        try:
            if notify.type == 'telegram':
                send_telegram(rule, history, payload)
            elif notify.type == 'webhook':
                send_webhook(rule, history, payload)
        except Exception as e:
            pass


def send_telegram(rule: Rule, history: RuleHistory, payload: dict[str, str]):
    url = f'https://api.telegram.org/bot{payload["token"]}/sendMessage'

    message = '\n'.join([value.content for value in history.values if value.is_new])

    requests.post(url=url, json={
        'chat_id': payload['chat_id'],
        'text': f'''
<b>《{rule.name}》{history.content}</b>
{message}
        ''',
        'parse_mode': 'HTML'
    })


def send_webhook(rule: Rule, history: RuleHistory, payload: dict[str, str]):
    url = payload['webhook_url']
    data = {
        'rule': {
            'id': rule.id,
            'name': rule.name,
            'url': rule.url
        },
        'history': {
            'status': history.status,
            'content': history.content,
            'values:': [{
                'content': i.content,
                'values': i.values,
                'is_new': i.is_new
            } for i in history.values]
        }
    }
    requests.post(url, json=data)
