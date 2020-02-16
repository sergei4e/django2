# Create your tasks here
from __future__ import absolute_import, unicode_literals

from time import sleep
from celery import shared_task


@shared_task
def run_bbc(task_pk=None):
    from news.crawlers.bbc_crawler import run
    from .models import Task

    if task_pk:
        sleep(3)
        task = Task.objects.get(pk=task_pk)
        run(task)

    else:
        run()
