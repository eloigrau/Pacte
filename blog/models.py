from django.db import models
from pacte.models import Profil, Suivis
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mass_mail
#from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save

from actstream.models import followers

class Choix():
    type_territoire = ('0', '-----------'), ('1','Communauté de Communes ACVI'), ('2','Département'),  ('3','Région'), ('4','Argelers de la Marenda'), ('5','Bages'), \
                      ('6', 'Banyuls de la Marenda'), ('7', 'Cervera de la Marenda'), ('8','Cotlliure'), ('9','Elna'), \
                ('10',"La Roca d'Albera"), ('11',"Montesquiu d'Albera"), ('12','Ortafà'),('13','Palau del Vidre'),\
                      ('15','Port Vendres'),('16','Sant Andreu'), ('17','Sant Genís de Fontanes'),\
                      ('18','Sureda'), ('19','Vilallonga dels Monts')


    type_annonce = ('0','Annonce'), ('1','Administratif'), ('2', 'Mesure / action'), ('3', 'Echanges avec les candidats'), ('4','Réunion du collectif'), ('5','Idées'), \
                ('6','Listes signataires'), ('7','Divers'), ('8','Suivi'), ('9','Conseils municipaux'),

    sousgroupesArticles = {
        "Documentation":[('2', 'Mesure / action'), ('5','Idées'), ('7','Divers'),],
        "Vie du collectif":[('0','Annonce'),('1','Administratif'), ('4','Réunions du collectif'),],
        "Suivi des communes": [('3', 'Echanges avec les candidats'), ('6','Listes signataires'), ('8','Suivi'), ('9','Conseils municipaux'),]
    }

    couleurs_annonces_old = {
        '0':"#d1ecdc",
        '1':"#D4CF7D",
        '2':"#E0E3AB",
        '3':"#AFE4C1",
        '4':"#fff2a0",
        '5':"#B2AFE4",
        '6':"#bccacf",
        '8':"#b3b6e6",
        '9':"#3EA7BB",
        '7':"#349D9B",
        '10':"#d0f4de",
    }
    couleurs_annonces = {
    '0': "#d1ecdc",
    '1': "#D4CF7D",
    '2': "#E0E3AB",
    '3': "#AFE4C1",
    '4': "#fff2a0",
    '5': "#B2AFE4",
    '6': "#cebacf",
    '7': "#caf9b7",
    '8': "#ced2d3",
    '9': "#349D9B",
    '10': "#bccacf",
    '11': "#87bfae",
    '12': "#d0f4de",
    '13': "#fffdcc",
    '14': "#daffb3",
    '15': '#ddd0a8',
    }

    def get_couleur(categorie):
        try:
            return Choix.couleurs_annonces[categorie]
        except:
            return Choix.couleurs_annonces["10"]

class Article(models.Model):
    categorie = models.CharField(max_length=30,         
        choices=(Choix.type_annonce),
        default='Annonce', verbose_name="categorie")
    territoire = models.CharField(max_length=2,
        choices=(Choix.type_territoire),
        default='', verbose_name="Territoire")
    titre = models.CharField(max_length=100,)
    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    contenu = models.TextField(null=True)
    date_creation = models.DateTimeField(verbose_name="Date de parution", default=timezone.now)
    date_modification = models.DateTimeField(verbose_name="Date de modification", default=timezone.now)
    estPublic = models.BooleanField(default=False, verbose_name='Public ou réservé aux membres du collectif ACVI')
    estModifiable = models.BooleanField(default=False, verbose_name="Modifiable par n'importe qui")

    date_dernierMessage = models.DateTimeField(verbose_name="Date du dernier message", auto_now=True)
    dernierMessage = models.CharField(max_length=100, default=None, blank=True, null=True)
    estArchive = models.BooleanField(default=False, verbose_name="Archiver l'article")

    start_time = models.DateTimeField(verbose_name="Date (optionnel, pour affichage dans l'agenda)", null=True,blank=True, help_text="jj/mm/année")
    end_time = models.DateTimeField(verbose_name="Date de fin (optionnel, pour affichage dans l'agenda)",  null=True,blank=True, help_text="jj/mm/année")

    class Meta:
        ordering = ('-date_creation', )
        
    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('blog:lireArticle', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_creation = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    @property
    def get_couleur(self):
        if self.categorie in Choix.couleurs_annonces:
            return Choix.couleurs_annonces[self.categorie]
        return Choix.couleurs_annonces["10"]

    @property
    def get_territoire(self):
        if self.territoire and self.territoire != '0' and self.territoire != '--':
            return self.get_territoire_display #[x[1] for x in Choix.type_territoire if x[0] == self.territoire][0]
        return ""

    @property
    def get_territoire_lieu(self):
        if self.territoire and self.territoire != '0' and self.territoire != '--':
            if self.territoire == '1' or self.territoire == '3' :
                return "à la " + str(self.get_territoire_display())
            elif self.territoire == '2' :
                return "au " + str(self.get_territoire_display())
            else :
                return "à " + str(self.get_territoire_display())
        return ""


@receiver(post_save, sender=Article)
def on_save_articles(instance, created, **kwargs):
    if created:
        suivi, created = Suivis.objects.get_or_create(nom_suivi='articles')
        titre = "PacteACVI - nouvel article"
        message = " Un nouvel article a été créé : https://pacteacvi.herokuapp.com" + instance.get_absolute_url() + \
                  "\n\n------------------------------------------------------------------------------" \
                  "\n vous recevez cet email, car vous avez choisi de suivre les articles (en cliquant sur la cloche) sur le site https://pacteacvi.herokuapp.com/forum/articles/"
        emails = [suiv.email for suiv in followers(suivi) if instance.auteur != suiv and (instance.estPublic or suiv.is_membre_collectif)]
        try:
            send_mass_mail([(titre, message, "pacteacvi@gmail.com", emails), ])
        except:
            pass


class Commentaire(models.Model):
    auteur_comm = models.ForeignKey(Profil, on_delete=models.CASCADE)
    commentaire = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "(" + str(self.id) + ") "+ str(self.auteur_comm) + ": " + str(self.article)

    @property
    def get_edit_url(self):
        return reverse('blog:modifierCommentaireArticle',  kwargs={'id':self.id})


@receiver(post_save,  sender=Article)
def on_save_article(instance, **kwargs):
    titre = "PacteACVI - Article actualisé"
    message = "L'article '" +  instance.titre + "' a été modifié (ou quelqu'un l'a commenté): http://pacteacvi.herokuapp.com" + instance.get_absolute_url() + \
              "\n\n------------------------------------------------------------------------------" \
              "\n vous recevez cet email, car vous avez choisi de suivre ce projet sur le site https://pacteacvi.herokuapp.com/forum/articles/"
   # emails = [(titre, message, "asso@perma.cat", (suiv.email, )) for suiv in followers(instance)]
    emails = [suiv.email for suiv in followers(instance)  if instance.auteur != suiv  and (instance.estPublic or suiv.is_membre_collectif)]
    try:
        send_mass_mail([(titre, message, "pacteacvi@gmail.com", emails), ])
    except:
        pass



class Evenement(models.Model):
    titre = models.CharField(verbose_name="Titre de l'événement (si laissé vide, ce sera le titre de l'article)",max_length=100, null=True, blank=True, default="")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, help_text="L'événement doit être associé à un article existant (sinon créez un article avec une date)" )
    start_time = models.DateTimeField(verbose_name="Date", null=False,blank=False, help_text="jj/mm/année" , default=timezone.now)
    end_time = models.DateTimeField(verbose_name="Date de fin (optionnel pour un evenement sur plusieurs jours)",  null=True,blank=True, help_text="jj/mm/année")

    class Meta:
        unique_together = ('article', 'start_time',)

    def get_absolute_url(self):
        return self.article.get_absolute_url()


    @property
    def gettitre(self):
        if not self.titre:
            return self.article.titre
        return self.titre

    @property
    def estPublic(self):
        return self.article.estPublic
