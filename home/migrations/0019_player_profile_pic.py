# Generated by Django 4.0.8 on 2022-12-08 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_tag_alter_product_options_alter_team_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/'),
        ),
    ]
