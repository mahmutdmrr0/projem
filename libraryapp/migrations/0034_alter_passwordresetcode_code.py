# Generated by Django 5.1.5 on 2025-04-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0033_alter_userprofile_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
