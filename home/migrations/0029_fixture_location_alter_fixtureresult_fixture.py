# Generated by Django 4.0.8 on 2023-02-02 07:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_remove_fixtureresult_fixture_results_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='fixtureresult',
            name='fixture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associated_fixture', to='home.fixture'),
        ),
    ]
