from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from app.models import Client, Commercant, Commerce, Gerer, Produit
from app.forms import SignInForm, SignUpFormClient, SignUpFormCommercant, CommerceForm, ProduitForm

#VIEW PAGE D'ACCUEIL
def homepage(request):
    return render(request, 'index.html')


#---------------- VIEWS DE CONNEXION, DECONNEXION  ----------------


def login_user(request):
    error=False
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password"]
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request,user)
                return redirect('homepage')
            else:
                error=True
                #ErrorMessage = "Username ou mot de passe incorrect"
    else:
        form= SignInForm()
    return render(request, 'signin.html', locals())


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


#---------------- VIEWS DE CREATION (CREATE) ----------------

#Creation d'un compte client
def signup_client(request):
    if request.method == 'POST':
        form = SignUpFormClient(request.POST)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur de base
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #Authentification de l'utilisateur
            Utilisateur = User.objects.get(username=username)
            groupe_client = Group.objects.get(id='2')  # On ajoute l'utilisateur au groupe client ici (id groupe client = 2 )
            Utilisateur.groups.add(groupe_client)
            client = Client(numclient=Utilisateur, datenaissanceclient=form.cleaned_data.get('datenaissanceclient'), telephoneclient=form.cleaned_data.get('telephoneclient'), codepostalclient=form.cleaned_data.get('codepostalclient'), villeclient=form.cleaned_data.get('villeclient'), rueclient=form.cleaned_data.get('rueclient'), numclient_id=Utilisateur.id)
            client.save()  # Sauvegarde du client
            login(request, user) #Connexion au site
            return redirect('homepage')
    else:
        form = SignUpFormClient(request.POST)
    return render(request, 'signup_client.html', {'formClient': form})

#Creation d'un compte commercant
def signup_commercant(request):
    if request.method == 'POST':
        form = SignUpFormCommercant(request.POST)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #Authentification de l'utilisateur
            Utilisateur = User.objects.get(username=username)
            groupe_commercant = Group.objects.get(id='1')  # On ajoute l'utilisateur au groupe commercant ici (id groupe commercant = 1 )
            Utilisateur.groups.add(groupe_commercant)
            commercant = Commercant(numcommercant=Utilisateur, telephonecommercant=form.cleaned_data.get('telephonecommercant'), numcommercant_id=Utilisateur.id)
            commercant.save()  # Sauvegarde du commercant
            login(request, user) #Connexion au site
            return redirect('homepage')
    else:
        form = SignUpFormCommercant(request.POST)
    return render(request, 'signup_Commercant.html', {'formCommercant': form})

#Creation d'un commerce
def create_commerce(request):
    if request.method == 'POST':
        form = CommerceForm(request.POST)
        if form.is_valid():
            commerce = form.save()
            commercant = Commercant.objects.get(numcommercant = request.user.id)
            new_gestion = Gerer(numcommercant = commercant, numcommerce = commerce)
            new_gestion.save()
            return render(request, 'index.html')
    else:
        form = CommerceForm(request.POST)
    return render(request, 'create/createCommerce.html', {'formCommerce': form})

def create_produit(request, idcommerce):
    #Si c'est une requete en POST
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        #On verifie que les donnees sont valides
        if form.is_valid():
            qtestock = form.cleaned_data.get('quantitestock')
            commerce = Commerce.objects.get(numsiret=idcommerce)
            new_produit = Produit(idcommerce=commerce, numcategorie=form.cleaned_data.get('choice_categorie'), nomproduit=form.cleaned_data.get('nomproduit'), marqueproduit=form.cleaned_data.get('marqueproduit'), descriptifproduit=form.cleaned_data.get('descriptifproduit'), caracteristiquesproduit=form.cleaned_data.get('caracteristiquesproduit'), prixproduit=form.cleaned_data.get('prixproduit'), tauxremise=form.cleaned_data.get('tauxremise'), quantitestock=form.cleaned_data.get('quantitestock'), quantitedisponible=qtestock, datelimitereservation=form.cleaned_data.get('datelimitereservation'), photoproduit1=form.cleaned_data.get('photoproduit1'), photoproduit2=form.cleaned_data.get('photoproduit2'))
            new_produit.save()
            return render(request, 'index.html')
    #Si c'est une requete GET ou autre chose
    else:
        form = ProduitForm()
    return render(request, 'create/createProduit.html', {'formProduit': form})


#---------------- VIEWS DE LECTURE (READ) ----------------

def read_commerce(request, idcommerce):
    gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
    return render(request, 'read/readCommerce.html', {'gerer' : gerer})





#---------------- VIEWS DE MISES A JOUR (UPDATE) ----------------




#---------------- VIEWS DE SUPPRESSION (DELETE) ----------------





#---------------- VIEWS DE A DEFINIR ----------------