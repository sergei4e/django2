# Generated by Django 3.0.2 on 2020-02-08 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_auto_20200208_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='articles',
        ),
    ]