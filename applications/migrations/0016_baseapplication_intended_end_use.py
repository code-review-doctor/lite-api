# Generated by Django 2.2.11 on 2020-03-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0015_licence"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseapplication",
            name="intended_end_use",
            field=models.TextField(blank=True, default=None, max_length=2200, null=True),
        ),
    ]
