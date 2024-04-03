from datetime import datetime

import pytz
from extensions import scheduler
from .crawl import melon_chart_top100_crawler, melon_chart_hot100_crawler, melon_chart_day_crawler, \
    melon_chart_month_crawler, \
    melon_chart_week_crawler
from .crawl_billboard import billboard_chart_hot100_crawler, billboard_chart_billboard200_crawler, \
    billboard_chart_global200_crawler
from .event_listener import init_event_listener

timezone = pytz.timezone('America/Atikokan')


def init():
    init_event_listener()
    scheduler.add_job(
        func=melon_chart_top100_crawler,
        trigger="cron",
        minute="1",
        id="melon_chart_top100_crawler",
        name="melon_chart_top100_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_hot100_crawler,
        trigger="cron",
        minute="2",
        id="melon_chart_hot100_crawler",
        name="melon_chart_hot100_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_day_crawler,
        trigger="cron",
        hour="9",
        minute="1",
        id="melon_chart_day_crawler",
        name="melon_chart_day_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_week_crawler,
        trigger="cron",
        week="1",
        minute="1",
        id="melon_chart_week_crawler",
        name="melon_chart_week_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=melon_chart_month_crawler,
        trigger="cron",
        week="1",
        minute="1",
        id="melon_chart_month_crawler",
        name="melon_chart_month_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=billboard_chart_hot100_crawler,
        trigger="cron",
        week="1",
        minute="1",
        id="billboard_chart_hot100_crawler",
        name="billboard_chart_hot100_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=billboard_chart_billboard200_crawler,
        trigger="cron",
        week="1",
        minute="1",
        id="billboard_chart_billboard200_crawler",
        name="billboard_chart_billboard200_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )

    scheduler.add_job(
        func=billboard_chart_global200_crawler,
        trigger="cron",
        week="1",
        minute="1",
        id="billboard_chart_global200_crawler",
        name="billboard_chart_global200_crawler",
        next_run_time=datetime.now(timezone),
        replace_existing=True,
    )
