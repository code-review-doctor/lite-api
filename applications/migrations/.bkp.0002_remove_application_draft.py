# Generated by Django 2.1.7 on 2019-04-08 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='draft',
        ),
    ]
