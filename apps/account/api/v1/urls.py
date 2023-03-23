from django.urls import path

from .views import AccountRegisterAPIView, AccountListAPIView, MyAccountAPIView, LoginAPIView, \
    AccountOwnImageUpdateView, VerifyEmail

urlpatterns = [
    path('register/', AccountRegisterAPIView.as_view()),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('login/', LoginAPIView.as_view()),
    path('profiles/', AccountListAPIView.as_view()),
    path('profile/<str:phone_number>/', MyAccountAPIView.as_view()),
    path('image-update/<int:pk>/', AccountOwnImageUpdateView.as_view()),
]

