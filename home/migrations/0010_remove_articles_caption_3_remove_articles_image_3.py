# Generated by Django 4.0 on 2021-12-17 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_articles_content_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='caption_3',
        ),
        migrations.RemoveField(
            model_name='articles',
            name='image_3',
        ),
    ]