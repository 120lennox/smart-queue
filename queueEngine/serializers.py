from .models import Queue, QueueEntry
from rest_framework import serializers

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = [
            'id',
            'host',
            'name',
            'description',
            'status',
            'created_at',
            'updated_at',
            'allow_qr_code',
            'allow_search_in',
        ]


class QueueEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueEntry
        fields = [
            'id',
            'queue',
            'queuer',
            'status',
            'join_method',
            'joined_at',
            'served_at',
            'left_at',
            'estimated_wait_time',
        ]