# Generated by Django 5.1.5 on 2025-04-10 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0034_alter_passwordresetcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
