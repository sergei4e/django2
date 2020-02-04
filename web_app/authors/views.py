from django.shortcuts import render
from userena.views import signin
from django.http import HttpResponse

from .models import Author


def author_profile_detail(request, **kwargs):
    user = Author.objects.get(user__username=kwargs.get('username'))
    context = {'user': user}
    return render(request, 'authors/base-authors.html', context)


def custom_signin(request, *args, **kwargs):
    if request.POST:
        return signin(request, *args, **kwargs)
    else:
        return HttpResponse(status=404)

