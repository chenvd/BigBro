import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db import SessionFactory
from app.db.models import Rule
from app.service import crawler


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def init(self):
        with SessionFactory() as db:
            rules = Rule.list(db)
            for rule in rules:
                if rule.status:
                    self.add(rule.id, cron=rule.cron)
        self.scheduler.start()

    def add(self, rule_id: int, cron: str):
        exist = self.scheduler.get_job(str(rule_id))
        if exist:
            self.scheduler.remove_job(exist.id)
        self.scheduler.add_job(crawler.do_job, trigger=CronTrigger.from_crontab(cron), id=str(rule_id),
                               args=[rule_id])

    def remove(self, rule_id: int):
        self.scheduler.remove_job(str(rule_id))

    def manually(self, rule_id: int):
        job = self.scheduler.get_job(str(rule_id))
        job.modify(next_run_time=datetime.datetime.now())

    def list(self):
        return self.scheduler.get_jobs()


scheduler = Scheduler()
