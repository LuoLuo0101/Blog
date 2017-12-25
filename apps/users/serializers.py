# coding:utf-8
__author__ = 'Luo'

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import UserProfile



class UserRegisterSerializer(serializers.ModelSerializer):

    # UniqueValidator：注意要去官网看下那些验证的字段
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        label="用户名",
        validators=[UniqueValidator(
            queryset=UserProfile.objects.all(),
            message="用户已存在"
        )]
    )

    email = serializers.CharField(
        required=True,
        allow_blank=False,
        label="邮箱",
        validators=[UniqueValidator(
            queryset=UserProfile.objects.all(),
            message="邮箱已存在"
        )]
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        label="密码",
        write_only=True,  # 需要你填写，但是不会被序列化返回到前端
    )

    def create(self, validated_data):
        '''重写这个是为了让密码变成密文'''
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ("username", "email", "password")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("nick_name", "username", "birthday", "gender", "desc", "focus", "refocus", "integral", "image")