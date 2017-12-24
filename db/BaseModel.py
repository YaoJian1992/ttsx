from django.db import models


class BaseModel(models.Model):

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间(auto_now系统自动给我们记录时间)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 逻辑删除
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True  # 告诉django本类作为抽象基类
