# Generated by Django 4.0 on 2021-12-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_articles_image_url_articles_image_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='caption_1',
            field=models.CharField(default='Impala Rugby', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='caption_2',
            field=models.CharField(default='Impala Rugby', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='caption_3',
            field=models.CharField(default='Impala Rugby', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='image_3',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='articles',
            name='tags',
            field=models.TextField(default='Impala', max_length=150, null=True),
        ),
    ]
