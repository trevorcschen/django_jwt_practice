from .models import Article, User,Token
from .serializers import ArticleSerializer, UserSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, \
permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,\
BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from django.middleware import csrf
from .utils import get_tokens_for_user, updateAccess
from django.contrib.auth import  authenticate
from django.conf import settings

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
# @authentication_classes([SessionAuthentication, BasicAuthentication])
def article_list(request):
    if request.method == "GET":
        # print(request.COOKIES)
        # print(f'ddd {request.user.is_authenticated}')
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        print(request.user)
        print(request.headers.get("Authorization").split(' ')[1])
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def login(request):
#     email = request.data.get('email', None)
#     password = request.data.get('password', None)
    
#     user = User.objects.filter(email=email).first()
    
#     if user is None:
#         raise AuthenticationFailed("User Not Found")
    
#     if not user.check_password(password):
#         raise AuthenticationFailed("User credentials incorrect")
#     serializer = MyTokenObtainPairSerializer(user)
#     # print(MyTokenObtainPairSerializer.get_token(user))
#     return Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
        

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
@api_view(["POST"])
def login(request):
    data = request.data
    response = Response()
    email = data.get('email', None)
    password = data.get('password', None)
    user = authenticate(email= email, password =password)
    if user is not None:
        if user.is_active:
            data = get_tokens_for_user(user)
            access = data.get('access')
            updateAccess(access, response)
            response.set_cookie(
                key = 'refresh_token', 
                value = data["refresh"],
                max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                            )
            # t1 = Token.objects.filter(user__email__exact=user.email)
            # if t1.exists():
            #     print('exists then update')
            # else:
            Token.objects.create(key=data['refresh'], user=user)
            csrf.get_token(request)
            response.data = {"messsage" : "Login successfully"}
            response.status = status.HTTP_200_OK
            return response
        else:
            return Response({"msg": "This account is not active!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Invalid user credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

    # return Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
@api_view(["POST"])
def set_cookieAPI(request):
    response = Response()
    # response.delete_cookie('access_token')
    access = request.data.get('access')
    print(f'here {access}')
    response.data  = {"msg": "done"}
    response.status = status.HTTP_200_OK
    updateAccess(data = access, response = response)
    return response

@api_view(["POST"])
def validate_authenticate(request):
    print('validating')
    access = request.COOKIES.get('access_token', None)
    refresh = request.COOKIES.get('refresh_token', None)
    if  refresh is None:
        return Response({"msg": "Expired token"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"msg": "authenticate"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def logout(request):
    response = Response()
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.status = status.HTTP_200_OK
    response.data = {"msg": "log out successful"}
    refresh = request.COOKIES.get('refresh_token', None)
    if refresh is not None:
        t1 = Token.objects.get(key=refresh)
        t1.delete()
    return response
    # return Response({"msg" : "log out successful"}, status=status.HTTP_200_OK)