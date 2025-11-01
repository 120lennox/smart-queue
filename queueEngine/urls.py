from .views import QueueViewSet, QueueEntryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'queues', QueueViewSet)
router.register(r'queue-entries', QueueEntryViewSet)

urlpatterns = router.urls