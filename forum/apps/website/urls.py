from rest_framework.routers import DefaultRouter

from forum.apps.website import views


router = DefaultRouter(trailing_slash=False)
router.register(r'', views.TopicViewSet)
urlpatterns = router.urls
