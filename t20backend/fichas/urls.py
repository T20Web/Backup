from rest_framework import routers
from .views import FichaViewSet

router = routers.DefaultRouter()
router.register(r'fichas', FichaViewSet, basename='ficha')

urlpatterns = router.urls