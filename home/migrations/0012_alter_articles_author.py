# Generated by Django 4.0 on 2022-02-06 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_articles_tags_author_alter_articles_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.author'),
        ),
    ]