import datetime
import uuid

from django.db import models


class Draft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exporter_id = models.TextField(default='')
    control_code = models.CharField(max_length=30, default='')
    activity = models.TextField(default='')
    destination = models.TextField(default='')
    usage = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    last_modified_at = models.DateTimeField(default=datetime.now, blank=True)
