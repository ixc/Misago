from rest_framework import serializers

from misago.categories.serializers import CategorySerializer
from misago.core.serializers import MutableFields
from misago.threads.models import Post
from misago.users.serializers import UserSerializer

from .post import PostSerializer


__all__ = [
    'FeedSerializer',
]

FeedUserSerializer = UserSerializer.subset_fields(
    'id',
    'fullname',
    'avatars',
    'url',
    'title',
    'rank',
)

FeedCategorySerializer = CategorySerializer.subset_fields('name', 'css_class', 'url')


class FeedSerializer(PostSerializer, MutableFields):
    poster = FeedUserSerializer(many=False, read_only=True)
    category = FeedCategorySerializer(many=False, read_only=True)

    thread = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + ['category', 'thread']

    def get_thread(self, obj):
        return {
            'title': obj.thread.title,
            'url': obj.thread.get_absolute_url(),
        }


FeedSerializer = FeedSerializer.exclude_fields('is_liked', 'is_new', 'is_read')
