# coding:utf-8
__author__ = 'Luo'

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
    一个 post_save 的信号捕捉
    :param sender: 发送者
    :param instance: 数据的实例
    :param created: 是否是新建
    :param kwargs: 其他参数
    :return: 返回值
    '''
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()