# Generated by Django 4.1.5 on 2023-01-28 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='work',
            name='success',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='result',
            field=models.IntegerField(null=True),
        ),
    ]
