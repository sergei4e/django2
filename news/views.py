from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Category


def index_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:3].prefetch_related('categories')
    context = {
        'last_articles': last_articles,
    }
    return render(request, 'news/index.html', context)


def blog_handler(request, **kwargs):
    cat_slug = kwargs.get('cat_slug')
    page = int(kwargs.get('number', 1))
    count = 2
    if cat_slug:
        category = Category.objects.get(slug=cat_slug)
        last_articles = Article.objects.filter(
            categories__slug=cat_slug).order_by(
            '-pub_date')[(page-1)*count:page*count].prefetch_related('categories')
        art_count = Article.objects.filter(
            categories__slug=cat_slug).count()
        max_page = (art_count // count) + 1
    else:
        art_count = Article.objects.all().count()
        max_page = (art_count // count) + 1
        last_articles = Article.objects.all().order_by(
            '-pub_date')[(page-1)*count:page*count].prefetch_related('categories')
        category = None
    context = {
        'last_articles': last_articles,
        'category': category,
        'pages': range(2, max_page+1),
        'corrent_page': page,
        'max_page': max_page
    }
    return render(request, 'news/blog.html', context)


def page_handler(request, post_slug):
    main_article = Article.objects.get(slug=post_slug)
    try:
        prev_article = Article.objects.get(id=main_article.id-1)
    except ObjectDoesNotExist:
        prev_article = None
    try:
        next_article = Article.objects.get(id=main_article.id+1)
    except ObjectDoesNotExist:
        next_article = None
    context = {
        'article': main_article,
        'prev_article': prev_article,
        'next_article': next_article
    }
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
