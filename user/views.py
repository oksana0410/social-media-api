from django.contrib.auth import get_user_model
from rest_framework import generics, status, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Follow
from user.serializers import UserSerializer, FollowingSerializer, FollowerSerializer, FollowSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogoutView(APIView):

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        email = self.request.query_params.get("email")
        queryset = self.queryset

        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset


class FollowUserView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        followed_user = get_object_or_404(get_user_model(), pk=pk)

        if user == followed_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(user=user, followed_user=followed_user)

        if created:
            return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

        return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowUserView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        followed_user = get_object_or_404(get_user_model(), pk=pk)

        follow = Follow.objects.filter(user=user, followed_user=followed_user).first()

        if follow:
            follow.delete()
            return Response({"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK)

        return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.following.all()


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.followers.all()
