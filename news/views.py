from django.shortcuts import render
from django.db.models import Count

from .models import Article, Category


def index_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:3].prefetch_related('categories')

    cat_list = Category.objects.annotate(
        count=Count('article__id')).order_by('count')[:5]

    context = {
        'last_articles': last_articles,
        'menu_categories': cat_list
    }
    return render(request, 'news/index.html', context)


def blog_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:10].prefetch_related('categories')
    context = {'last_articles': last_articles}
    return render(request, 'news/blog.html', context)


def category_handler(request, cat_slug):
    context = {}
    return render(request, 'news/blog.html', context)


def page_handler(request, post_slug):
    context = {}
    return render(request, 'news/page.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'news/contact.html', context)


def about_handler(request):
    context = {}
    return render(request, 'news/about.html', context)


def search_handler(request):
    context = {}
    return render(request, 'news/search.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context,
                  content_type='text/plain')
