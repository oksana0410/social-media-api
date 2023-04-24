from rest_framework import serializers

from social_media.models import Hashtag, Post, Comment


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ("id", "tag")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "comment", "created_at")


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "content", "photos", "user", "hashtag")
        read_only_fields = ("id", "user")


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        slug_field="tag", read_only=True, many=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "photos",
            "user",
            "hashtags",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        slug_field="comment", read_only=True, many=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "photos",
            "user",
            "comments",
        )
