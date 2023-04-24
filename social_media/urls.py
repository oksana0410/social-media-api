from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CommentViewSet, HashtagViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social-media"
