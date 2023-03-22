from django.urls import path, include


urlpatterns = [
    path('', include('apps.payment.api.v1.urls'))
    ]
