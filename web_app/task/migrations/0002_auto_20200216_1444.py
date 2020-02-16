# Generated by Django 3.0.2 on 2020-02-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(choices=[('run_bbc', 'Run BBC Crawler'), ('run_nt', 'Run NT Crawler'), ('run_cnn', 'Run CNN Crawler')], max_length=255),
        ),
    ]
