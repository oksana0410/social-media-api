from rest_framework import serializers

from social_media.models import Hashtag, Post, Comment, Like


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ("id", "tag")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "user", "comment", "created_at")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=True,
        slug_field="email",
        read_only=True
    )

    class Meta:
        model = Like
        fields = ("id", "user")


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "content", "photos", "user", "hashtag")
        read_only_fields = ("id", "user")


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        slug_field="tag", read_only=True, many=True
    )
    likes = serializers.IntegerField(source="likes.count")

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "photos",
            "user",
            "hashtags",
            "likes"
        )


class PostDetailSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "photos",
            "user",
            "comments",
            "likes"
        )
