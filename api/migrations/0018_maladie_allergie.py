# Generated by Django 5.0.4 on 2024-05-27 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_documentmedicale_type_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='maladie',
            name='allergie',
            field=models.BooleanField(default=False),
        ),
    ]