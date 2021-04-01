import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name = '分类'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Tag(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name = '标签'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Post(models.Model):
  title = models.CharField(max_length=70, verbose_name='标题')
  body = models.TextField(verbose_name='正文')
  created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
  modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
  excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要信息')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
  tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
  author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
  views = models.PositiveBigIntegerField(default=0, editable=False)

  # def save(self, *args, **kwargs):
  #   self.modified_time = timezone.now()
  #   super().save(*args, **kwargs)

  def increase_views(self):
    self.views += 1
    self.save(update_fields=['views'])

  class Meta:
    verbose_name = '文章'
    verbose_name_plural = verbose_name
    ordering = ['-created_time', 'title']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('blog:detail', kwargs={'pk': self.pk})

  def save(self, *args, **kwargs):
    self.modified_time = timezone.now()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    self.excerpt = strip_tags(md.convert(self.body))[:54]

    super().save(*args, **kwargs)
