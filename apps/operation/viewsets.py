# coding:utf-8
from django.db.models import Q

__author__ = 'Luo'

from rest_framework.filters import OrderingFilter
from common.paginations import StandardPagination
from django_filters.rest_framework import DjangoFilterBackend
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

    pagination_class = StandardPagination

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        """
        当这条收藏记录被创建时,将文章收藏数也加一
        :param serializer: 序列化对象
        :return: 
        """
        userfav = serializer.save()
        article = userfav.article
        article.star_num += 1
        article.save()

    def perform_destroy(self, instance):
        """
        当这条收藏记录被删除时,将文章收藏数也减一
        :param instance: 用户收藏
        :return: 
        """
        article = instance.article
        article.star_num -= 1
        article.save()
        instance.delete()

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

    pagination_class = StandardPagination

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        """
        当这条关注记录被创建时,用户关注数加一,对方被关注数加一
        :param serializer: 序列化对象
        :return: 
        """
        userfocus = serializer.save()
        from_user = userfocus.from_user
        to_user = userfocus.to_user
        from_user.focus += 1  # 关注人的关注数加一
        to_user.refocus += 1  # 被关注人的被关注数加一
        from_user.save()
        to_user.save()

    def perform_destroy(self, instance):
        """
        当这条关注记录被删除时,用户关注数减一,对方被关注数减一
        :param instance: 用户收藏
        :return: 
        """
        from_user = instance.from_user
        to_user = instance.to_user
        from_user.focus -= 1  # 关注人的关注数加一
        to_user.refocus -= 1  # 被关注人的被关注数加一
        from_user.save()
        to_user.save()
        instance.delete()

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

    pagination_class = StandardPagination

    # 设置排序
    filter_backends = (OrderingFilter,)

    # 排序
    ordering_fields = ('-create_time',)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        '''这个方法是为了让当前用户只能查看自己的留言'''
        queryset = UserLeavingMessage.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))
        return queryset

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

    pagination_class = StandardPagination

    # 设置排序,过滤的类
    filter_backends = (OrderingFilter, DjangoFilterBackend)

    # 排序
    ordering_fields = ('create_time',)

    # 设置过滤字段
    filter_fields = ('article_id',)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        """
        当这条收藏记录被创建时,将文章收藏数也加一
        :param serializer: 序列化对象
        :return: 
        """
        usercomment = serializer.save()
        user = usercomment.article.user
        user.integral += 5
        user.save()

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
