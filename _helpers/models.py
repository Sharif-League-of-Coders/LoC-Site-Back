from datetime import datetime

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created = models.DateTimeField(auto_created=True, default=datetime.now(), verbose_name='created')

    class Meta:
        abstract = True
