from django.db import models

from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="分类名")

    user = models.ForeignKey(to=UserProfile, related_name="user_category", verbose_name="创建人")

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类表"
        db_table = "category"  # 重命名数据表名
        unique_together = ("name", "user")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(max_length=30, verbose_name="标签名")

    user = models.ForeignKey(to=UserProfile, related_name="user_tags", verbose_name="创建人")

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签表"
        db_table = "tag"  # 重命名数据表名
        unique_together = ("name", "user")

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=200, verbose_name="标题")

    content = models.TextField(max_length=100000, blank=True, verbose_name="文章内容")

    user = models.ForeignKey(to=UserProfile, related_name="user_articles", verbose_name="创建人")

    category = models.ForeignKey(to=Category, related_name="cate_articles", verbose_name="分类")

    tags = models.ManyToManyField(to=Tag, related_name="tag_article", verbose_name="标签", db_table="article_tag")

    click_num = models.IntegerField(default=0, verbose_name="浏览量")

    star_num = models.IntegerField(default=0, verbose_name="收藏数")

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "文章表"
        db_table = "article"  # 重命名数据表名

    def __str__(self):
        return self.title
