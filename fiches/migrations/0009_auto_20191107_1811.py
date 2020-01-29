# Generated by Django 2.1.11 on 2019-11-07 17:11

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('fiches', '0008_fiche_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiche',
            name='contenu',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fiche',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Une liste de mots clés, séparés par des virgules.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Mots-clés'),
        ),
    ]