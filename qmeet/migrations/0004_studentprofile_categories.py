# Generated by Django 2.2.7 on 2020-05-11 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0003_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='categories',
            field=models.ManyToManyField(through='qmeet.StudentCategories', to='qmeet.Categories'),
        ),
    ]
