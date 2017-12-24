from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户"

    def ready(self):
        '''导入信号'''
        import users.signals