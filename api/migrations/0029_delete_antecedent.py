# Generated by Django 5.0.4 on 2024-05-28 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_remove_maladie_membre_antecedent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Antecedent',
        ),
    ]