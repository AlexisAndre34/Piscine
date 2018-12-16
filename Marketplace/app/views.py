from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from app.models import Client, Commercant, Commerce, Gerer, Produit, Commande, Reservation, Appartenir
from app.forms import SignInForm, SignUpFormClient, SignUpFormCommercant, CommerceForm, ProduitForm, UpdateClientForm, UpdateCommercantForm


#VIEW PAGE D'ACCUEIL
def homepage(request):
    return render(request, 'accueil.html')


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
                request = init_reservation(request) #On initiliase le panier et le panier_reservation de l'utilisateur
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
            request = init_reservation(request) #On initiliase le panier et le panier_reservation de l'utilisateur
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
            request = init_reservation(request) #On initiliase le panier et le panier_reservation de l'utilisateur
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
    commerce = get_object_or_404(Commerce,  numsiret=idcommerce)
    estGerant = not (not Gerer.objects.filter(numcommercant=request.user.id, numcommerce=idcommerce))
    return render(request, 'read/readCommerce.html', locals())

#permet de read tous les commerces d'un commercant
def read_commerce_by_commercant(request):
    listeGerer = Gerer.objects.filter(numcommercant = request.user.id)
    return render(request, 'read/readCommerceByCommercant.html', locals())


#permet de read un produit
def read_produit(request, pk):
    produit = get_object_or_404(Produit, numproduit=pk)
    return render(request, 'read/readProduit.html', {'produit' : produit})

#permet de read un Client
def read_moncompte(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    return render(request, 'read/moncompte.html', locals())

#permet de read un commande
def read_commande(request, idcommande):
    commande = Commande.objects.get(numcommande=idcommande)
    appartenir = Appartenir.objects.filter(numcommande=commande)
    return render(request, 'read/readCommande.html', locals())

#permet de read les commandes d'un Client
def read_mescommandesClient(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    commandes = Commande.objects.filter(numclient=client)
    return render(request, 'read/mescommandesClient.html', locals())

#permet de read les réservations d'un Client
def read_mesreservationsClient(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    reservations = Reservation.objects.filter(numclient=request.user.id)
    return render(request, 'read/mesreservationsClient.html', locals())

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
        commerce.save()
        gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
        return render(request, 'read/readCommerce.html', {'gerer': gerer})
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
		produits_all = Produit.objects.filter(nomproduit__icontains=recherche)
	elif request.method == "GET":
		produits_all = Produit.objects.filter(nomproduit__icontains=keyword)
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
    prix_panier = float()
    for produit in panier_session:
        objet_produit = Produit.objects.get(numproduit=produit[0])
        prix_total = objet_produit.prixproduit * produit[1]
        prix_total = round(prix_total, 2)
        prix_panier = prix_panier + prix_total

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

def trierCommandes(request):
    # LigneCommande = [] #LigneCommande = [Commerce1, [ [Ligne_produit1], [Ligne_produit2], ... ] ]
    CommandesEnCours = []  # CommandesEnCours = [ [LigneCommande1], [LigneCommande2], ... ]
    panier_session = request.session.get('panier')

    for ligne_produit in panier_session:
        objet_produit = Produit.objects.get(numproduit=ligne_produit[0])
        i = 0  # // i de 0 à len(CommandeEnCours)-1
        while i < (len(CommandesEnCours) - 1) and CommandesEnCours[i][0].numsiret != objet_produit.idcommerce:  # Tant que on a pas parcourur tout la liste et qu'on a pas trouvé un commerce correspondant (Sortie du while si 1 des 2 est réalisé)
            i = i + 1

        ligne_produit[0] = objet_produit  # On remplace l'id produit par un objet de type produit pour le recuperer dans la template

        # On doit tester notre sortie de while
        if not CommandesEnCours:  # Si notre liste est vide
            LigneCommande = [objet_produit.idcommerce]  # Si on trouve un commerce correspondant à notre produit, alors on ajoute la nouvelle ligne produit à la suite de la ligne de commande déjà existante
            LigneCommande.append([]) #On insère une liste vide qui accueillera toutes les lignes produit
            LigneCommande[1].append(ligne_produit)
            CommandesEnCours.append(LigneCommande)
        else:
            if CommandesEnCours[i][0].numsiret == objet_produit.idcommerce.numsiret:  # Si on a trouvé un commerce qui correspond au produit
                CommandesEnCours[i][1].append(ligne_produit)
            elif i == (len(CommandesEnCours) - 1):  # Sinon
                LigneCommande = [objet_produit.idcommerce]  # Création d'une nouvelle ligne commande avec en tête le commerce
                LigneCommande.append([])
                LigneCommande[1].append(ligne_produit)  # A la suite du commerce on ajoute la ligne_produit (Produit,Quantite) de notre panier
                CommandesEnCours.append(LigneCommande)  # On ajoute cette nouvelle ligne de commande à notre liste de commande à traiter

    return CommandesEnCours

def verification_commande(request):
    #LigneCommande = [] #LigneCommande = [Commerce1,[Ligne_produit1], [Ligne_produit2], ... ]
    CommandesEnCours = [] #CommandesEnCours = [ [LigneCommande1], [LigneCommande2], ... ]
    Erreurs = []
    prix_total = float()
    error_qte = False
    panier_session = request.session.get('panier')


    for ligne_produit in panier_session:
        objet_produit = Produit.objects.get(numproduit=ligne_produit[0])
        prix_total = prix_total + round((objet_produit.prixproduit * ligne_produit[1]),2)
        i = 0 #// i de 0 à len(CommandeEnCours)-1
        while i < (len(CommandesEnCours)-1) and CommandesEnCours[i][0].numsiret != objet_produit.idcommerce : #Tant que on a pas parcourur tout la liste et qu'on a pas trouvé un commerce correspondant (Sortie du while si 1 des 2 est réalisé)
            i = i + 1

        # On vérifie les quantité dispo
        erreur = str()
        if objet_produit.quantitestock < ligne_produit[1]: #Si stock insuffisant
            erreur = "Le stock de " + objet_produit.nomproduit + " est insuffisant. Quantite proposée: " + str(objet_produit.quantitestock) + ". Veuillez modifier la quantite de ce produit dans votre panier."
            #ligne_produit[1] == objet_produit.quantitestock
            error_qte = True

        if objet_produit.quantitestock == 0: #Si rupture de stock
            erreur = "Rupture de stock pour le " + objet_produit.nomproduit + ". Veuillez supprimer ce produit de votre panier."
            #ligne_produit[1] == objet_produit.quantitestock
            error_qte = True

        Erreurs.append(erreur)

        ligne_produit[0] = objet_produit  # On remplace l'id produit par un objet de type produit pour le recuperer dans la template

        #On doit tester notre sortie de while
        if not CommandesEnCours : #Si notre liste est vide

            LigneCommande = [objet_produit.idcommerce]  # Si on trouve un commerce correspondant à notre produit, alors on ajoute la nouvelle ligne produit à la suite de la ligne de commande déjà existante
            LigneCommande.append(ligne_produit)
            CommandesEnCours.append(LigneCommande)
        else :
            if CommandesEnCours[i][0].numsiret == objet_produit.idcommerce.numsiret: #Si on a trouvé un commerce qui correspond au produit
                CommandesEnCours[i].append(ligne_produit)
            elif i == (len(CommandesEnCours)-1): #Sinon
                LigneCommande = [objet_produit.idcommerce]  # Création d'une nouvelle ligne commande avec en tête le commerce
                LigneCommande.append(ligne_produit)  # A la suite du commerce on ajoute la ligne_produit (Produit,Quantite) de notre panier
                CommandesEnCours.append(LigneCommande)  # On ajoute cette nouvelle ligne de commande à notre liste de commande à traiter


    return render(request, 'panier/verification.html', locals())

def validation_commande(request):
    Commandes = trierCommandes(request)

    for commande in Commandes:
        montant_commande = float()
        for produit in commande[1]: #On recupère le montant total de chaque commande par commerce
            montant_commande = montant_commande + round((produit[0].prixproduit * produit[1]),2)
        client = Client.objects.get(numclient=request.user.id)
        new_commande = Commande(numclient=client, montantcommande=montant_commande, numcommerce=commande[0])
        new_commande.save() #Sauvegarde de la commande

        for produit in commande[1]:
            new_appartenir = Appartenir(numproduit=produit[0], numcommande=new_commande, quantitecommande=produit[1] , livraisondemande=False)
            new_appartenir.save() #Sauvegarde
            produit[0].quantitestock = produit[0].quantitestock - produit[1] #On modifie la quantite en stock du produit
            produit[0].save() #Sauvegarde

    request = init_panier(request)
    return render(request, 'panier/valide.html')

def reset_panier(request):
    return render(init_panier(request), 'panier/panier.html', locals())

#---------------- VIEWS RESERVATION ---------------------
@login_required
def afficher_reservation(request):
    reservation_session = request.session.get('reservation')
    produits = []
    prix_ClickCollect = 0.0
    for produit in reservation_session:
        objet_produit = Produit.objects.get(numproduit=produit[0])
        prix_total = objet_produit.prixproduit * produit[1]
        prix_total = round(prix_total,2)

        prix_ClickCollect = prix_ClickCollect + prix_total
        produit = [objet_produit,produit[1],prix_total]
        produits.append(produit)

    return render(request, 'reservation/reservation.html', locals())

def init_reservation(request):
    reservation = []
    request.session['reservation'] = reservation #On initialise le reservation dans la session
    return request

@login_required
def ajout_reservation(request, idproduit):
    produit = get_object_or_404(Produit, numproduit=idproduit)

    reservation_session = request.session.get('reservation')
    for produit_reservation in reservation_session:
        if produit.numproduit == produit_reservation[0]:
            produit_reservation[1]=produit_reservation[1]+1 #On incrèmente la quantite au reservation
            request.session['reservation'] = reservation_session #On sauvegarde
            return afficher_reservation(request)

    new_ligne_reservation = [produit.numproduit,1] #new_ligne_reservation = [numproduit,Quantité]
    reservation_session.append(new_ligne_reservation)
    request.session['reservation'] = reservation_session

    return afficher_reservation(request)

def supprimer_reservation(request, idproduit):
    reservation_session = request.session.get('reservation')
    for produit_reservation in reservation_session:
        if idproduit == produit_reservation[0]:
            reservation_session.remove(produit_reservation)

    request.session['reservation'] = reservation_session  # On sauvegarde
    return afficher_reservation(request)

def quantite_reservation(request, idproduit):

    reservation_session = request.session.get('reservation')
    for produit_reservation in reservation_session:
        if idproduit == produit_reservation[0]:
            produit_reservation[1]=produit_reservation[1]-1 #On modifie la quantite du produit au reservation
            if produit_reservation[1] == 0:
                produit_reservation[1]=1
    request.session['reservation'] = reservation_session #On sauvegarde
    return afficher_reservation(request)


def reset_reservation(request):
    return render(init_reservation(request), 'reservation/reservation.html', locals())


#---------------- VIEWS DE A DEFINIR ----------------