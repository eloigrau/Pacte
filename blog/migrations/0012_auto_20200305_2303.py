# Generated by Django 2.2.9 on 2020-03-05 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200217_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='estPublic',
            field=models.BooleanField(default=False, verbose_name='Public ou réservé aux membres du collectif ACVI'),
        ),
    ]