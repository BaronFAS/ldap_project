from datetime import datetime

import pytz
from django.utils import timezone


def get_now() -> datetime:
    return timezone.now()


def to_utc_tz(timestamp: datetime) -> datetime:
    return timestamp.replace(tzinfo=pytz.UTC)
