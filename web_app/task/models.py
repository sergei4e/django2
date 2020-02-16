from django.db import models


CHOISES = (
    ('run_bbc', 'Run BBC Crawler'),
    ('run_nt', 'Run NT Crawler'),
    ('run_cnn', 'Run CNN Crawler'),
)


class Task(models.Model):
    task_name = models.CharField(max_length=255, choices=CHOISES)
    started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
