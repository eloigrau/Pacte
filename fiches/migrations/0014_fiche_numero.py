# Generated by Django 2.1.11 on 2019-11-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiches', '0013_fiche_objectif'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiche',
            name='numero',
            field=models.PositiveIntegerField(default=1),
        ),
    ]