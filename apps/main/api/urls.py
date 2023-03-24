from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.main.api.v1.urls'))
]
