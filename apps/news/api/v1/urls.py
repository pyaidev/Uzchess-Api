from django.urls import path

from apps.news.api.v1.views import ListNewAPIView, RetrieveNewAPIVIew

urlpatterns = [
    path('list/news/', ListNewAPIView.as_view(), name='list_news'),
    path('retrieve/news/<str:slug>', RetrieveNewAPIVIew.as_view(), name='retrieve_news')
]
