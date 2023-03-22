from django.urls import path
from .views import PaymentCreateView

urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
]