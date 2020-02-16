from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin

from userena.models import UserenaSignup
from userena.utils import get_profile_model

from news.crawlers.bbc_crawler import run
from threading import Thread


admin.site.unregister(get_user_model())
admin.site.unregister(get_profile_model())


def run_crawler_for_author(modeladmin, request, queryset):
    for object in queryset:
        if object.id == 1:
            Thread(target=run).start()


run_crawler_for_author.short_description = "Run Crawler for author"


class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1


class UserenaAdmin(UserAdmin, GuardedModelAdmin):
    inlines = [UserenaSignupInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")


class AuthorAdmin(GuardedModelAdmin):
    actions = (run_crawler_for_author, )
    list_display = (
        'id',
        'user',
        'avatar',
        'bio'
    )
    list_display_links = ('id', 'user')
    list_filter = ("user__is_active", )


admin.site.register(get_user_model(), UserenaAdmin)
admin.site.register(get_profile_model(), AuthorAdmin)
