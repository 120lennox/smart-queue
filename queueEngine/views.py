from django.shortcuts import render
from rest_framework import viewsets
from .models import Queue, QueueEntry
from .serializers import QueueSerializer, QueueEntrySerializer


# Create your views here.
class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

class QueueEntryViewSet(viewsets.ModelViewSet):
    queryset = QueueEntry.objects.all()
    serializer_class = QueueEntrySerializer
