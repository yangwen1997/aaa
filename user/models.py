from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('S', '保密'),
    )
    nickname = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    plt_icon = models.CharField(max_length=256, blank=True)  # 第三方平台用户的头像
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)
    perm_id = models.IntegerField()

    @property
    def avatar(self):
        return self.icon.url if self.icon else self.plt_icon

    @property
    def perm(self):
        '''用户对应的权限'''
        if not hasattr(self, '_perm'):
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm

    def has_perm(self, perm_name):
        '''检查用户是否具有某个权限'''
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level


class Permission(models.Model):
    name = models.CharField(max_length=16, unique=True)
    level = models.IntegerField()
