# Generated by Django 2.2.16 on 2020-12-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flags", "0009_auto_20201229_1454"),
        ("routing_rules", "0002_auto_20200408_1023"),
    ]

    operations = [
        migrations.RenameField(model_name="routingrule", old_name="flags", new_name="flags_to_include",),
        migrations.AddField(
            model_name="routingrule",
            name="flags_to_exclude",
            field=models.ManyToManyField(blank=True, related_name="exclude_routing_rules", to="flags.Flag"),
        ),
    ]
