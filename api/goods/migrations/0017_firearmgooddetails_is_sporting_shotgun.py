# Generated by Django 2.2.16 on 2020-11-26 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0016_auto_20201123_0332"),
    ]

    operations = [
        migrations.AddField(
            model_name="firearmgooddetails", name="is_sporting_shotgun", field=models.BooleanField(null=True),
        ),
    ]
