"""Log scheduler events."""
import logging

from apscheduler.events import (
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_SUBMITTED,
)

from extensions import scheduler


logger = logging.getLogger(__name__)


def init_event_listener():
    scheduler.add_listener(job_missed, EVENT_JOB_MISSED)
    scheduler.add_listener(job_error, EVENT_JOB_ERROR)
    scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)
    scheduler.add_listener(job_added, EVENT_JOB_ADDED)
    scheduler.add_listener(job_removed, EVENT_JOB_REMOVED)
    scheduler.add_listener(job_submitted, EVENT_JOB_SUBMITTED)

def job_missed(event):
    """Job missed event."""
    with scheduler.app.app_context():
        logger.warning('Job %s missed - %s', event.job_id, event.scheduled_run_time)
        # print(event)  # noqa: T001



def job_error(event):
    """Job error event."""
    with scheduler.app.app_context():
        logger.error('Job %s error - %s', event.job_id, event.scheduled_run_time)


def job_executed(event):
    """Job executed event."""
    with scheduler.app.app_context():
        logger.info('Job %s executed - %s', event.job_id, event.scheduled_run_time)


def job_added(event):
    """Job added event."""
    with scheduler.app.app_context():
        logger.info('Job %s added', event.job_id)


def job_removed(event):
    """Job removed event."""
    with scheduler.app.app_context():
        logger.info('Job %s removed', event.job_id)


def job_submitted(event):
    """Job scheduled to run event."""
    with scheduler.app.app_context():
        logger.info('Job %s submitted', event.job_id)


