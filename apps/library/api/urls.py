from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.library.api.v1.urls'))
]
