from django.urls import path, include, re_path
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from . import views
sitemaps = {
    'post': PostSitemap,
}
app_name = 'blog'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('post/<int:pk>/', views.detail, name='detail'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path("archives/", views.PostArchivesView.as_view(), name="archives"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("about/<int:pk>/", views.AboutDetailView.as_view(), name="about"),
    # path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archives/<int:year>/<int:month>/',views.ArchiveView.as_view(), name='archive'),
    # path('categories/<int:pk>/', views.category, name='category'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    # path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search'),
    re_path(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}),
    re_path(r'^robots\.txt', include('robots.urls')),
]
