from django.db import models
from django.contrib.auth.models import AbstractUser
from common.constant import Gender


class UserProfile(AbstractUser):
    '''用户扩展表'''
    nick_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="昵称")

    birthday = models.DateField(null=True, blank=True, verbose_name="生日")

    gender = models.IntegerField(
        choices=((Gender.MALE.value, "男"), (Gender.FEMALE.value, "女"), (Gender.NONE.value, "未知")),
        default=Gender.NONE.value
    )

    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name="个人描述")

    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="住址")

    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")

    integral = models.IntegerField(default=0, verbose_name="积分")

    # 设置默认头像和上传头像的路径
    image = models.ImageField(
        upload_to="image/user",
        default="image/user/default.png",
        max_length=100,
        verbose_name="个人头像"
    )

    class Meta:
        verbose_name = verbose_name_plural = "用户信息"
        db_table="userprofile"  # 重命名数据表名

    def __str__(self):
        return self.username
