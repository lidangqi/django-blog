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
from functools import wraps
import pymdownx.superfences
from pymdownx.superfences import SuperFencesBlockPreprocessor, highlight_validator

# Create your models here.

def _highlight_validator(language, options):
    filename = options.pop("filename", "")
    okay = highlight_validator(language, options)
    if filename != "":
        options["filename"] = filename
    return okay


def _highlight(method):
    @wraps(method)
    def wrapper(self, src, language, options, md, classes=None, id_value="", **kwargs):
        filename = options.get("filename", "")
        code = method(
            self,
            src,
            language,
            options,
            md,
            classes=classes,
            id_value=id_value,
            **kwargs
        )
        if filename == "":
            return code
        return '<div class="literal-block"><div class="code-block-caption">{}</div>{}</div>'.format(
            filename, code
        )

    return wrapper

# Monkey patch pymdownx.superfences for code block caption purpose
pymdownx.superfences.highlight_validator = _highlight_validator

SuperFencesBlockPreprocessor.highlight = _highlight(
    SuperFencesBlockPreprocessor.highlight
)

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

def generate_rich_content(value, *, toc_depth=2, toc_url=""):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.admonition",
            "markdown.extensions.nl2br",
            TocExtension(slugify=slugify, toc_depth=toc_depth),
            # "pymdownx.extra",
            # "pymdownx.magiclink",
            # "pymdownx.tasklist",
            # "pymdownx.tilde",
            # "pymdownx.caret",
            # "pymdownx.superfences",
            # "pymdownx.tabbed",
            # "pymdownx.highlight",
            # "pymdownx.inlinehilite",
        ],
        # extension_configs = {"pymdownx.highlight": {"linenums_style": "pymdownx-inline"}},
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}

class Post(models.Model):
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
        "markdown.extensions.admonition",
        "markdown.extensions.nl2br",
        TocExtension(slugify=slugify,),
        "pymdownx.extra",
        "pymdownx.magiclink",
        "pymdownx.tasklist",
        "pymdownx.tilde",
        "pymdownx.caret",
        "pymdownx.superfences",
        "pymdownx.tabbed",
        "pymdownx.highlight",
        "pymdownx.inlinehilite",
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
