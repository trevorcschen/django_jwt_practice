from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer
from .models import Token
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    refresh = MyTokenObtainPairSerializer.get_token(user)
    return {
        'refresh' : str(refresh),
        'access': str(refresh.access_token)
    }

def updateAccess(data, response= Response()):
    response.set_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value = data,
                expires= settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                # max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                            )
def gen_token(refresh_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMjQ4Nzc0MiwianRpIjoiNTQzZTU2NTRkYzA1NDc1OGIwMTZkYzY1YzcyNDJhYzIiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImlzX3N0YWZmIjp0cnVlfQ.2kA5sw4xvPm7zsmb_KqdNtqaDQMIkwE_DfRnEIKqdrU'):
    if refresh_token is not None:
        ref_dict = {'refresh': refresh_token}
        try:
            t = TokenRefreshSerializer(data = ref_dict)
            if t.is_valid():
                q = t.validated_data
        except TokenError:
            t1 = Token.objects.filter(key= refresh_token).first()
            q = get_tokens_for_user(t1.user)
            t1.key = q.get('refresh')
            t1.save()
        raw_token = q.get('access')
        access_dict = {'access' : raw_token}
        
        return q.get('refresh'), access_dict   