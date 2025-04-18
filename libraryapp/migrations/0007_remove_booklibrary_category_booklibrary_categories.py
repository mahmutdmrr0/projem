# Generated by Django 5.1.5 on 2025-03-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0006_book_related_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booklibrary',
            name='category',
        ),
        migrations.AddField(
            model_name='booklibrary',
            name='categories',
            field=models.ManyToManyField(blank=True, to='libraryapp.category'),
        ),
    ]
