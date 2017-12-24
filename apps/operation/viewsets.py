# coding:utf-8
__author__ = 'Luo'

from operation.models import UserFav, UserFocus, UserLeavingMessage, UserComment
from operation.serializers import UserFavLRSerializer, UserFavCUDSerializer, UserFocusLRSerializer, \
    UserFocusCUDSerializer, UserLeavingMessageCUDSerializer, UserLeavingMessageLRSerializer, UserCommentLRSerializer, \
    UserCommentCUDSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions


class UserFavViewSet(viewsets.ModelViewSet):
    '''用户收藏'''

    queryset = UserFav.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return UserFavCUDSerializer
        else:
            return UserFavLRSerializer

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


class UserFocusViewSet(viewsets.ModelViewSet):
    '''用户关注'''

    queryset = UserFocus.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return UserFocusCUDSerializer
        else:
            return UserFocusLRSerializer

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


class UserLeavingMessageViewSet(viewsets.ModelViewSet):
    '''用户留言'''

    queryset = UserLeavingMessage.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return UserLeavingMessageCUDSerializer
        else:
            return UserLeavingMessageLRSerializer

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


class UserCommentViewSet(viewsets.ModelViewSet):
    '''用户评论'''

    queryset = UserComment.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return UserCommentCUDSerializer
        else:
            return UserCommentLRSerializer

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
