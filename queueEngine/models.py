from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Queue(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queues')
    name = models.CharField(max_length=255) 
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    allow_qr_code = models.BooleanField(default=True)
    allow_search_in = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} - {self.host.username}"
    
    def get_current_position(self, queuer):
        try:
            entry = self.entries.get(queuer=queuer, status='waiting')
            return self.entries.filter(joined_at__lt=entry.created_at, status='waiting').count() + 1
        except QueueEntry.DoesNotExist:
            return None

    def get_queue_length(self):
        return self.entries.filter(status='waiting').count()
    
    def get_qr_data(self):
        pass


class QueueEntry(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('served', 'Served'),
        ('serving', 'Being Served'),
    ]

    JOIN_METHOD_CHOICES = [
        ('qr_code', 'QR Code'),
        ('search_in', 'Search In'),
        ('host_added', 'Host Added'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='entries')
    queuer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queue_entries')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    join_method = models.CharField(max_length=15, choices=JOIN_METHOD_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    served_at = models.DateTimeField(blank=True, null=True)
    left_at = models.DateTimeField(blank=True, null=True)

    estimated_wait_time = models.IntegerField(blank=True, null=True)  # in minutes

    class Meta:
        ordering = ['joined_at']
        unique_together = ('queue', 'queuer', 'status')

    def __str__(self):
        return f"{self.queuer.username} in {self.queue.name} - {self.status}"
    
    def get_position(self):
        return self.queue.get_current_position(self.queuer)