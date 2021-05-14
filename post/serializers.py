from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from post.models import Category, Tag, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)

    def validate_title(self, title):
        if self.Meta.model.objects.filter(titlte=title).exists():
            raise serializers.ValidationError('Такая категория уже существует')
        return title


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title',)

        def validate_title(self, title):
            if self.Meta.model.objects.filter(titlte=title).exists():
                raise serializers.ValidationError('Такая категория уже существует')
            return title


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = Post.objects.create(user=user, **validated_data)

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
            fields.pop('description')
            fields.pop('tags')
            fields.pop('category')
            fields.pop('posted')
        elif action == 'create':
            fields.pop('slug')
            fields.pop('user')
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category, context=self.context).data
        representation['tags'] = TagSerializer(instance.tags.all(), many=True, context=self.context).data
        # representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        # representation['likes_count'] = instance.likes.count()
        return representation


class PostListSerializer(serializers.ModelSerializer):

    details = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='slug')

    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'posted', 'price', 'details']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Укажите рейтинг от 1 до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

