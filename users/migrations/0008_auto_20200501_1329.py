# Generated by Django 2.2.11 on 2020-05-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_govuser_default_queue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baseuser",
            name="type",
            field=models.CharField(
                choices=[("exporter", "Exporter"), ("internal", "Internal"), ("system", "System")], max_length=8
            ),
        ),
        migrations.AlterField(
            model_name="permission",
            name="type",
            field=models.CharField(
                choices=[("exporter", "Exporter"), ("internal", "Internal")], default="internal", max_length=8
            ),
        ),
        migrations.AlterField(
            model_name="role",
            name="type",
            field=models.CharField(
                choices=[("exporter", "Exporter"), ("internal", "Internal")], default="internal", max_length=8
            ),
        ),
    ]
