# Generated by Django 2.2.9 on 2020-01-24 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0008_exhibition_clearance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goodonapplication",
            name="application",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="goods", to="applications.BaseApplication"
            ),
        ),
    ]
