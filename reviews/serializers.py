from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment, Rating, Favorite


class CommentSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'article', 'created_at', 'text']
        read_only_fields = ['user', 'created_at']
    
    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']
        
    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)
    
    def validate(self, attrs):
        user = self.context.get('request').user
        article = attrs.get('article')
        rate = Rating.objects.filter(user=user, article=article)
        if rate.exists():
            raise serializers.ValidationError('Rate already exists')
        return attrs

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']
        
        
    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)
    
    def validate(self, attrs):
        user = self.context.get('request').user
        article = attrs.get('article')
        favorite = Favorite.objects.filter(user=user, article=article)
        if favorite.exists():
            raise serializers.ValidationError('Rate already exists')
        return super().validate(attrs)