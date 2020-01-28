"""super_news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from news import views


urlpatterns = [
    path('', views.index_handler, name='homepage'),

    path('blog/', views.blog_handler, name='blog'),
    path('category/<cat_slug>', views.blog_handler, name='category'),

    path('post/<post_slug>', views.page_handler, name='article'),

    path('about/', views.about_handler, name='about'),
    path('contact/', views.contact_handler, name='contact'),
    path('search/', views.search_handler, name='search'),

    path('robots.txt', views.robots_handler),

    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
