# Generated by Django 3.0.6 on 2020-05-25 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0003_remove_studentprofile_display_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedCategories',
            fields=[
                ('categories', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
    ]
