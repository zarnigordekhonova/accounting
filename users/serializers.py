from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from .models import UserRoles, CustomUser, Branches, Roles


User = get_user_model()


class RolesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class BranchesViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branches
        fields = '__all__'


class PasswordResetRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password should be similar")
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError("User is not active")

        data.update({
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'branch': self.user.branch.name if self.user.branch else None
        })

        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'branch', 'is_active']
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'branch': {'read_only': True},
            'is_active': {'read_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'branch', 'is_active']
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True}
        }


class UserListSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField(method_name='get_company')

    def get_company(self, obj):
        return obj.branch.name if obj.branch else None

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'branch', 'is_active']


class UserRolesReadSerializer(serializers.ModelSerializer):
    roles = RolesViewSerializer(many=True)
    user = serializers.SerializerMethodField(method_name='get_user')

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }

    class Meta:
        model = UserRoles
        fields = ['id', 'user', 'roles']

class UserRolesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRoles
        fields = '__all__'
