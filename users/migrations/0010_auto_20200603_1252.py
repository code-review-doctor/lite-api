# Generated by Django 2.2.12 on 2020-06-03 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_auto_20200505_0942"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userorganisationrelationship",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="users", to="organisations.Organisation"
            ),
        ),
    ]
