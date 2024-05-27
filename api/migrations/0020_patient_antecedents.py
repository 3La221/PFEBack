# Generated by Django 5.0.4 on 2024-05-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_documentmedicale_ordonance'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='antecedents',
            field=models.ManyToManyField(blank=True, related_name='antecedents', to='api.maladie'),
        ),
    ]