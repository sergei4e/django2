from django.db.models import Count

from .models import Category, Tag


def menu_categories(request):
    cat_list = Category.objects.annotate(
        count=Count('article__id')).order_by('-count')[:5]

    return {'menu_categories': cat_list}


def tags_linking(request):
    tags_list = Tag.objects.order_by('?')[:10]
    return {'tags_list': tags_list}