# Generated by Django 2.2.7 on 2020-04-07 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='test',
            field=models.CharField(default=2, max_length=300),
            preserve_default=False,
        ),
    ]
