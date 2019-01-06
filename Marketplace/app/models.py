from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

BOOLEAN_CHOICES = (
    (True,'Oui'),
    (False,'Non'),
)

#Entitée héritant des Users définit par Django
class Commercant(models.Model):
    numcommercant = models.OneToOneField(User, on_delete=models.CASCADE)
    telephonecommercant = models.CharField(max_length=15)
    class Meta:
        db_table = 'commercant'

class Client(models.Model):
    numclient = models.OneToOneField(User, on_delete=models.CASCADE)
    datenaissanceclient = models.DateField()
    pointsclient = models.IntegerField(default='0')
    telephoneclient = models.CharField(blank=True, max_length=15)
    codepostalclient = models.IntegerField(blank=False)
    villeclient = models.CharField(blank=False, max_length=30)
    rueclient = models.CharField(blank=False, max_length=30)
    class Meta:
        db_table = 'client'

#Autres entités
class Commerce(models.Model):
    numsiret = models.BigIntegerField(primary_key=True, help_text="Renseignez votre numèro de siret, 14 chiffres succesifs")
    nomcommerce = models.CharField(max_length=30)
    typecommerce = models.CharField(max_length=30)
    emailcommerce = models.EmailField()
    livraisondisponible = models.BooleanField(choices=BOOLEAN_CHOICES)
    joursretrait = models.IntegerField(blank=False, null=True)  # Correspond à un nombre de jour
    telephonecommerce = models.CharField(max_length=15)
    codepostalcommerce = models.IntegerField()
    villecommerce = models.CharField(max_length=30)
    ruecommerce = models.CharField(max_length=30)
    gpslatitude = models.FloatField(blank=False, null=True)
    gpslongitude = models.FloatField(blank=False, null=True)
    class Meta:
        db_table = 'commerce'

class Categorie(models.Model):
    numcategorie = models.AutoField(primary_key=True)
    nomcategorie = models.CharField(max_length=30)
    class Meta:
        db_table = 'categorie'


class Produit(models.Model):
    numproduit = models.AutoField(primary_key=True)
    idcommerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, db_column='idcommerce')
    numcategorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, db_column='numcategorie')
    nomproduit = models.CharField(max_length=30)
    marqueproduit = models.CharField(max_length=30)
    descriptifproduit = models.TextField(max_length=400)
    caracteristiquesproduit = models.TextField(max_length=400)
    prixproduit = models.FloatField(max_length=30)
    tauxremise = models.FloatField(max_length=5)
    quantitestock = models.IntegerField(default='0')
    quantitedisponible = models.IntegerField() #Lors de la création d'un produit le nb de produit disponible est egal au nb de produit en stock
    photoproduit1 = models.ImageField(upload_to = 'media/', blank=False, null=True)
    photoproduit2 = models.ImageField(upload_to = 'media/', blank=True, null=True)
    class Meta:
        db_table = 'produit'

class Commande(models.Model):
    numcommande = models.AutoField(primary_key=True)
    numclient = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='numclient')
    numcommerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, db_column='numcommerce')
    montantcommande = models.FloatField(max_length=30)
    datecommande = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date de la commande")
    class Meta:
        db_table = 'commande'


class Reservation(models.Model):
    numreservation = models.AutoField(primary_key=True)
    numclient = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='numclient')
    numcommerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, db_column='numcommerce')
    montantreservation = models.FloatField(max_length=30)
    datereservation = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date de la réservation")
    datelimitereservation = models.DateField(blank=False, null=True, verbose_name="Date limite de la réservation")
    paiementrealise = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)
    class Meta:
        db_table = 'reservation'

class Reduction(models.Model):
    REDUCTION_CHOICES = (
        ('pourcentage','Taux de réduction en %'),
        ('bon',"Bon d'achat en euros"),
    )
    codereduction = models.AutoField(primary_key=True)
    numclient = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='numclient')
    numcommerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, db_column='numcommerce')
    typereduction = models.CharField(max_length=15,choices=REDUCTION_CHOICES)
    valeurreduction = models.FloatField(max_length=10)
    estutilise = models.BooleanField(choices=BOOLEAN_CHOICES)
    class Meta:
        db_table = 'reduction'

class Concerner(models.Model):
    numproduit = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='numproduit')
    numcategorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, db_column='numcategorie')
    class Meta:
        db_table = 'concerner'
        unique_together = ('numproduit','numcategorie')

class Commenter(models.Model):
    numproduit = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='numproduit')
    numclient = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='numclient')
    commentaire = models.TextField(max_length=300)
    note = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    datecommentaire = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Date du commentaire")
    class Meta:
        db_table = 'commenter'
        unique_together = ('numproduit','numclient')

class Appartenir(models.Model):
    numproduit = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='numproduit')
    numcommande = models.ForeignKey(Commande, on_delete=models.CASCADE, db_column='numcommande')
    quantitecommande = models.IntegerField()
    livraisondemande = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    class Meta:
        db_table = 'appartenir'
        unique_together = ('numproduit','numcommande')

class Reserver(models.Model):
    numproduit = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='numproduit')
    numreservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, db_column='numreservation')
    quantitereserve = models.IntegerField()
    class Meta:
        db_table = 'reserver'
        unique_together = ('numproduit','numreservation')

class Gerer(models.Model):
    numcommercant = models.ForeignKey(Commercant, on_delete=models.CASCADE, db_column='numcommercant')
    numcommerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, db_column='numcommerce')
    class Meta:
        db_table = 'gerer'
        unique_together = ('numcommercant','numcommerce')