from rest_framework.decorators import api_view, permission_classes
from accounts.serializers import (
    SignupSerializer
)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

@extend_schema(
        tags=["Accounts"],
        description="Accounts 생성을 위한 API",
        request=SignupSerializer,
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        response_serializer = SignupSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
        tags=["Accounts"],
        description="Login을 위한 API",
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': '빈칸이 있습니다. 모두 입력해주세요.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': '해당 유저가 없습니다.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response({'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)