from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.news.api.v1.serializers import ListNewModelSerializer, DetailNewModelSerializer
from apps.news.models import NewArticle, NewArticleView


class ListNewAPIView(ListAPIView):
    queryset = NewArticle.objects.all().order_by('-created_at')
    serializer_class = ListNewModelSerializer
    permission_classes = (IsAuthenticated,)


class RetrieveNewAPIVIew(RetrieveAPIView):
    queryset = NewArticle.objects.all()
    serializer_class = DetailNewModelSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.META.get('HTTP_USER_AGENT', ''))
        queryset = super().get_queryset()
        new = get_object_or_404(queryset, slug=self.kwargs["slug"])
        if self.request.user.is_authenticated:
            new_view, created = NewArticleView.objects.update_or_create(
                new=new,
                user=self.request.user,
            )
            if created:
                new.view += 1
                new.save()
        elif self.request.META.get('HTTP_USER_AGENT', ''):
            device_id = self.request.META.get('HTTP_USER_AGENT', '')
            blog_view, created = NewArticleView.objects.update_or_create(
                new=new,
                device_id=device_id,
            )
            if created:
                new.view += 1
                new.save()

        return queryset
