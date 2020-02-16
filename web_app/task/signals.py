
def my_callback(sender, **kwargs):
    from .tasks import run_bbc

    if kwargs.get('created'):
        instance = kwargs.get('instance')

        if instance.task_name == 'run_bbc':
            run_bbc.delay(instance.pk)
