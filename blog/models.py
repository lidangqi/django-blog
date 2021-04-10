from mdeditor.fields import MDTextField
from django.shortcuts import render
import markdown, re
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.utils.functional import cached_property

# Create your models here.
class Category(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name = '分类'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Tag(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)

  class Meta:
    verbose_name = '标签'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.admonition",
            TocExtension(slugify=slugify),
        ],
    )
    content = md.convert(value)
    n = content.count('<div class="codehilite">', 0, len(content))
    for i in range(n):
        content = re.sub(r'<div class="codehilite">',
                    '<div class="codehilite" id="code{}">'
                    '<button id="ecodecopy" style="float: right;z-index:10" class="copybtn" '
                    'data-clipboard-action="copy" '
                    'data-clipboard-target="#code{}"> \
                    <i class="iconfont icon-copy"></i><span>复制</span> \
                    </button>'
                    .format(i, i), content, 1)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div> ', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}

class About(models.Model):
  name = models.CharField(max_length=100)
  id = models.AutoField(primary_key=True)
  avatar_img = models.ImageField(upload_to='images/', blank=True, verbose_name='关于我头像')
  body = MDTextField(verbose_name='正文')

  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name = '关于'
    verbose_name_plural = verbose_name

class Post(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=70, verbose_name='标题')
  body = MDTextField(verbose_name='正文')
  created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
  modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
  excerpt = models.CharField(max_length=400, blank=True, verbose_name='摘要信息')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
  tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
  author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
  views = models.PositiveBigIntegerField(default=0, editable=False)
  index_img = models.ImageField(upload_to='images/', blank=True, verbose_name='文章封面')
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
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.admonition",
        TocExtension(slugify=slugify),
    ])
    self.excerpt = strip_tags(md.convert(self.body))[:54]

    super().save(*args, **kwargs)

  @property
  def toc(self):
    return self.rich_content.get("toc", "")

  @property
  def body_html(self):
    return self.rich_content.get("content", "")

  @cached_property
  def rich_content(self):
    return generate_rich_content(self.body)
