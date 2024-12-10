from prometheus_client import Counter
from prometheus_client import Histogram


cloud_core_task_runs_total = Counter(
    "cloud_core_task_runs_total",
    "Total calls to a celery task",
    ["task_name", "status"],
)

cloud_core_task_duration_seconds = Histogram(
    "cloud_core_task_duration_seconds",
    "Call time of a celery task",
    ["task_name"],
)
