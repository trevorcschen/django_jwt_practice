from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework import authentication, exceptions
from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import jwt
from .utils import updateAccess
from rest_framework_simplejwt.exceptions import InvalidToken
import requests
import json
import time

def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied(f"CSRF Failed {reason}")
    
class CustomAuthentication(JWTAuthentication):
    def authenticate(self,request):
        print('q')
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        # print(raw_token)
        if raw_token is None:
            return None
        try:
            validated_token = self.get_validated_token(raw_token) 
            print('succ')
        except InvalidToken:
            print('invalid token')
            # access ='"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIyMzk4NDQ4LCJqdGkiOiIwMzk4ODJiNWY5MWU0OWRlYjdjNDZiMmEzZjA0ZjRjMyIsInVzZXJfaWQiOjEsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwiaXNfc3RhZmYiOnRydWV9.s6Ilwb_RDvXcZvIdlU3JDa4AxczkNWnUGYZBpPAatwk'
            aq = request.body.decode('utf-8')
            access  = json.loads(aq).get('access')
            # refresh = request.COOKIES.get('refresh_token', None)
            # if refresh is None:
            #     return None
            # ref_dict = {'refresh' : refresh}
            # resp = requests.post('http://127.0.0.1:8000/api/token/refresh',
            #                      headers = {'content-type' : 'application/json'},
            #                      data = json.dumps(ref_dict))
            # access  = resp.json().get('access')
            if access is None:
                return None
            raw_token = access
        validated_token = self.get_validated_token(raw_token)
        # print(f'auth here {validated_token}')
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token