from django.shortcuts import render


def blog_hendler(request):
    context = {}
    return render(request, 'news/blog.html', context)


def page_hendler(request):
    context = {}
    return render(request, 'news/page.html', context)


def contact_hendler(request):
    context = {}
    return render(request, 'news/contact.html', context)


def about_hendler(request):
    context = {}
    return render(request, 'news/about.html', context)


def index_hendler(request):
    context = {}
    return render(request, 'news/index.html', context)


def search_hendler(request):
    context = {}
    return render(request, 'news/search.html', context)


def robots_hendler(request):
    context = {}
    return render(request, 'news/robots.txt', context,
                  content_type='text/plain')
