from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('__all__')
        read_only_fields = ('author',)


class GroupSerializer (serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    read_only_fields = ('post',)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'])
        ]

    def validate_following(self, value):
        user = self.context.get('request').user
        if value == user:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя')
        return value
