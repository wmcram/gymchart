from datetime import timedelta
from django.utils import timezone
from django.db import models


class MetricType(models.Model):
    display_name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name

    def get_recent_data(self):
        cutoff = timezone.now() - timedelta(days=7)
        return self.datapoints.filter(timestamp__gte=cutoff).order_by("timestamp")


class TimeSeriesMetric(models.Model):
    metric_type = models.ForeignKey(
        MetricType, on_delete=models.CASCADE, related_name="datapoints")
    timestamp = models.DateTimeField(db_index=True)
    value = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['metric_type', 'timestamp']),
        ]
        ordering = ['timestamp']

    @classmethod
    def cleanup_old_data(cls):
        """Delete data older than 1 month"""
        cutoff = timezone.now() - timedelta(days=30)
        cls.objects.filter(timestamp__lt=cutoff).delete()
