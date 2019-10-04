# Generated by Django 2.2.4 on 2019-09-26 15:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
        ('flags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, default=None, max_length=280, null=True)),
                ('is_good_controlled', models.BooleanField(blank=True, default=None, null=True)),
                ('control_code', models.TextField(blank=True, default=None, null=True)),
                ('is_good_end_product', models.BooleanField(blank=True, default=None, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_application', to='applications.OpenApplication')),
                ('flags', models.ManyToManyField(related_name='goods_type', to='flags.Flag')),
            ],
        ),
    ]
