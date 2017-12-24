# coding:utf-8
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer

__author__ = 'Luo'
from django.contrib.auth import get_user_model


# 导入 jwt 中的 payload
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

User = get_user_model()

class UserRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''用户'''
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 拿到User对象
        user = self.perform_create(serializer)

        # 生成payload
        payload = jwt_payload_handler(user)

        # Token.objects.create(user=instance)：很奇怪为什么不这样生成，解决，因为这个Token是原生Token，我们需要的是JWT Token
        # 生成Token
        re_dict = serializer.data
        re_dict["token"] = jwt_encode_handler(payload)
        # re_dict["name"] = user.name if user.name else user.username # 因为在Serializer中有，这里注销掉

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''重写这个方法是为了返回User对象'''
        return serializer.save()