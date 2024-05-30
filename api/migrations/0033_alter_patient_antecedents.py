# Generated by Django 5.0.4 on 2024-05-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_antecedent_alter_patient_antecedents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='antecedents',
            field=models.ManyToManyField(blank=True, related_name='antecedents', to='api.maladie'),
        ),
    ]
