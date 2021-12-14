# Generated by Django 4.0 on 2021-12-14 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_articles_options_rename_story_articles_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='image_url',
        ),
        migrations.AddField(
            model_name='articles',
            name='image_1',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='articles',
            name='image_2',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
