from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from accounts.models import Role, UserRole

User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
        )
    nickname = serializers.CharField(required=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'roles']

    def get_roles(self, obj):
        # 해당 유저가 가진 역할 목록을 반환 (UserRole 중계 테이블을 통해)
        user_roles = UserRole.objects.filter(user=obj)
        
        # 역할이 있을 경우 직렬화된 데이터 반환, 없을 경우 빈 리스트 반환
        if user_roles.exists():
            return RoleSerializer([user_role.role for user_role in user_roles], many=True).data
        return []  # 역할이 없으면 빈 리스트 반환

    def create(self, validated_data):
        # 사용자 생성
        user = User.objects.create_user(**validated_data)
        
        # 'USER' 역할 가져오기 (없으면 생성)
        user_role, created = Role.objects.get_or_create(role='USER')
        
        # UserRole 중계 테이블에 사용자와 역할 추가
        UserRole.objects.create(user=user, role=user_role)

        return user