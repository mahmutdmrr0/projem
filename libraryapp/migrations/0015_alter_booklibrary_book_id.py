# Generated by Django 5.1.5 on 2025-03-11 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0014_alter_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklibrary',
            name='book_id',
            field=models.CharField(max_length=150),
        ),
    ]
