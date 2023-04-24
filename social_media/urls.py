from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, HashtagViewSet, CommentCreateView

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:pk>/comment-create/",
        CommentCreateView.as_view(),
        name="create_comment",
    ),
]

app_name = "social-media"
