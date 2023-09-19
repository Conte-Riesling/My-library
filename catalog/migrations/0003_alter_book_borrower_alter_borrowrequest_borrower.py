# Generated by Django 4.2.4 on 2023-08-23 21:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_remove_book_borrower_remove_borrowrequest_borrower_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='borrower',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='borrower',
            field=models.ManyToManyField(help_text='User who wants to borrow a book', to=settings.AUTH_USER_MODEL),
        ),
    ]
