# Generated by Django 3.0.6 on 2020-05-21 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0009_remove_studentprofile_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=50),
        ),
    ]
