# coding:utf-8
__author__ = 'Luo'
from blogger.models import Category, Tag, Article
from rest_framework import serializers


class CategoryLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """

    class Meta:
        model = Category
        fields = ("id", "name")


class CategoryCUDSerializer(serializers.ModelSerializer):
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
        model = Category
        fields = ("name", "user")


class TagLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """

    class Meta:
        model = Tag
        fields = ("id", "name")


class TagCUDSerializer(serializers.ModelSerializer):
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
        model = Tag
        fields = ("name", "user")


class ArticleLRSerializer(serializers.ModelSerializer):
    """
    list:
        列表
    retrieve:
        单个
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    category = CategoryLRSerializer(many=False)

    tags = TagLRSerializer(many=True)

    click_num = serializers.IntegerField(read_only=True)

    star_num = serializers.IntegerField(read_only=True)

    create_time = serializers.DateTimeField(read_only=True)

    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCUDSerializer(serializers.ModelSerializer):
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

    def validate_category(self, category):
        user = self.context["request"].user
        categorys = Category.objects.filter(user=user, id=category.id)
        if categorys:
            return category
        else:
            # 其实应该是过期被删除或者验证码发送失败
            raise serializers.ValidationError("分类不存在")

    def validate_tags(self, tags):
        user = self.context["request"].user
        tag_list = Tag.objects.filter(user=user)
        tag_ids = [tag.id for tag in tag_list]
        for tag in tags:
            if tag.id not in tag_ids:
                raise serializers.ValidationError("标签不存在")
        if tag_list:
            return tags
        else:
            # 其实应该是过期被删除或者验证码发送失败
            raise serializers.ValidationError("标签不存在")

    class Meta:
        model = Article
        fields = ("title", "content", "user", "category", "tags")
