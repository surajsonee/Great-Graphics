from django.db import models
from django.contrib.auth.models import User


class Testimonial(models.Model):
    """testimonial form"""
    stars = models.TextField(max_length=10, default='', null=False, blank=False)
    text = models.TextField(max_length=200, default='', null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author
