# Generated by Django 2.2.9 on 2020-01-30 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200130_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categorie',
            field=models.CharField(choices=[('0', 'Annonce'), ('1', 'Administratif'), ('2', 'Agenda'), ('3', 'Mesure du Pacte'), ('Autre', 'Autre')], default='Annonce', max_length=30, verbose_name='categorie'),
        ),
    ]
