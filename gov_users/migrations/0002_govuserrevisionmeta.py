# Generated by Django 2.2 on 2019-06-12 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0001_squashed_0004_auto_20160611_1202'),
        ('gov_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GovUserRevisionMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gov_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gov_users.GovUser')),
                ('revision', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reversion.Revision')),
            ],
        ),
    ]
