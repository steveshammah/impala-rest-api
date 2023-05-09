# Generated by Django 4.0.8 on 2023-05-08 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_fixture_location_alter_fixtureresult_fixture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixture',
            name='away_team',
        ),
        migrations.RemoveField(
            model_name='fixture',
            name='home_team',
        ),
        migrations.RemoveField(
            model_name='fixtureresult',
            name='MOTM',
        ),
        migrations.RemoveField(
            model_name='fixtureresult',
            name='fixture',
        ),
        migrations.RemoveField(
            model_name='notificationmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='Partner',
        ),
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='smsmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='Fixture',
        ),
        migrations.DeleteModel(
            name='FixtureResult',
        ),
        migrations.DeleteModel(
            name='NotificationModel',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.DeleteModel(
            name='SmsModel',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
