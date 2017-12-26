# coding:utf-8
__author__ = 'Luo'
from common.paginations import StandardPagination
from rest_framework.filters import OrderingFilter
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
    queryset = Article.objects.all()

    # 设置排序
    filter_backends = (OrderingFilter, )

    # 排序
    ordering_fields = ('-create_time', "click_num", "star_num")

    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            return ArticleCUDSerializer
        else:  # self.action == "list" or self.action == "retrieve":
            return ArticleLRSerializer

    def perform_create(self, serializer):
        """
        发表一篇博客,用户加20积分
        :param serializer: 序列化对象
        :return: 
        """
        article = serializer.save()
        user = article.user
        user.integral += 20
        user.save()

    def retrieve(self, request, *args, **kwargs):
        """
        文章被查看一次,浏览量加1,用户积分加1
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 返回这篇博客
        """
        instance = self.get_object()
        user = instance.user
        user.integral += 20
        instance.click_num += 1
        user.save()
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
