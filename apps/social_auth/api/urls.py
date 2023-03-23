from django.urls import path, include


urlpatterns = [
    path('v1/', include('apps.social_auth.api.v1.urls'))
]