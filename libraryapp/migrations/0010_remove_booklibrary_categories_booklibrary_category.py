# Generated by Django 5.1.5 on 2025-03-10 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0009_remove_booklibrary_category_booklibrary_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booklibrary',
            name='categories',
        ),
        migrations.AddField(
            model_name='booklibrary',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='libraryapp.category'),
        ),
    ]
