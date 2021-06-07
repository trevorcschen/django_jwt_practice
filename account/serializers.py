from rest_framework import serializers
from .models import Article,User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author','date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password' :
                {
                    'write_only' : True,
                    'style' : {'input_type' : 'password'}
                }
        }
    def create(self,validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance    
    
class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
    
    def get_access(self,obj):
        token = RefreshToken.for_user(obj)
        token['name'] = obj.name
        token['email'] = obj.email
        token['password'] = obj.password
        token['is_staff'] = obj.is_staff
        
        return str(token.access_token)
    def get_refresh(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user): ## payload
        token = super().get_token(user)
        token['email'] = user.email
        # token['password'] = user.password
        token['is_staff'] = user.is_staff
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        print(attrs)
        data['nobody'] = 'sdasdas'
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        # serializer = UserSerializerWithToken(se)
        return data
