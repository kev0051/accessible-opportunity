# Generated by Django 3.2 on 2023-03-26 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_poster',
            field=models.BooleanField(default=False),
        ),
    ]
