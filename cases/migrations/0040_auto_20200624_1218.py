# Generated by Django 2.2.13 on 2020-06-24 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0039_auto_20200618_1318"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casetype",
            name="reference",
            field=models.CharField(
                choices=[
                    ("oiel", "Open Individual Export Licence"),
                    ("ogel", "Open General Export Licence"),
                    ("oicl", "Open Individual Trade Control Licence"),
                    ("siel", "Standard Individual Export Licence"),
                    ("sicl", "Standard Individual Trade Control Licence"),
                    ("sitl", "Standard Individual Transhipment Licence"),
                    ("f680", "MOD F680 Clearance"),
                    ("exhc", "MOD Exhibition Clearance"),
                    ("gift", "MOD Gifting Clearance"),
                    ("cre", "HMRC Query"),
                    ("gqy", "Goods Query"),
                    ("eua", "End User Advisory Query"),
                    ("ogtcl", "Open General Trade Control Licence"),
                    ("ogtl", "Open General Transhipment Licence"),
                    ("comp_c", "Compliance Site Case"),
                    ("comp_v", "Compliance Visit Case"),
                ],
                max_length=6,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="casetype",
            name="sub_type",
            field=models.CharField(
                choices=[
                    ("standard", "Standard Licence"),
                    ("open", "Open Licence"),
                    ("hmrc", "HMRC Query"),
                    ("end_user_advisory", "End User Advisory Query"),
                    ("goods", "Goods Query"),
                    ("exhibition_clearance", "MOD Exhibition Clearance"),
                    ("gifting_clearance", "MOD Gifting Clearance"),
                    ("f680_clearance", "MOD F680 Clearance"),
                    ("compliance_site", "Compliance Site Case"),
                    ("compliance_visit", "Compliance Visit Case"),
                ],
                max_length=35,
            ),
        ),
    ]
