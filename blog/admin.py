from django.contrib import admin
from .models import Post, Category, Tag
from django.utils.html import format_html

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  def image_tag(self, obj):
        if obj.index_img:
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.index_img.url))
        return ""
  image_tag.allow_tags = True
  image_tag.short_description = '文章封面'

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    super().save_model(request, obj, form, change)

  list_display = ['title', 'image_tag', 'created_time', 'modified_time', 'category', 'author']
  fields = ['title', 'index_img', 'body', 'excerpt', 'category', 'tags']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
