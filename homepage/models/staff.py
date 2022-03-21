from django.db import models

from _helpers.models import BaseModel


class Staff(BaseModel):
    name = models.CharField(max_length=120, verbose_name='name')
    position = models.CharField(max_length=220, verbose_name='position')
    image = models.ImageField(verbose_name='pic')
    email = models.EmailField(verbose_name='email')
    show_in_homepage = models.BooleanField(default=False, verbose_name='show in homepage')

    class Meta:
        unique_together = ('name', 'email')
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'
