# Generated by Django 2.2.10 on 2020-02-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0002_auto_20200224_1111"),
    ]

    operations = [
        migrations.AlterField(
            model_name="party",
            name="role",
            field=models.CharField(
                choices=[
                    ("intermediate_consignee", "Intermediate Consignee"),
                    ("additional_end_user", "Additional End User"),
                    ("agent", "Agent"),
                    ("submitter", "Authorised Submitter"),
                    ("consultant", "Consultant"),
                    ("contact", "Contact"),
                    ("exporter", "Exporter"),
                    ("customer", "Customer"),
                    ("other", "Other"),
                ],
                default="other",
                help_text="Third party type only",
                max_length=22,
                null=True,
            ),
        ),
    ]
