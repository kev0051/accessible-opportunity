# Generated by Django 3.2 on 2023-04-12 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='disability',
            field=models.CharField(choices=[('V', 'Visual'), ('A', 'Auditory'), ('P', 'Physical'), ('C', 'Cognitive'), ('O', 'Other')], default='O', max_length=1),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=models.CharField(max_length=20000),
        ),
    ]
