# Generated by Django 3.0.6 on 2020-05-26 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qmeet', '0004_auto_20200525_1233'),
    ]

    operations = [
        migrations.RunSQL('''
            CREATE SCHEMA Music;            
        ''')
    ]
