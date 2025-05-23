# Generated by Django 5.1.5 on 2025-04-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0044_alter_book_google_books_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_url',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Kapak URL'),
        ),
        migrations.AlterField(
            model_name='book',
            name='google_books_id',
            field=models.CharField(max_length=100, unique=True, verbose_name='Google Kitap ID'),
        ),
        migrations.AlterField(
            model_name='book',
            name='info_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Bilgi Linki'),
        ),
        migrations.AlterField(
            model_name='book',
            name='preview_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Önizleme Linki'),
        ),
    ]
