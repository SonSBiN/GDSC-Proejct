# Generated by Django 4.0.6 on 2022-07-09 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_top_10_res_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='top_10_res',
            name='list',
            field=models.CharField(max_length=10000, verbose_name='상위 10위 음식점 pk값'),
        ),
    ]