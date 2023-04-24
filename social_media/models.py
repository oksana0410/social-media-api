import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Hashtag(models.Model):
    tag = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.tag


def content_picture_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "content_pictures/",
        f"{slugify(instance.title)}-{uuid.uuid4()}{extension}",
    )


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    photos = models.ImageField(blank=True, null=True, upload_to=content_picture_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    hashtag = models.ManyToManyField(Hashtag, related_name="posts")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.comment
