from django.urls import path

from .views import AccountRegisterAPIView, AccountListAPIView, MyAccountAPIView, LoginAPIView, \
    AccountOwnImageUpdateView, VerifyEmail, RequestPasswordResetEmail, SetNewPasswordAPIView

urlpatterns = [
    path('register/', AccountRegisterAPIView.as_view()),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    # path('request-reset-email/', RequestPasswordResetEmail.as_view(),
    #      name="request-reset-email"),
    # path('password-reset/<uidb64>/<token>/',
    #      PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('password-reset-complete', SetNewPasswordAPIView.as_view(),
    #      name='password-reset-complete'),
    path('login/', LoginAPIView.as_view()),
    path('profiles/', AccountListAPIView.as_view()),
    path('profile/<str:phone>/', MyAccountAPIView.as_view()),
    path('image-update/<int:pk>/', AccountOwnImageUpdateView.as_view()),
]

