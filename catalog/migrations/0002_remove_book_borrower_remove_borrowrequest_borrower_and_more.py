# Generated by Django 4.2.4 on 2023-08-23 21:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='borrower',
        ),
        migrations.RemoveField(
            model_name='borrowrequest',
            name='borrower',
        ),
        migrations.AddField(
            model_name='book',
            name='borrower',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrowrequest',
            name='borrower',
            field=models.ManyToManyField(help_text='User who wants to borrow a book', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
