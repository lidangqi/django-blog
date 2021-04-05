# Generated by Django 3.1.7 on 2021-04-05 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210404_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='index_img',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='文章封面'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=400, verbose_name='摘要信息'),
        ),
    ]
