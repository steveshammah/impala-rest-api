# Generated by Django 4.0 on 2021-12-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_rename_content_articles_content_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='content_2',
            field=models.TextField(null=True),
        ),
    ]
