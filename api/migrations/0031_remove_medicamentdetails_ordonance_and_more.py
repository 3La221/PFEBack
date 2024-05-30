# Generated by Django 5.0.4 on 2024-05-30 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_centre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicamentdetails',
            name='ordonance',
        ),
        migrations.RemoveField(
            model_name='medicamentdetails',
            name='isChronic',
        ),
        migrations.AddField(
            model_name='medicamentdetails',
            name='consultation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medicaments', to='api.consultation'),
        ),
        migrations.DeleteModel(
            name='Ordonance',
        ),
    ]