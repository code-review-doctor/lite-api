# Generated by Django 2.2.4 on 2019-11-05 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20191001_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='control_code',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='good',
            name='part_number',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='good',
            name='description',
            field=models.TextField(default='', max_length=280),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='good',
            name='is_good_end_product',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='good',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.Organisation'),
        ),
    ]
