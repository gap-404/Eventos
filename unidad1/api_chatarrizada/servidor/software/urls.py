from rest_framework.routers import DefaultRouter
from .views import SoftwareViewSet

router = DefaultRouter()
router.register(r'software', SoftwareViewSet)

urlpatterns = router.urls
