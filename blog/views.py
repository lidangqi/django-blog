import markdown
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag, About
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q, Count
from braces.views import SetHeadlineMixin

# Create your views here.

# def index(request):
#   post_list = Post.objects.all().order_by('-created_time')
#   return render(request, 'blog/index.html', context={
#     'title': '我的博客首页',
#     'welcome': '欢迎访问我的博客首页',
#     'post_list': post_list,
#   })


class IndexView(PaginationMixin, ListView):
  model = Post
  template_name = 'blog/index.html'
  context_object_name = 'post_list'
  paginate_by = 10

# def detail(request, pk):
#   post = get_object_or_404(Post, pk=pk)

#   post.increase_views()
  
#   md = markdown.Markdown(extensions=[
#     'markdown.extensions.extra',
#     'markdown.extensions.codehilite',
#     'markdown.extensions.toc',
#   ])
#   post.body = md.convert(post.body)

#   m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#   post.toc = m.group(1) if m is not None else ''

#   return render(request, 'blog/detail.html', context={'post': post})

class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/detail.html'
  context_object_name = 'post'

  def get(self, request, *args, **kwargs):
    response = super(PostDetailView, self).get(request, *args, **kwargs)
    self.object.increase_views()
    return response
  
  # def get_object(self, queryset=None):
  #   post = super().get_object(queryset=None)
  #   md = markdown.Markdown(extensions=[
  #       'markdown.extensions.extra',
  #       'markdown.extensions.codehilite',
  #       TocExtension(slugify=slugify),
  #   ])
    
  #   post.body = md.convert(post.body)
  #   m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
  #   post.toc = m.group(1) if m is not None else ''

  #   return post

# def archive(request, year, month):
#   post_list = Post.objects.filter(created_time__year=year, 
#       created_time__month=month).order_by('created_time')

#   return render(request, 'blog/index.html', context={'post_list': post_list})

class ArchiveView(IndexView):
  def get_queryset(self):
    year = self.kwargs.get('year')
    month = self.kwargs.get('month')
    return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)
  

class PostArchivesView(SetHeadlineMixin, ListView):
    headline = "归档"
    model = Post
    template_name = "blog/archives.html"

# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
  def get_queryset(self):
    cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    return super(CategoryView, self).get_queryset().filter(category=cate)


class CategoryListView(SetHeadlineMixin, ListView):
    model = Category
    headline = "分类"
    template_name = "blog/category.html"
    queryset = Category.objects.all().annotate(num_posts=Count("post"))

# def tag(request, pk):
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
class TagView(IndexView):
  def get_queryset(self):
    t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
    return super(TagView, self).get_queryset().filter(tags=t)


class TagListView(SetHeadlineMixin, ListView):
    model = Tag
    headline = "标签"
    template_name = "blog/tags.html"


class AboutDetailView(DetailView):
    model = About
    headline = "关于"
    template_name = "blog/about.html"
    context_object_name = 'about'

    def get(self, request, *args, **kwargs):
      response = super(AboutDetailView, self).get(request, *args, **kwargs)
      return response

def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR,
                             error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})
