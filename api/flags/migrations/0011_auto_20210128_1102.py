# Generated by Django 2.2.17 on 2021-01-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flags", "0010_flaggingrule_excluded_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flag",
            name="level",
            field=models.CharField(
                choices=[
                    ("Case", "Case"),
                    ("Organisation", "Organisation"),
                    ("Good", "Good"),
                    ("Destination", "Destination"),
                    ("PartyOnApplication", "PartyOnApplication"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="flaggingrule",
            name="level",
            field=models.CharField(
                choices=[
                    ("Case", "Case"),
                    ("Organisation", "Organisation"),
                    ("Good", "Good"),
                    ("Destination", "Destination"),
                    ("PartyOnApplication", "PartyOnApplication"),
                ],
                max_length=20,
            ),
        ),
    ]
