import time

from django.db import transaction
from django.conf import settings
from celery.utils.log import get_task_logger

from utils.metrics import cloud_core_task_runs_total
from utils.metrics import cloud_core_task_duration_seconds
from cloud_core.celery import app


logger = get_task_logger(__name__)


class ProfiledTask(app.Task):
    """Celery task with simple time profiling and metrics for time and success/failure"""

    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        ret = super().__call__(*args, **kwargs)
        total_time = time.perf_counter() - start_time

        if settings.METRICS_ENABLED:
            cloud_core_task_duration_seconds.labels(
                task_name=self.name,
            ).observe(total_time)

        return ret

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if settings.METRICS_ENABLED:
            expected = False
            for t in self.throws:
                if isinstance(exc, t):
                    expected = True
                    break
            cloud_core_task_runs_total.labels(
                task_name=self.name,
                status="expected-error" if expected else "error",
            ).inc()
        logger.error(f"Failure detected for task {self}, {exc}")
        return super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        if settings.METRICS_ENABLED:
            cloud_core_task_runs_total.labels(
                task_name=self.name,
                status="success",
            ).inc()

        return super().on_success(retval, task_id, args, kwargs)


class TransactionAwareTask(ProfiledTask):
    """
    Task class which is aware of django db transactions and only executes tasks
    after transaction has been committed
    """

    def apply_async(self, *args, **kwargs):
        """
        Unlike the default task in celery, this task does not return an async
        result
        """
        transaction.on_commit(
            lambda: super(TransactionAwareTask, self).apply_async(*args, **kwargs),
        )
