from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}::{self.content}'

    def get_absolute_url(self):
        return f'{self.restaurant.get_absolute_url()}#review-{self.pk}'
