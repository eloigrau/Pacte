# Generated by Django 2.2.9 on 2020-01-30 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacte', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='code_postal',
            field=models.CharField(blank=True, default='66000', max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='profil',
            name='commune',
            field=models.CharField(blank=True, default='Perpignan', max_length=50, null=True),
        ),
    ]
