from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from app.models import Client, Commercant, Commerce, Gerer, Produit
from app.forms import SignInForm, SignUpFormClient, SignUpFormCommercant, CommerceForm, ProduitForm, UpdateClientForm, UpdateCommercantForm


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
                request = init_panier(request)
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
            request = init_panier(request)
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
            request = init_panier(request)
            return redirect('homepage')
    else:
        form = SignUpFormCommercant(request.POST)
    return render(request, 'signup_commercant.html', {'formCommercant': form})

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
#permet de read un commerce
def read_commerce(request, idcommerce):
    gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
    return render(request, 'read/readCommerce.html', {'gerer' : gerer})

#permet de read tous les commerces d'un commercant
def read_commerce_by_commercant(request):
    listeGerer = Gerer.objects.filter(numcommercant = request.user.id)
    return render(request, 'read/readCommerceByCommercant.html', locals())


#permet de read un produit
def read_produit(request, pk):
    produit = get_object_or_404(Produit, numproduit=pk)
    return render(request, 'read/readProduit.html', {'produit' : produit})

#---------------- VIEWS DE MISES A JOUR (UPDATE) ----------------

def update_commercant(request):
    user = User.objects.get(id=request.user.id)
    commercant = Commercant.objects.get(numcommercant=request.user.id)
    if request.method == "POST":
        form = UpdateCommercantForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            commercant.telephonecommercant = form.cleaned_data.get('telephonecommercant')
            commercant.save()
            return render(request, 'index.html')#A Definir une autre redirection
    else:
        return render(request, 'update/updateCommercant.html', locals())

def update_client(request):
    user = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    if request.method == "POST":
        form = UpdateClientForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            client.datenaissanceclient = form.cleaned_data.get('datenaissanceclient')
            client.telephoneclient = form.cleaned_data.get('telephoneclient')
            client.codepostalclient = form.cleaned_data.get('codepostalclient')
            client.villeclient = form.cleaned_data.get('villeclient')
            client.rueclient = form.cleaned_data.get('rueclient')
            client.save()
            return render(request, 'index.html')#A Definir une autre redirection
    else:
        date = str(client.datenaissanceclient.year)+"-"+str(client.datenaissanceclient.month)+"-"+str(client.datenaissanceclient.day) #Permet d'avoir le bon format de date pour le input : type=date , du formulaire
        return render(request, 'update/updateClient.html', locals())

def update_commerce(request, idcommerce):
    user = User.objects.get(id=request.user.id)
    commerce = get_object_or_404(Commerce, numsiret=idcommerce)
    if request.method == "POST":
        commerce.nomcommerce = request.POST.get('nomcommerce')
        commerce.typecommerce = request.POST.get('typecommerce')
        commerce.emailcommerce = request.POST.get('emailcommerce')
        commerce.livraisoncommerce = request.POST.get('livraisoncommerce')
        commerce.telephonecommerce = request.POST.get('telephonecommerce')
        commerce.codepostalcommerce = request.POST.get('codepostalcommerce')
        commerce.villecommerce = request.POST.get('villecommerce')
        commerce.ruecommerce = request.POST.get('ruecommerce')
        #print(form.cleaned_data.get('ruecommerce'))
        commerce.save()
        return render(request, 'index.html')
    else:
        form = CommerceForm(instance=commerce)
    return render(request, 'update/updateCommerce.html', locals())

# mise a jour d'un produit

def update_produit(request, pk):
    produit = get_object_or_404(Produit, numproduit=pk)
    get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=produit.idcommerce)
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit.nomproduit = form.cleaned_data.get('nomproduit')
            produit.marqueproduit = form.cleaned_data.get('marqueproduit')
            produit.descriptifproduit = form.cleaned_data.get('descriptifproduit')
            produit.caracteristiqueproduit = form.cleaned_data.get('caracteristiqueproduit')
            produit.prixproduit = form.cleaned_data.get('prixproduit')
            produit.tauxremise = form.cleaned_data.get('tauxremise')
            produit.quantitestock = form.cleaned_data.get('quantitestock')
            produit.datelimitereservation = form.cleaned_data.get('datelimitereservation')
            produit.photoproduit1 = form.cleaned_data.get('photoproduit1')
            produit.photoproduit2 = form.cleaned_data.get('photoproduit2')
            produit.save()
            return render(request, 'index.html')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'update/updateProduit.html', {'Produitform': form})


#---------------- VIEWS DE SUPPRESSION (DELETE) ----------------

#permet de delete un commerce

def delete_commerce(request, idcommerce):
    gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
    if request.method == 'POST':
        Commerce.objects.get(numsiret = idcommerce).delete()
        return render(request, 'index.html')

    return render(request, 'delete/deleteView.html')
		
#permet de delete un produit

def delete_produit(request, pk):
    produit = get_object_or_404(Produit , numproduit=pk)
    if request.method == 'POST':
        Produit.objects.get(numproduit = pk).delete()
        return render(request, 'index.html')

    return render(request, 'delete/deleteView.html')



#--------------- SEARCH -------------------------#
def search(request, keyword=None, page=1):
	recherche = request.POST.get('recherche')
	if request.method == "POST":
		produits_all = Produit.objects.filter(nomproduit__contains=recherche)
	elif request.method == "GET":
		produits_all = Produit.objects.filter(nomproduit__contains=keyword)
		recherche=keyword
		
	paginator = Paginator(produits_all, 1) #On affiche 1 produit par page
	try:
		produits = paginator.page(page)
	except EmptyPage:
		produits = paginator.page(paginator.num_pages)
		
	return render(request, 'list/produits_recherche.html', locals())

#---------------- VIEWS DE LISTE ----------------
#permet de voir les produits d'un commerce
def produit_by_commerce(request, idcommerce):
    c = Commerce.objects.get(idcommerce = idcommerce)
    c.produit_set.all()


#---------------- VIEWS DASHBOARD ----------------

def dashboard_commercant(request):
    return render(request, 'dashboard_commercant.html')

#---------------- VIEWS PANIER ----------------

@login_required
def afficher_panier(request):
    panier_session = request.session.get('panier')
    produits = []
    for produit in panier_session:
        objet_produit = Produit.objects.get(numproduit=produit[0])
        prix_total = objet_produit.prixproduit * produit[1]

        produit = [objet_produit,produit[1],prix_total]
        produits.append(produit)

    return render(request, 'panier/panier.html', locals())

def init_panier(request):
    panier = []
    request.session['panier'] = panier #On initialise le panier dans la session
    return request

@login_required
def ajout_panier(request, idproduit):
    produit = get_object_or_404(Produit, numproduit=idproduit)

    panier_session = request.session.get('panier')
    for produit_panier in panier_session:
        if produit.numproduit == produit_panier[0]:
            produit_panier[1]=produit_panier[1]+1 #On incrèmente la quantite au panier
            request.session['panier'] = panier_session #On sauvegarde
            return afficher_panier(request)

    new_ligne_panier = [produit.numproduit,1] #new_ligne_panier = [numproduit,Quantité]
    panier_session.append(new_ligne_panier)
    request.session['panier'] = panier_session

    return afficher_panier(request)

def supprimer_panier(request, idproduit):
    panier_session = request.session.get('panier')
    for produit_panier in panier_session:
        if idproduit == produit_panier[0]:
            panier_session.remove(produit_panier)

    request.session['panier'] = panier_session  # On sauvegarde
    return afficher_panier(request)

def quantite_panier(request, idproduit):

    panier_session = request.session.get('panier')
    for produit_panier in panier_session:
        if idproduit == produit_panier[0]:
            produit_panier[1]=produit_panier[1]-1 #On modifie la quantite du produit au panier
            if produit_panier[1] == 0:
                produit_panier[1]=1
    request.session['panier'] = panier_session #On sauvegarde
    return afficher_panier(request)


def reset_panier(request):
    return init_panier(request)




#---------------- VIEWS DE A DEFINIR ----------------