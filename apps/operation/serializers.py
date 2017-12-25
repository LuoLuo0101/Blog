# coding:utf-8
__author__ = 'Luo'

from operation.models import UserFav, UserFocus, UserLeavingMessage, UserComment
from blogger.serializers import ArticleLRSerializer
from rest_framework import serializers


class UserFavLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """
    article = ArticleLRSerializer(many=False)

    class Meta:
        model = UserFav
        fields = ("id", "article", "create_time")


class UserFavCUDSerializer(serializers.ModelSerializer):
    """
    create:
        创建
    update:
        更新
    destroy:
        删除
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserFav
        fields = ("user", "article")


class UserFocusLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """

    class Meta:
        model = UserFocus
        fields = ("id", "to_user", "create_time")


class UserFocusCUDSerializer(serializers.ModelSerializer):
    """
    create:
        创建
    update:
        更新
    destroy:
        删除
    """
    from_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserFocus
        fields = ("from_user", "to_user")


class UserLeavingMessageLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """

    class Meta:
        model = UserLeavingMessage
        fields = ("id", "to_user", "message", "create_time")


class UserLeavingMessageCUDSerializer(serializers.ModelSerializer):
    """
    create:
        创建
    update:
        更新
    destroy:
        删除
    """
    from_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserLeavingMessage
        fields = ("from_user", "to_user", "message")


class UserCommentLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """
    # article = ArticleLRSerializer(many=False)

    class Meta:
        model = UserComment
        fields = ("id", "user", "article", "comment", "create_time")


class UserCommentCUDSerializer(serializers.ModelSerializer):
    """
    create:
        创建
    update:
        更新
    destroy:
        删除
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserComment
        fields = ("user", "article", "comment")

