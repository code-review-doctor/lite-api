# Generated by Django 2.2.10 on 2020-02-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0005_case_copy_of"),
    ]

    operations = [
        migrations.AddField(model_name="case", name="last_closed_at", field=models.DateTimeField(null=True),),
        migrations.AddField(model_name="case", name="sla_days", field=models.PositiveSmallIntegerField(default=0),),
        migrations.AddField(model_name="case", name="sla_remaining_days", field=models.SmallIntegerField(null=True),),
        migrations.AddField(model_name="case", name="sla_updated_at", field=models.DateTimeField(null=True),),
    ]
