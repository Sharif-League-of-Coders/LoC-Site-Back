from _helpers.models import BaseModel
from django.db import models


class Home(BaseModel):
    about_this_event = models.TextField(verbose_name='about this event')
    activate = models.BooleanField(default=True, verbose_name='activated')
    number = models.PositiveIntegerField(default=1, verbose_name='دوره', primary_key=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Home Detail'
        verbose_name_plural = 'Homes'
