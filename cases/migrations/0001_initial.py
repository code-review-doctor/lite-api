# Generated by Django 2.2 on 2019-05-29 12:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case', to='applications.Application')),
            ],
        ),
        migrations.CreateModel(
            name='CaseNote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, default=None, max_length=2200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_note', to='cases.Case')),
            ],
        ),
    ]
