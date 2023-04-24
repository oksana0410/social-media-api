from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("posts/?<post_id>/comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social-media"
