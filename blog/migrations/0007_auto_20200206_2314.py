# Generated by Django 2.2.9 on 2020-02-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200206_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categorie',
            field=models.CharField(choices=[('0', 'Annonce'), ('1', 'Administratif'), ('2', 'Mesure du Pacte'), ('3', 'Echanges avec les candidats'), ('4', 'Réunion'), ('5', 'Covoiturage'), ('6', 'Diverss')], default='Annonce', max_length=30, verbose_name='categorie'),
        ),
    ]
