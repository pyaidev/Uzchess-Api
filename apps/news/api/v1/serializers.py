from rest_framework.serializers import ModelSerializer

from apps.news.models import NewArticle


class ListNewModelSerializer(ModelSerializer):
    class Meta:
        model = NewArticle
        fields = (
            'id', 'title', 'image',
            'slug', 'created', 'description'
        )


class DetailNewModelSerializer(ModelSerializer):
    class Meta:
        model = NewArticle
        fields = (
            'id', 'title', 'image',
            'created', 'description',
            'view'
        )
