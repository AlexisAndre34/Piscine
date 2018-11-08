from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Commerce, Produit, Categorie

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
    choice_categorie = CategorieChoiceField(queryset=Categorie.objects.all(), to_field_name='numcategorie')
    class Meta:
        model = Produit
        exclude = [ 'idcommerce','numcategorie','numproduit','quantitedisponible']


class CommerceForm(forms.ModelForm):
    class Meta:
        model = Commerce
        fields = '__all__'

#Formulaire de creation d'un compte client
class SignUpFormClient(UserCreationForm):
    datenaissanceclient = forms.DateField()
    telephoneclient = forms.CharField()
    codepostalclient = forms.IntegerField()
    villeclient = forms.CharField()
    rueclient = forms.CharField()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','datenaissanceclient','email','telephoneclient','codepostalclient','villeclient','rueclient','password1', 'password2', )

#Formulaire de creation de compte commercant
class SignUpFormCommercant(UserCreationForm):
    telephonecommercant = forms.CharField()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','telephonecommercant', 'password1', 'password2', )

#-----Formulaire de mise à jour ---