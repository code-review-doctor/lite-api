# Generated by Django 3.1.7 on 2021-03-22 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("queues", "0003_auto_20201210_1649"),
        ("cases", "0047_caseassignmentsla"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=None,
            state_operations=[
                migrations.CreateModel(
                    name="CaseQueue",
                    fields=[
                        (
                            "id",
                            models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                        ),
                        ("case", models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="cases.case")),
                        ("queue", models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="queues.queue")),
                    ],
                    options={"db_table": "cases_case_queues"},
                ),
                migrations.AlterField(
                    model_name="case",
                    name="queues",
                    field=models.ManyToManyField(related_name="cases", through="cases.CaseQueue", to="queues.Queue"),
                ),
            ],
        ),
    ]
