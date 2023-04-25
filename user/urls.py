from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView, LogoutView, UserViewSet, FollowUserView, UnfollowUserView, \
    FollowingListView, FollowersListView

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("", include(router.urls)),
    path("users/<int:pk>/follow/", FollowUserView.as_view(), name="follow"),
    path("users/<int:pk>/unfollow/", UnfollowUserView.as_view(), name="unfollow"),
    path("users/following/", FollowingListView.as_view(), name="following"),
    path("users/followers/", FollowersListView.as_view(), name="followers"),
]

app_name = "user"
