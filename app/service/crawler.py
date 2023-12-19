import datetime
from datetime import datetime
from typing import List

import requests
import re
from lxml import etree
from urllib.parse import urlparse

from app import schema
from app.db import SessionFactory
from app.db.models import Rule, RuleHistory, RuleHistoryValue
from app.exception import BizException
from app.service import notify


def favicon(url: str):
    url_parts = urlparse(url)
    origin = f'{url_parts.scheme}://{url_parts.hostname}'

    response = requests.get(url).text
    html = etree.HTML(response)
    matched = html.xpath('//link[@rel="shortcut icon"]')
    if len(matched) > 0:
        href = matched[0].get('href')
        if href.startswith('./'):
            return f"{origin}{href[1:]}"
        else:
            return href
    else:
        return f"{origin}/favicon.ico"


def execute(rule: Rule) -> List[schema.CrawlerResult]:
    headers = {}
    if rule.user_agent:
        headers['User-Agent'] = rule.user_agent
    if rule.cookies:
        headers['Cookie'] = rule.cookies
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'

    response = requests.get(rule.url, headers=headers).text

    results: List[schema.CrawlerResult] = [schema.CrawlerResult(content=response)]

    if rule.xpath:
        html = etree.HTML(response)
        matched = html.xpath(rule.xpath)
        if len(matched) > 0:
            for index in range((len(matched)) if rule.is_list else 1):
                results[index] = schema.CrawlerResult(content=matched[index].text)
        else:
            raise BizException('XPath未匹配到内容')

    if rule.regex:
        for index in range(len(results)):
            result = results[index]
            matched = re.search(rule.regex, result.content)
            if matched:
                content = matched.group(0)
                groups = ','.join(matched.groups())
            else:
                content = None
                groups = None
            result.content = content
            result.groups = groups
        if len(list(filter(lambda i: i.content, results))) == 0:
            raise BizException("正则表达式未匹配到内容")

    return results


def do_job(rule_id: int):
    db = SessionFactory()
    with db:
        try:
            rule = Rule.get(db, rule_id)
            results = execute(rule)

            latest = db.query(RuleHistory).filter_by(rule_id=rule.id, status=1).order_by(
                RuleHistory.id.desc()).limit(1).one_or_none()
            if latest:
                has_new = False
                values: List[RuleHistoryValue] = []
                for result in results:
                    matched = list(filter(lambda i: i.content != result.content, latest.values))
                    if matched:
                        has_new = True
                    values.append(RuleHistoryValue(**result.model_dump(), is_new=not not matched))
                if has_new:
                    history = RuleHistory(rule_id=rule.id, status=1, content='发现更新')
                    history.values = values
                    rule.latest_update = datetime.now()
                    rule.has_new = True
                else:
                    history = RuleHistory(rule_id=rule.id, status=0, content='暂无更新')
                db.add(history)
            else:
                history = RuleHistory(rule_id=rule.id, status=1, content='发现更新')
                history.values = [RuleHistoryValue(**item.model_dump(), history_id=history.id, is_new=True) for item in
                                  results]
                db.add(history)
                rule.latest_update = datetime.now()
                rule.has_new = True
        except BizException as e:
            db.rollback()
            history = RuleHistory(rule_id=rule.id, status=-1, content=e.detail)
            db.add(history)
            rule.latest_update = datetime.now()
            rule.has_new = True
        except Exception as e:
            db.rollback()
            history = RuleHistory(rule_id=rule.id, status=-1, content='发生未知错误')
            db.add(history)
            rule.latest_update = datetime.now()
            rule.has_new = True

        rule.latest_execute = datetime.now()
        db.add(rule)
        db.commit()

        if rule.status != 0:
            notify.send(rule, history)
