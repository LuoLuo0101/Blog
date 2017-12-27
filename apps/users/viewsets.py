# coding:utf-8
__author__ = 'Luo'

from common.permissions import IsOwnerOrReadOnly
from users.models import UserProfile
from rest_framework import status, viewsets, permissions
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer, UserSerializer

# 导入 jwt 中的 payload
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


class UserRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''用户注册'''
    serializer_class = UserRegisterSerializer
    queryset = UserProfile.objects.all()

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


class UserViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    '''用户详情'''
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return UserSerializer   # 到时候这个要修改
        else:
            return UserSerializer

    def get_permissions(self):
        '''
        用于动态设置权限 替代 permission_classes
        :return: 返回权限
        '''
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            # 必须返回一个用户的实例
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        else:
            return []