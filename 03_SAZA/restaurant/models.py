from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model): 
    name = models.CharField(max_length=50, verbose_name='업소명')
    address = models.CharField(max_length=100, verbose_name='도로명 주소')
    dong = models.CharField(max_length=50, verbose_name='동')
    latitude = models.FloatField(verbose_name='위도', null=True)
    hardness = models.FloatField(verbose_name='경도', null=True)
    visitor_reviews = models.IntegerField(verbose_name='방문자 리뷰수')
    blog_reviews = models.IntegerField(verbose_name='블로그 리뷰수')
    total_counts = models.IntegerField(verbose_name='전체 리뷰수')
    link = models.TextField(verbose_name="URL")

class TOP_10_RES(models.Model):
    current = models.CharField(max_length=50, verbose_name='현재 위도 경도')
    list = models.CharField(max_length=10000, verbose_name='상위 10위 음식점 pk값')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}::{self.content}'

    def get_absolute_url(self):
        return f'{self.restaurant.get_absolute_url()}#review-{self.pk}'