import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'jwt_backends.settings')

import django 
django.setup()

from datetime import timedelta
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions as drf_exceptions

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenObtainSerializer,
    TokenObtainSlidingSerializer, TokenRefreshSerializer,
    TokenRefreshSlidingSerializer, TokenVerifySerializer,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken, OutstandingToken,
)
from rest_framework_simplejwt.tokens import (
    AccessToken, RefreshToken, SlidingToken,
)
from rest_framework_simplejwt.utils import (
    aware_utcnow, datetime_from_epoch, datetime_to_epoch,
)
from django.conf import settings
refresh = RefreshToken()
# refresh = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMjM4OTMzNiwianRpIjoiNWYyOWMyZmZhMzU4NGY4OWEzYWI1MGMzNDM1NTJiZjMiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImlzX3N0YWZmIjp0cnVlfQ.l3agGIeDYI_an6CTxJPvvE9oj08yo9_CsQQPHPAZRto'
s = TokenVerifySerializer(data = {'token' : str(refresh)})
print(s.is_valid())
# try:
#     s = TokenRefreshSerializer(data = {'refresh' : str(refresh)})
#     s.is_valid()
# except TokenError:
#     print('s')

# print(len('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIyMzk2NjMwLCJqdGkiOiIwN2Y5MDM5MDUxZjY0ODkyOWRhNDhiMzVhOGMwMTgyOSIsInVzZXJfaWQiOjEsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwiaXNfc3RhZmYiOnRydWV9.-cbEYEDBqqBLkG9V9KS952b2PHggsgdytMIpnL0uN-I'))

import jwt
from jwt.exceptions import ExpiredSignatureError

try:
    q =jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIyNDU2NzUxLCJqdGkiOiJkMmE5ODlmZjU0Yzg0ODEzOGVjMDZiYTY4NWRiZDNmOCIsInVzZXJfaWQiOjEsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwiaXNfc3RhZmYiOnRydWV9.93Y7caG-Fa_6CQRuo_gNbX-3s1G6l7BdcD-2HM9wuMs', settings.SECRET_KEY, algorithms=['HS256'])
    print(q)
except ExpiredSignatureError:
    print('q')