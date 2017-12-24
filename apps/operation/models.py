from django.db import models

from blogger.models import Article
from users.models import UserProfile


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(UserProfile, related_name="user_fav", verbose_name="用户")

    article = models.ForeignKey(Article, related_name="article_fav", verbose_name="文章")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = verbose_name = '用户收藏'
        unique_together = ("user", "article")

    def __str__(self):
        return self.article.title


class UserFocus(models.Model):
    """
    用户关注
    """
    from_user = models.ForeignKey(UserProfile, related_name="from_focus", verbose_name="关注人")

    to_user = models.ForeignKey(UserProfile, related_name="to_focus", verbose_name="被关注人")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="关注时间")

    class Meta:
        verbose_name_plural = verbose_name = '用户关注'
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return self.to_user.username


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    from_user = models.ForeignKey(UserProfile, related_name="from_message", verbose_name="发出人")

    to_user = models.ForeignKey(UserProfile, related_name="to_message", verbose_name="接收人")

    message = models.CharField(max_length=100, verbose_name="留言")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="留言时间")

    class Meta:
        verbose_name_plural = verbose_name = "用户留言"

    def __str__(self):
        return self.message


class UserComment(models.Model):
    """
    用户评论
    """
    user = models.ForeignKey(UserProfile, related_name="user_comment", verbose_name="用户")

    article = models.ForeignKey(Article, related_name="article_comment", verbose_name="文章")

    comment = models.CharField(max_length=100, verbose_name="评论")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    class Meta:
        verbose_name_plural = verbose_name = '用户评论'

    def __str__(self):
        return self.comment
