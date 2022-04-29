from django.db import models

from _helpers.models import BaseModel


class Sponsor(BaseModel):
    name = models.CharField(max_length=330, verbose_name='name')
    logo = models.ImageField(verbose_name='logo')
    website_address = models.URLField(verbose_name='url')
    activated_for_this_event = models.BooleanField(verbose_name='activated', default=True)

    class Meta:
        unique_together = ('website_address', 'name')
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'
