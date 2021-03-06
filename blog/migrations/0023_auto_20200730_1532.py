# Generated by Django 2.2.13 on 2020-07-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20200730_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='territoire',
            field=models.CharField(choices=[('0', '-----------'), ('1', 'Communauté de Communes ACVI'), ('2', 'Département'), ('3', 'Région'), ('4', 'Argelès de la Marenda'), ('5', 'Bages'), ('6', 'Banyuls de la Marenda'), ('7', 'Cervera de la Marenda'), ('8', 'Cotlliure'), ('9', 'Elna'), ('10', "La Roca d'Albera"), ('11', "Montesquiu d'Albera"), ('12', 'Ortafà'), ('13', 'Palau-del-Vidre'), ('15', 'Port-Vendres'), ('16', 'Sant-Andreu'), ('17', 'Sant Genís de Fontanes'), ('18', 'Sureda'), ('19', 'Vilallonga dels Monts')], default='0', max_length=2, verbose_name='Territoire'),
        ),
    ]
