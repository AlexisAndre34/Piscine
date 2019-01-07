from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Commerce, Produit, Categorie, Commenter, Reduction
import datetime

#Formulaire pour la connexion au site
class SignInForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


#-----Formulaire de creation ---

#formulaire de creation de produit, choix des categories
class CategorieChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nomcategorie

#formulaire de creation de produit
class ProduitForm(forms.ModelForm):
    choice_categorie = CategorieChoiceField(queryset=Categorie.objects.all(), to_field_name='numcategorie', label="Categorie")
    class Meta:
        model = Produit
        exclude = [ 'idcommerce','numcategorie','numproduit','quantitedisponible']
        labels = {"nomproduit": "Nom du produit",
                  "marqueproduit": "Marque",
                  "descriptifproduit": "Descriptif",
                  "caracteristiquesproduit": "Caractéristiques",
                  "prixproduit": "Prix (en euros)",
                  "tauxremise": "Remise (en %)",
                  "quantitestock": "Quantité (en stock)",
                  "photoproduit1": "Photo n°1",
                  "photoproduit2": "Photo n°2"}

class CommerceForm(forms.ModelForm):
    class Meta:
        model = Commerce
        fields = '__all__'
        labels = {"numsiret": "Numéro de Siret",
                  "nomcommerce":"Nom du commerce",
                  "typecommerce": "Type de commerce",
                  "emailcommerce": "Adresse éléctonique",
                  "livraisondisponible": "Je souhaite réaliser des livraisons à mes clients",
                  "joursretrait": "Nombre de jours maximum pour retirer une réservation",
                  "telephonecommerce": "Téléphone",
                  "codepostalcommerce":"Code postal",
                  "villecommerce": "Ville",
                  "ruecommerce": "Rue",
                  "gpslatitude": "Latitude",
                  "gpslongitude": "Longitude",
                  "horairescommerce": "Horaires d'ouverture"}

#Formulaire de creation de commentaire
class CommentaireForm(forms.ModelForm):
  class Meta:
    model = Commenter
    exclude = ['id','numproduit','numclient','datecommentaire']

#Formulaire de creation de reduction
class ReductionForm(forms.ModelForm):
    class Meta:
        model = Reduction
        fields = ('typereduction',)
        labels = {"typereduction": "Type de réduction"}
        
#Formulaire de creation d'un compte client
class SignUpFormClient(UserCreationForm):
    datenaissanceclient = forms.DateField(label="Date de naissance",widget = forms.SelectDateWidget(years=range(1900, 2100)))
    telephoneclient = forms.CharField(label="Numéro de téléphone")
    codepostalclient = forms.IntegerField(label="Code postal")
    villeclient = forms.CharField(label="Ville")
    rueclient = forms.CharField(label="Rue")
    class Meta:
        model = User
        fields = ('username','first_name','last_name','datenaissanceclient','email','telephoneclient','codepostalclient','villeclient','rueclient','password1', 'password2', )

#Formulaire de creation de compte commercant
class SignUpFormCommercant(UserCreationForm):
    telephonecommercant = forms.CharField(label="Numéro de téléphone")
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','telephonecommercant', 'password1', 'password2', )

#-----Formulaire de mise à jour ---

class UpdateCommercantForm(forms.Form):
    first_name = forms.CharField(label = "Prénom")
    last_name = forms.CharField(label = "Nom")
    email = forms.EmailField(label="Adresse éléctonique")
    telephonecommercant = forms.CharField(label ="Téléphone")

class UpdateClientForm(forms.Form):
    first_name = forms.CharField(label = "Prénom")
    last_name = forms.CharField(label = "Nom")
    email = forms.EmailField(label = "Adresse éléctonique")
    datenaissanceclient = forms.DateField(label="Date de naissance")
    telephoneclient = forms.CharField(label="Téléphone")
    codepostalclient = forms.IntegerField(label="Code Postal")
    villeclient = forms.CharField(label="Ville")
    rueclient = forms.CharField(label="Rue")