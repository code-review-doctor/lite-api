# Generated by Django 2.2.16 on 2021-01-11 04:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('external_data', '0001_initial'),
        ('applications', '0043_baseapplication_foi_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='DenialMatchOnApplication',
            fields=[
                ('created_at', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created_at')),
                ('updated_at', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='updated_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.TextField(choices=[('partial', 'Partial'), ('exact', 'Exact')])),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denial_matches', to='applications.BaseApplication')),
                ('denial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denials_on_application', to='external_data.Denial')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
