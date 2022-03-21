import os

from django.db import models


class Post(models.Model):
    def upload_path(self, filename):
        return os.path.join('blog', 'posts', self.title, filename)

    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to=upload_path)
    title = models.CharField(max_length=256)
    text = models.TextField()
    brief_text = models.CharField(max_length=256, blank=True, null=True)
    author = models.ForeignKey('blog.Author', related_name='posts',
                               on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Author(models.Model):
    def upload_path(self, filename):
        return os.path.join('blog', 'writers',
                            f'{self.first_name} {self.last_name}',
                            filename)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
