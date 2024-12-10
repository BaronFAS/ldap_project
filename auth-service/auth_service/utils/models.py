import uuid

from django.db import models


class AbstractCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseSyncJob(models.Model):
    STATE_PENDING = "STATE_PENDING"
    STATE_RUNNING = "STATE_RUNNING"
    STATE_SENT = "STATE_SENT"
    STATE_ERROR = "STATE_ERROR"
    STATE_COMPLETED = "STATE_COMPLETED"
    STATES = (
        (STATE_PENDING, STATE_PENDING),
        (STATE_RUNNING, STATE_RUNNING),
        (STATE_SENT, STATE_SENT),
        (STATE_ERROR, STATE_ERROR),
        (STATE_COMPLETED, STATE_COMPLETED),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    attempts = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=32, choices=STATES, default=STATE_PENDING)
    detail_info = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["created"]
