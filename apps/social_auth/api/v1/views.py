from allauth.account.adapter import get_adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer


class CustomSocialLoginView(LoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter