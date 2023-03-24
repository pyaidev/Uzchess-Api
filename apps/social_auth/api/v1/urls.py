from django.urls import path
from apps.social_auth.api.v1.views import GoogleLogin

urlpatterns = [
    path('socilal-auth/', GoogleLogin.as_view(), name='social_login')

]