from datetime import datetime

import pytz
from extensions import scheduler
from .crawl import melon_chart_crawler, melon_chart_hot100_crawler, melon_chart_day_crawler
from .event_listener import init_event_listener

timezone = pytz.timezone('America/Atikokan')
def init():
    init_event_listener()
    scheduler.add_job(
        func=melon_chart_crawler,
        trigger="cron",
        minute="1",
        id="melon_chart_crawler",
        name="melon_chart_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_hot100_crawler,
        trigger="cron",
        minute="1",
        id="melon_chart_hot100_crawler",
        name="melon_chart_hot100_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_day_crawler,
        trigger="cron",
        hour="0",
        minute="1",
        id="melon_chart_day_crawler",
        name="melon_chart_day_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )
