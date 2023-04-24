from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from social_media.models import Post, Comment, Hashtag
from social_media.permissions import IsAdminOrIfAuthenticatedReadOnly
from social_media.serializers import (
    PostSerializer,
    PostDetailSerializer,
    PostListSerializer,
    CommentSerializer,
    HashtagSerializer
)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PostPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "list":
            return PostListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        return serializer.save(user=self.request.user, post_id=post_id)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, post_id=post_id)
