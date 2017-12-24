# coding:utf-8
__author__ = 'Luo'
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer

from django.contrib.auth import get_user_model

# 导入 jwt 中的 payload
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

User = get_user_model()


class UserRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''用户注册'''
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 拿到User对象
        user = self.perform_create(serializer)

        # 生成payload
        payload = jwt_payload_handler(user)

        # 生成 JWT
        re_dict = serializer.data
        re_dict["token"] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''重写这个方法是为了返回User对象'''
        return serializer.save()
