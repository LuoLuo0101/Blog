# coding:utf-8
__author__ = 'Luo'
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from blogger.models import Tag, Category, Article
from blogger.serializers import TagCUDSerializer, TagLRSerializer, CategoryCUDSerializer, CategoryLRSerializer, \
    ArticleCUDSerializer, ArticleLRSerializer
from rest_framework import viewsets, status, permissions


class CategoryViewSet(viewsets.ModelViewSet):
    '''分类'''

    queryset = Category.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return CategoryCUDSerializer
        else:  # self.action == "list" or self.action == "retrieve":
            return CategoryLRSerializer

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


class TagViewSet(viewsets.ModelViewSet):
    '''标签'''

    queryset = Tag.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return TagCUDSerializer
        else:  # self.action == "list" or self.action == "retrieve":
            return TagLRSerializer

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


class ArticleViewSet(viewsets.ModelViewSet):
    """文章"""
    queryset = Article.objects.all().order_by("-create_time")

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return ArticleCUDSerializer
        else:  # self.action == "list" or self.action == "retrieve":
            return ArticleLRSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
