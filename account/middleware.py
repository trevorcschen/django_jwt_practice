from django.utils.deprecation import MiddlewareMixin
import json
from rest_framework_simplejwt.exceptions import InvalidToken
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .utils import updateAccess, get_tokens_for_user, gen_token
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from .models import Token
class TokensMiddleware(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-refresh" endpoint --- check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.token = None
        self.refresh = None

    def __call__(self, request):
        # print(request.body)
        # print(f'call here {self.token}')
        response = self.get_response(request)
        
       # if request.path not in ['/api/token/refresh'] and request.COOKIES.get('access_token',None):
        if request.path not in ['/api/token/refresh']:
            # print('access available')
            if self.token is not None:
                print('store cookie')
                updateAccess(data = self.token, response=response)
                print(f'expired {self.token}')
                self.token = None
            if self.refresh is not None:
                response.set_cookie(
                key = 'refresh_token', 
                value = self.refresh,
                max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                            )
                print(f'refresh : {self.refresh}')
                self.refresh = None
        else:
            print('None')
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        # print(f'process hgere {self.token}')
        whitelistURL = ['/admin/login/', '/api/token/refresh', '/admin/']
        # print(request.path.startswith('/admin/'))
  
        if not request.path.startswith('/admin/') and request.path not in whitelistURL and request.COOKIES.get('access_token', None):
            print('access expire probably')
            print(request.user)
            try:
                qs = jwt.decode(request.COOKIES.get('access_token', None), settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                ## generate new access code with refresh code if the old access code has been expired
                print('error')
                refresh_token = request.COOKIES.get('refresh_token', None)
                if refresh_token is not None:
                    ref_dict = {'refresh' : refresh_token}
                    try:
                        t = TokenRefreshSerializer(data = ref_dict)
                        if t.is_valid():
                            q = t.validated_data
                    except TokenError:
                        t1 = Token.objects.filter(key = refresh_token).first()
                        q = get_tokens_for_user(t1.user)
                        self.refresh = q.get('refresh')
                        t1.key = q.get('refresh')
                        t1.save()
                    raw_token = q.get('access')
                    access_dict = {'access' : raw_token}
                    request._body = json.dumps(access_dict).encode('utf-8')
                    self.token = raw_token
        elif(request.COOKIES.get('access_token', None) == None and request.COOKIES.get('refresh_token', None)
             and request.path not in whitelistURL and not request.path.startswith('/admin/')): # if access token is not present in cookie while refresh token is
            refresh_token = request.COOKIES.get('refresh_token', None)
            print('refresh here but access not')
            r , a_dict = gen_token(refresh_token)
            if r is not None:
                self.refresh = r
            self.token = a_dict.get('access', None)
            request._body = json.dumps(a_dict).encode('utf-8')
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        elif(request.path == '/logout/'):
            print('process log out')
        return None
    
    