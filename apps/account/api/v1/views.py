import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.account.models import Account
from config import settings
from .permissions import IsOwnUserOrReadOnly
from .serializers import RegisterSerializer, LoginSerializer, UserImageUpdateSerializer, AccountSerializer, \
    EmailVerificationSerializer
from .utils import Util


class AccountRegisterAPIView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/register/
    serializer_class = RegisterSerializer

    # user create
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = Account.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        print(absurl)
        email_body = absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = Account.objects.get(id=payload['user_id'])
            if not user.email_is_verified:
                user.email_is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class AccountListAPIView(generics.ListAPIView):
    # http://127.0.0.1:8000/account/login/profiles/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)
    pagination_class = None


class MyAccountAPIView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/account/login/{phone_number}/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)
    lookup_field = 'phone_number'


class AccountOwnImageUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/image-update/<id>/
    serializer_class = UserImageUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated, IsOwnUserOrReadOnly)

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.get_serializer(query)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'query does not match'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)
