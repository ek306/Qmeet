# Generated by Django 3.0.6 on 2020-05-25 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='display_picture',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
