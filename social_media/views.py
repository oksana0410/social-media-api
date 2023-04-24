from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_media.models import Post, Comment
from social_media.serializers import PostSerializer, PostDetailSerializer, PostListSerializer, LikeSerializer, \
    CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "list":
            return PostListSerializer
        if self.action == "add_like":
            return LikeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def add_like(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(data={"post": post.id, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        like = post.likes.filter(user=request.user).first()

        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)