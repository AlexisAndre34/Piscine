from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from app.models import Client, Commercant, Commerce, Gerer, Produit, Concerner, Categorie, Commande, Reservation, Appartenir, Reserver, Commenter, Reduction
from app.forms import SignInForm, SignUpFormClient, SignUpFormCommercant, CommerceForm, ProduitForm, UpdateClientForm, UpdateCommercantForm, CommentaireForm, ReductionForm
from datetime import datetime, timedelta
from django.db.models import Q #Pour réaliser des Query Set plus complexe, en OR
from django.core import serializers
from django.http import JsonResponse

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
                groupe = User.objects.filter(groups__name='client', id=user.id) #On cherche si notre utilisateur est un client
                if not groupe: #Si aucun objet n'est retourné, il n'est pas client
                    estClient = False
                else:           #Sinon, c'est un client
                    estClient =True
                request.session['estClient'] = estClient #On mémorise cette information
                request = init_panier(request)
                request = init_reservation(request) #On initiliase le panier et le panier_reservation de l'utilisateur

                if estClient:
                    return redirect('homepage')
                else:
                    return redirect('gestion/dashboard/')
            else:
                error=True
                #ErrorMessage = "Username ou mot de passe incorrect"
    else:
        form= SignInForm()
    return render(request, 'signin.html', locals())


def logout_user(request):
    logout(request)
    return render(request, 'accueil.html')


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
            estClient = True
            request.session['estClient'] = estClient  # On mémorise le fait que c'est un client en session
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
            estClient = False
            request.session['estClient'] = estClient  # On mémorise le fait que c'est un commerçant en session
            request = init_panier(request)
            request = init_reservation(request) #On initiliase le panier et le panier_reservation de l'utilisateur
            return redirect('homepage')
    else:
        form = SignUpFormCommercant(request.POST)
    return render(request, 'signup_commercant.html', {'formCommercant': form})

#Creation d'un commerce
@login_required
@permission_required('app.add_commerce',raise_exception=True) #Si l'utilisateur n'est pas connecté, on le redirge vers la connection. S'il est connecté mais qu'il n'a pas les droits on lève une erreur 403 (permission denied)
def create_commerce(request):
    if request.method == 'POST':
        form = CommerceForm(request.POST)
        if form.is_valid():
            commerce = form.save()
            commercant = Commercant.objects.get(numcommercant = request.user.id)
            new_gestion = Gerer(numcommercant = commercant, numcommerce = commerce)
            new_gestion.save()
            return read_commerce(request, commerce.numsiret)
    else:
        form = CommerceForm(request.POST)
    return render(request, 'create/createCommerce.html', {'formCommerce': form})

@login_required
@permission_required('app.add_produit',raise_exception=True)
def create_produit(request, idcommerce):
    #Si c'est une requete en POST
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        #On verifie que les donnees sont valides
        if form.is_valid():
            qtestock = form.cleaned_data.get('quantitestock')
            commerce = Commerce.objects.get(numsiret=idcommerce)
            new_produit = Produit(idcommerce=commerce, numcategorie=form.cleaned_data.get('choice_categorie'), nomproduit=form.cleaned_data.get('nomproduit'), marqueproduit=form.cleaned_data.get('marqueproduit'), descriptifproduit=form.cleaned_data.get('descriptifproduit'), caracteristiquesproduit=form.cleaned_data.get('caracteristiquesproduit'), prixproduit=form.cleaned_data.get('prixproduit'), tauxremise=form.cleaned_data.get('tauxremise'), quantitestock=form.cleaned_data.get('quantitestock'), quantitedisponible=qtestock, photoproduit1=form.cleaned_data.get('photoproduit1'), photoproduit2=form.cleaned_data.get('photoproduit2'))
            new_produit.save()
            new_concerner = Concerner(numcategorie=form.cleaned_data.get('choice_categorie'), numproduit=new_produit)
            new_concerner.save()
            return read_commerce(request, commerce.numsiret)
    #Si c'est une requete GET ou autre chose
    else:
        form = ProduitForm()
    return render(request, 'create/createProduit.html', {'formProduit': form})


#Doit être connecté
@login_required
@permission_required('app.add_reduction',raise_exception=True)
def create_reduction(request,idcommerce):
    utilisateur = User.objects.get(id=request.user.id)
    client = get_object_or_404(Client, numclient=utilisateur)
    commerce = get_object_or_404(Commerce, numsiret=idcommerce)

    if client.pointsclient > 1000: #On vérifie bien que le client possède suffisament de points
        if request.method == 'POST':
            form = ReductionForm(request.POST)
            if form.is_valid():
                new_reduction = Reduction(numclient=client, numcommerce=commerce, typereduction=form.cleaned_data.get('typereduction'), valeurreduction=10, estutilise=False)
                new_reduction.save()
                client.pointsclient = client.pointsclient-1000 #On réduit le nombre de points client
                client.save()
                return read_moncompte(request)
        else:
            form = ReductionForm()
        return render(request, 'create/createReduction.html', {'formReduction': form, "commerce": commerce})
    else:
        return read_moncompte(request)


#---------------- VIEWS DE LECTURE (READ) ----------------
#permet de read un commerce
@login_required
@permission_required('app.view_commerce',raise_exception=True)
def read_commerce(request, idcommerce):
    commerce = get_object_or_404(Commerce,  numsiret=idcommerce)
    estGerant = not (not Gerer.objects.filter(numcommercant=request.user.id, numcommerce=idcommerce)) #Premier not : pour tester si le resultat de la requete est vide (cela retourne un boolean) , Deuxième not : s'effectue sur le boolean retourné par le premier not

    estClient = request.session.get('estClient') #On teste si l'utilisateur est un client. Si c'est le cas on va récuperer un objet de type client pour pouvoir tester ensuite si il a un bombre de points suffisant pour générer une réduction dans la template.
    if estClient:
        client = Client.objects.get(numclient=request.user.id)


    return render(request, 'read/readCommerce.html', locals())

#permet de read tous les commerces d'un commercant
@login_required
@permission_required('app.view_commerce',raise_exception=True)
def read_commerce_by_commercant(request):
    commercant = Commercant.objects.get(numcommercant = request.user.id)
    listeGerer = Gerer.objects.filter(numcommercant = commercant)
    return render(request, 'read/readCommerceByCommercant.html', locals())

def read_commerce_by_ville(request, ville):
    listeCommerces = Commerce.objects.filter(villecommerce = ville)
    listeCom = []
    for commerce in listeCommerces:
        listeCom.append(commerce)
        
    return render(request, 'list/liste_commerces_by_ville.html', locals())


#permet de read un produit
@login_required
@permission_required('app.view_commerce',raise_exception=True)
def read_produit(request, pk):
    produit = get_object_or_404(Produit, numproduit=pk)
    commentaires = Commenter.objects.filter(numproduit=produit)

    estClient = request.session.get('estClient')
    if estClient :
      client = Client.objects.get(numclient=request.user.id)
      achat = False

      commandes_client = Commande.objects.filter(numclient=client) #On vérifie si le client à déjà commandé le produit
      if len(commandes_client)>0:
          for commande in commandes_client:
              appartenir = Appartenir.objects.filter(numcommande=commande)
              for ligne_produit in appartenir:
                  if ligne_produit.numproduit == produit:
                      achat = True

      reservations_client = Reservation.objects.filter(numclient=client, paiementrealise=True)  # On vérifie si le client à déjà reservé (et payé) le produit
      if len(reservations_client) > 0:
          for reservation in reservations_client:
              reserver = Reserver.objects.filter(numreservation=reservation)
              for ligne_produit in reserver:
                  if ligne_produit.numproduit == produit:
                      achat = True

      b1 = Commenter.objects.filter(numproduit=produit, numclient=client)#Si c'est un client, on regarde s'il a déjà commenter le produit
    
    #Si c'est une requete en POST
    if request.method == 'POST':
        formCommentaire = CommentaireForm(request.POST, request.FILES)
        #On verifie que les donnees sont valides
        if formCommentaire.is_valid():
            new_commenter = Commenter(numproduit=produit, numclient=client, commentaire=formCommentaire.cleaned_data.get('commentaire'), note=formCommentaire.cleaned_data.get('note'), datecommentaire=formCommentaire.cleaned_data.get('datecommentaire'))
            new_commenter.save()
            return render(request, 'read/readProduit.html', locals())
    #Si c'est une requete GET ou autre chose
    else:
        formCommentaire = CommentaireForm()
    return render(request, 'read/readProduit.html', locals())

#permet de read un Client
def read_moncompte(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    return render(request, 'read/moncompte.html', locals())

#permet de read une commande
@login_required
@permission_required('app.view_commande',raise_exception=True)
def read_commande(request, idcommande):
    commande = Commande.objects.get(numcommande=idcommande)
    estClient = request.session.get('estClient')
    if estClient:
        client = Client.objects.get(numclient=request.user.id)
        if commande.numclient != client: #On vérifie que le client est concerné par la reservation
            raise PermissionDenied #Si ce n'est pas le cas, permission denied
    else:
        commercant = Commercant.objects.get(numcommercant=request.user.id)
        gerer = Gerer.objects.filter(numcommercant=commercant, numcommerce=commande.numcommerce ) #On vérifie que le commerçant est concerné par la reservation
        if not gerer: #Si le commerçant ne gère pas le commerce en question
            raise PermissionDenied #Alors permission denied

    appartenir = Appartenir.objects.filter(numcommande=commande) #On arrive ici si les permissions sont bonnes
    return render(request, 'read/readCommande.html', locals())

#permet de read une reservation
@login_required
@permission_required('app.view_reservation',raise_exception=True)
def read_reservation(request, idreservation):
    reservation = Reservation.objects.get(numreservation=idreservation)
    estClient = request.session.get('estClient')
    if estClient:
        client = Client.objects.get(numclient=request.user.id)
        if reservation.numclient != client: #On vérifie que le client est concerné par la reservation
            raise PermissionDenied #Si ce n'est pas le cas, permission denied
    else:
        commercant = Commercant.objects.get(numcommercant=request.user.id)
        gerer = Gerer.objects.filter(numcommercant=commercant, numcommerce=reservation.numcommerce ) #On vérifie que le commerçant est concerné par la reservation
        if not gerer: #Si le commerçant ne gère pas le commerce en question
            raise PermissionDenied #Alors permission denied

    reserver = Reserver.objects.filter(numreservation=reservation) #On arrive ici si les permissions sont bonnes
    return render(request, 'read/readReservation.html', locals())

#permet de read les commandes d'un Client
def read_mescommandesClient(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=request.user.id)
    commandes = Commande.objects.filter(numclient=client)
    return render(request, 'read/mescommandesClient.html', locals())

#permet de read les commandes d'un Commerce
def read_mescommandesCommerce(request, idcommerce):
    utilisateur = User.objects.get(id=request.user.id)
    commercant = Commercant.objects.get(numcommercant=utilisateur)
    commerce = get_object_or_404(Gerer, numcommercant=commercant, numcommerce=idcommerce) #On doit faire la requete sur un objet de type commerçant
    commandes = Commande.objects.filter(numcommerce=commerce.numcommerce).order_by('-datecommande') #De manière générale on fait les requetes sur le type le plus souvent
    return render(request, 'list/list_commandes_commerces.html', {'commandes': commandes})

#permet de read les réservations d'un Client
def read_mesreservationsClient(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=utilisateur)
    reservations = Reservation.objects.filter(numclient=client).order_by('paiementrealise') #Résultat ordonné, les réservations non payés d'abord, ensuite c'est ordonné par date
    return render(request, 'read/mesreservationsClient.html', locals())

#permet de read les réservations d'un Commerce
def read_mesreservationsCommerce(request, idcommerce):
    utilisateur = User.objects.get(id=request.user.id)
    commercant = Commercant.objects.get(numcommercant=utilisateur)
    commerce = get_object_or_404(Gerer, numcommercant=commercant, numcommerce=idcommerce) #On doit faire la requete sur un objet de type commerçant
    reservations = Reservation.objects.filter(numcommerce=commerce.numcommerce, paiementrealise=False).order_by('-datereservation') #On cherche les réservations qui n'ont pas été payé par le client et on trie nos reservations avec les date de réservations de la plus rècente à la plus ancienne,
    return render(request, 'list/list_reservations_commerces.html', {'reservations': reservations})

def list_commerces_carte(request):
    return render(request, 'list/map_commerces.html')

def list_reduction(request):
    utilisateur = User.objects.get(id=request.user.id)
    client = Client.objects.get(numclient=utilisateur)
    reductions = Reduction.objects.filter(numclient=client)
    return render(request, 'list/list_reductions.html', {'reductions': reductions})

@login_required
@permission_required('app.view_commerce',raise_exception=True)
def carte_commerces(request):

    commerces = Commerce.objects.all()
    data = {
        "commerces": serializers.serialize("json", commerces)
    }

    return JsonResponse(data)

def carte_search(request):
    recherche = request.POST.get('recherche')
    commerces = Commerce.objects.filter(nomcommerce__icontains=recherche)
    data = {
        "commerces": serializers.serialize("json", commerces)
    }

    return JsonResponse(data)

#---------------- VIEWS DE MISES A JOUR (UPDATE) ----------------
@login_required
@permission_required('app.change_commercant',raise_exception=True)
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
            return dashboard_commercant(request)
    else:
        return render(request, 'update/updateCommercant.html', locals())

@login_required
@permission_required('app.change_client',raise_exception=True)
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
            return read_moncompte(request)
    else:
        date = str(client.datenaissanceclient.year)+"-"+str(client.datenaissanceclient.month)+"-"+str(client.datenaissanceclient.day) #Permet d'avoir le bon format de date pour le input : type=date , du formulaire
        return render(request, 'update/updateClient.html', locals())

@login_required
@permission_required('app.change_commerce',raise_exception=True)
def update_commerce(request, idcommerce):
    user = User.objects.get(id=request.user.id)
    commerce = get_object_or_404(Commerce, numsiret=idcommerce)
    if request.method == "POST":
        commerce.nomcommerce = request.POST.get('nomcommerce')
        commerce.typecommerce = request.POST.get('typecommerce')
        commerce.emailcommerce = request.POST.get('emailcommerce')
        commerce.livraisondisponible = request.POST.get('livraisondisponible')
        commerce.joursretrait = request.POST.get('joursretrait')
        commerce.horairescommerce = request.POST.get('horairescommerce')
        commerce.telephonecommerce = request.POST.get('telephonecommerce')
        commerce.codepostalcommerce = request.POST.get('codepostalcommerce')
        commerce.villecommerce = request.POST.get('villecommerce')
        commerce.ruecommerce = request.POST.get('ruecommerce')
        commerce.gpslatitude = request.POST.get('gpslatitude')
        commerce.gpslongitude = request.POST.get('gpslongitude')
        commerce.save()
        gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
        return read_commerce(request, commerce.numsiret)
    else:
        form = CommerceForm(instance=commerce)
    return render(request, 'update/updateCommerce.html', locals())

# mise a jour d'un produit
@login_required
@permission_required('app.change_produit',raise_exception=True)
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
            new_quantite = form.cleaned_data.get('quantitestock') - produit.quantitestock
            produit.quantitestock = produit.quantitestock + new_quantite
            produit.quantitedisponible = produit.quantitedisponible + new_quantite
            if produit.quantitedisponible < 0:
                produit.quantitedisponible = 0
            if form.cleaned_data.get('photoproduit1') is not None:
                produit.photoproduit1 = form.cleaned_data.get('photoproduit1')

            if form.cleaned_data.get('photoproduit2') is not None:
                produit.photoproduit2 =form.cleaned_data.get('photoproduit2')
            produit.numcategorie = form.cleaned_data.get('choice_categorie')

            produit.save()
            concerner = Concerner.objects.get(numproduit=produit) #On met également la table Concerner à jour en modifiant la categorie associé à notre produit
            concerner.numcategorie = form.cleaned_data.get('choice_categorie')
            concerner.save()
            return read_commerce(request, produit.idcommerce.numsiret)
    else:
        form = ProduitForm(instance=produit)
        print(form)
    return render(request, 'update/updateProduit.html', {'Produitform': form})


#---------------- VIEWS DE SUPPRESSION (DELETE) ----------------

#permet de delete un commerce
@login_required
@permission_required('app.delete_commerce',raise_exception=True)
def delete_commerce(request, idcommerce):
    gerer = get_object_or_404(Gerer, numcommercant=request.user.id, numcommerce=idcommerce)
    if request.method == 'POST':
        Commerce.objects.get(numsiret = idcommerce).delete()
        return dashboard_commercant(request)

    return render(request, 'delete/deleteView.html')
		
#permet de delete un produit
@login_required
@permission_required('app.delete_produit',raise_exception=True)
def delete_produit(request, pk):
    produit = get_object_or_404(Produit , numproduit=pk)
    if request.method == 'POST':
        Produit.objects.get(numproduit = pk).delete()
        return render(request, 'index.html')

    return render(request, 'delete/deleteView.html')



#--------------- SEARCH -------------------------#
@login_required
def search(request, keyword=None, page=1):
    #keyword et page sont utilisé lorsque l'utilisateur fait défiler les pages, par défaut ils valent respectivement None et 1
    recherche = request.POST.get('recherche') #On récupère la recherche de l'utilisateur qui nous est envoyé en requete POST
    if keyword is None : #Si la recherche est Vide
        if not recherche:
            return redirect('/') #Redirection vers la page d'accueil si aucun champ de recherche
            #redirect(request.META['HTTP_REFERER']) redirige l'utilisateur vers la page précedente mais problème de boucle infinie
        else:
            categories = Categorie.objects.filter(nomcategorie__icontains=recherche)
            if not categories: #Si aucune categorie trouvée
                produits_all = Produit.objects.filter(nomproduit__icontains=recherche)
            else:
                produits_all = Produit.objects.filter(Q(nomproduit__icontains=recherche) | Q(numcategorie=categories[0].numcategorie)) #On prend la première categorie qui à été retourné suite à notre requete

            produits = pagination(produits_all,page)
            return render(request, 'list/produits_recherche.html', locals())
    else:

        categories = Categorie.objects.filter(nomcategorie__icontains=keyword)
        if not categories:  # Si aucune categorie trouvée
            produits_all = Produit.objects.filter(nomproduit__icontains=keyword)
        else:
            produits_all = Produit.objects.filter(Q(nomproduit__icontains=keyword) | Q(numcategorie=categories[0].numcategorie))  # On prend la première categorie qui à été retourné suite à notre requete

        recherche=keyword #On passe la recherche à travers les différentes pages de la pagination

        produits = pagination(produits_all, page)
        return render(request, 'list/produits_recherche.html', locals())


def pagination(liste,nb_page):
    paginator = Paginator(liste, 2)  # On affiche 2 produit par page
    try:
        produits = paginator.page(nb_page)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

    return produits

#---------------- VIEWS DE LISTE ----------------
#permet de voir les produits d'un commerce
@login_required
@permission_required('app.view_commerce',raise_exception=True)
def produit_by_commerce(request, idcommerce, page=1):
    produitsParCommerce = Produit.objects.filter(idcommerce = idcommerce)
    listeProduits = []
    for produit in produitsParCommerce:
        listeProduits.append(produit)

    produits = pagination(listeProduits, page)
    return render(request, 'list/produits_by_commerce.html', locals())

#permet de voir les produits par ville
@login_required
@permission_required('app.view_commerce',raise_exception=True)
def produit_by_ville(request, ville, page=1):
    listeCommerces = Commerce.objects.filter(villecommerce = ville)
    listeProduits = []
    for commerce in listeCommerces:
        produitsParCommerce = Produit.objects.filter(idcommerce = commerce.numsiret)
        for produit in produitsParCommerce:
            listeProduits.append(produit)


    produits = pagination(listeProduits, page)
    return render(request, 'list/produit_by_ville.html', locals())

#permet de voir les produits par categorie
@login_required
@permission_required('app.view_produit',raise_exception=True)
def produit_by_categorie(request, numcategorie, page=1):
    produitsParCategorie = Produit.objects.filter(numcategorie = numcategorie)
    listeProduits = []
    for produit in produitsParCategorie:
        listeProduits.append(produit)

    produits = pagination(listeProduits,page) #La fonction que l'on appelle va créer la pagination pour ces produits
    return render(request, 'list/produits_by_categorie.html', locals())







#---------------- VIEWS DASHBOARD ----------------

@login_required
def dashboard_commercant(request):
    utilisateur = User.objects.get(id=request.user.id)
    commercant = Commercant.objects.get(numcommercant=request.user.id)
    return render(request, 'dashboard_commercant.html', locals())


#---------------- COMMUN  PANIER ET RESERVATION ----------------

#Affichage du panier si choix=True, si choix=False alors affichage des reservations
@login_required
@permission_required('app.view_reservation','app.view_commande',raise_exception=True)
def afficher_demande(request, choix):
    resultat = list()
    produits = list()
    prix_demande = float()
    panier_vide = True

    if choix:
        demande = request.session.get('panier')
    else:
        demande = request.session.get('reservation')

    for produit in demande:
        objet_produit = Produit.objects.get(numproduit=produit[0])
        prix_total = (objet_produit.prixproduit - ( (objet_produit.prixproduit * objet_produit.tauxremise) / 100)) * produit[1]
        prix_total = round(prix_total, 2)
        prix_demande = prix_demande + prix_total

        produit = [objet_produit,produit[1],prix_total]
        produits.append(produit)
    if produits:
        panier_vide = False

    # resultat = [produits,prix_demande,panier_vide]
    resultat.append(produits)
    resultat.append(prix_demande)
    resultat.append(panier_vide)

    return resultat


# trierDemande: requets x Bool -> list[]
# trie le panier si choix == True
# trie les reservation si choix == False
def trierDemande(request, choix):
    # LigneCommande = list() #LigneCommande = [Commerce1, [ [Ligne_produit1], [Ligne_produit2], ... ] ]
    CommandesEnCours = list()  # CommandesEnCours = [ [LigneCommande1], [LigneCommande2], ... ]
    Erreur = str()
    prix_total = float()
    error_qte = False

    if choix:
        demande = request.session.get('panier')
    else:
        demande = request.session.get('reservation')

    for ligne_produit in demande:
        objet_produit = Produit.objects.get(numproduit=ligne_produit[0])
        prix_total = prix_total + round(( (objet_produit.prixproduit - ( (objet_produit.prixproduit * objet_produit.tauxremise) / 100)) * ligne_produit[1]), 2)
        i = 0  # // i de 0 à len(CommandeEnCours)-1
        while (i < (len(CommandesEnCours)-1)) and CommandesEnCours[i][0].numsiret != objet_produit.idcommerce.numsiret:  # Tant que on a pas parcourur tout la liste et qu'on a pas trouvé un commerce correspondant (Sortie du while si 1 des 2 est réalisé)
            i = i + 1

        # On vérifie les quantité dispo
        if objet_produit.quantitedisponible < ligne_produit[1]:  # Si stock insuffisant
            Erreur = "Le stock de " + objet_produit.nomproduit + " est insuffisant. Quantite disponible: " + str(objet_produit.quantitedisponible) + ". Veuillez modifier la quantite de ce produit dans votre panier."
            # ligne_produit[1] == objet_produit.quantitedisponible
            error_qte = True

        if objet_produit.quantitestock == 0 or objet_produit.quantitedisponible == 0 :  # Si rupture de stock
            Erreur = "Rupture de stock pour le " + objet_produit.nomproduit + ". Veuillez supprimer ce produit de votre panier."
            # ligne_produit[1] == objet_produit.quantitedisponible
            error_qte = True

        ligne_produit[0] = objet_produit  # On remplace l'id produit par un objet de type produit pour le recuperer dans la template

        # On doit tester notre sortie de while
        if not CommandesEnCours:  # Si notre liste est vide
            LigneCommande = [objet_produit.idcommerce]  # Si on trouve un commerce correspondant à notre produit, alors on ajoute la nouvelle ligne produit à la suite de la ligne de commande déjà existante
            LigneCommande.append(list())  # On insère une liste vide qui accueillera toutes les lignes produit
            LigneCommande[1].append(ligne_produit)
            CommandesEnCours.append(LigneCommande)
        else:
            if CommandesEnCours[i][0].numsiret == objet_produit.idcommerce.numsiret:  # Si on a trouvé un commerce qui correspond au produit
                CommandesEnCours[i][1].append(ligne_produit)
            elif i == (len(CommandesEnCours) - 1):  # Sinon
                LigneCommande = [objet_produit.idcommerce]  # Création d'une nouvelle ligne commande avec en tête le commerce
                LigneCommande.append(list())
                LigneCommande[1].append(ligne_produit)  # A la suite du commerce on ajoute la ligne_produit (Produit,Quantite) de notre panier
                CommandesEnCours.append(LigneCommande)  # On ajoute cette nouvelle ligne de commande à notre liste de commande à traiter

    Reponse = list()
    Reponse.append(CommandesEnCours)
    Reponse.append(Erreur)
    Reponse.append(error_qte)
    Reponse.append(prix_total)
    return Reponse
#---------------- VIEWS PANIER ----------------

@login_required
def afficher_panier(request):
    resultat = afficher_demande(request,True)
    produits = resultat[0]
    prix_panier = resultat[1]
    panier_vide = resultat[2]
    return render(request, 'panier/panier.html', locals())

@login_required
def init_panier(request):
    panier = list()
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

@login_required
def supprimer_panier(request, idproduit):
    panier_session = request.session.get('panier')
    for produit_panier in panier_session:
        if idproduit == produit_panier[0]:
            panier_session.remove(produit_panier)

    request.session['panier'] = panier_session  # On sauvegarde
    return afficher_panier(request)

@login_required
def quantite_panier(request, idproduit):

    panier_session = request.session.get('panier')
    for produit_panier in panier_session:
        if idproduit == produit_panier[0]:
            produit_panier[1]=produit_panier[1]-1 #On modifie la quantite du produit au panier
            if produit_panier[1] == 0:
                produit_panier[1]=1
    request.session['panier'] = panier_session #On sauvegarde
    return afficher_panier(request)


@login_required
def verification_commande(request):
    Reponse = trierDemande(request,True)
    CommandesEnCours = Reponse[0]
    Erreur = Reponse[1]
    error_qte = Reponse[2]
    prix_total = Reponse[3]

    return render(request, 'panier/verificationPanier.html', locals())

@login_required
def validation_commande(request):
    Reponse = trierDemande(request,True)
    Commandes = Reponse[0]

    for commande in Commandes:
        montant_commande = float()
        for produit in commande[1]: #On recupère le montant total de chaque commande par commerce
            montant_commande = montant_commande + round( ( (produit[0].prixproduit - ((produit[0].prixproduit * produit[0].tauxremise)/100)) * produit[1]),2)
        client = Client.objects.get(numclient=request.user.id)
        new_commande = Commande(numclient=client, montantcommande=montant_commande, numcommerce=commande[0])
        new_commande.save() #Sauvegarde de la commande

        for produit in commande[1]:
            new_appartenir = Appartenir(numproduit=produit[0], numcommande=new_commande, quantitecommande=produit[1] , livraisondemande=False)
            new_appartenir.save() #Sauvegarde
            produit[0].quantitestock = produit[0].quantitestock - produit[1] #On modifie la quantite en stock du produit
            produit[0].quantitedisponible = produit[0].quantitedisponible - produit[1] #On modifie la quantite disponible du produit
            produit[0].save() #Sauvegarde

    type_demande = "commande"
    request = init_panier(request)
    return render(request, 'panier/valide.html', {'type_demande': type_demande})

@login_required
def reset_panier(request):
    return render(init_panier(request), 'panier/panier.html', locals())

#---------------- VIEWS RESERVATION ---------------------
@login_required
def afficher_reservation(request):
    resultat = afficher_demande(request, False)
    produits = resultat[0]
    prix_ClickCollect = resultat[1]
    reservation_vide = resultat[2]
    return render(request, 'reservation/reservation.html', locals())

def init_reservation(request):
    reservation = list()
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

@login_required
def supprimer_reservation(request, idproduit):
    reservation_session = request.session.get('reservation')
    for produit_reservation in reservation_session:
        if idproduit == produit_reservation[0]:
            reservation_session.remove(produit_reservation)

    request.session['reservation'] = reservation_session  # On sauvegarde
    return afficher_reservation(request)

@login_required
def quantite_reservation(request, idproduit):

    reservation_session = request.session.get('reservation')
    for produit_reservation in reservation_session:
        if idproduit == produit_reservation[0]:
            produit_reservation[1]=produit_reservation[1]-1 #On modifie la quantite du produit au reservation
            if produit_reservation[1] == 0:
                produit_reservation[1]=1
    request.session['reservation'] = reservation_session #On sauvegarde
    return afficher_reservation(request)

@login_required
def verification_reservation(request):
    Reponse = trierDemande(request,False)
    ReservationsEnCours = Reponse[0]
    Erreur = Reponse[1]
    error_qte = Reponse[2]
    prix_total = Reponse[3]

    return render(request, 'reservation/verificationReservation.html', locals())

@login_required
def validation_reservations(request):
    reponse = trierDemande(request, False)
    Reservations = reponse[0]
    reservations = list() #Pour afficher dans la template l'ensemble des réservations effectué par commerce et afficher la date limite de retrait
    for reservation in Reservations:
        montant_reservation = float()
        for produit in reservation[1]:
            montant_reservation = montant_reservation + round( ( (produit[0].prixproduit - ((produit[0].prixproduit * produit[0].tauxremise)/100)) * produit[1]),2 )
            datelimite = datetime.now() + timedelta(days=reservation[0].joursretrait)
        client = Client.objects.get(numclient =request.user.id)
        new_reservation = Reservation(numclient=client, montantreservation = montant_reservation, numcommerce=reservation[0], datelimitereservation=datelimite, paiementrealise=False)
        new_reservation.save()
        reservations.append(new_reservation)
        for produit in reservation[1]:
            new_reserver = Reserver(numproduit=produit[0], numreservation=new_reservation, quantitereserve=produit[1])
            new_reserver.save()
            produit[0].quantitedisponible = produit[0].quantitedisponible - produit[1]
            produit[0].save()



    type_demande = "reservation"
    request = init_reservation(request)
    return render(request, 'panier/valide.html', locals())

@login_required
def paiement_reservation(request, idreservation):
    reservation = get_object_or_404(Reservation, numreservation=idreservation)
    commercant = get_object_or_404(Commercant, numcommercant=request.user.id)
    verification = get_object_or_404(Gerer, numcommerce=reservation.numcommerce, numcommercant=commercant)

    #Si toutes les vérifications ont été passé et qu'aucune erreur 404 n'a été levée alors:
    reservation.paiementrealise = True #On modifie la reservation
    reservation.save()
    produits_reserver = Reserver.objects.filter(numreservation=reservation.numreservation)
    for produit_reserver in produits_reserver: #On va mdofier chaque produit de la reservation du client, pour changer leur quantite en stock
        produit_reserver.numproduit.quantitestock = produit_reserver.numproduit.quantitestock - produit_reserver.quantitereserve
        produit_reserver.numproduit.save()

    client = reservation.numclient
    client.pointsclient = client.pointsclient + int(reservation.montantreservation)
    client.save()
    return read_mesreservationsCommerce(request, reservation.numcommerce)

@login_required
def reset_reservation(request):
    return render(init_reservation(request), 'reservation/reservation.html', locals())

#---------------- VIEWS POUR LES REDUCTIONS  ----------------

def valider_reduction(request):
    message = "hello"
    code_reduction = request.POST.get('code_reduction')
    id_reservation = request.POST.get('id_reservation')

    reduction = Reduction.objects.filter(codereduction=code_reduction)
    if not reduction: #Si pas de résultat à notre requête
        message = "Réduction inexistante"
    else:
        reduction = reduction[0]
        if reduction.estutilise == True:
            message = "Réduction déjà utilisé"
        else:
            reservation = Reservation.objects.filter(numreservation=id_reservation)
            if not reservation:
                message = "Numéro de réservation incorrect."
            else:
                reservation = reservation[0]
                if reduction.typereduction == "bon": #On vérifie si la réduction est un bon ou un pourcentage
                    type="euros"
                    reservation.montantreservation = reservation.montantreservation - reduction.valeurreduction
                else:
                    type="%"
                    reservation.montantreservation = reservation.montantreservation - ((reservation.montantreservation*reduction.valeurreduction)/100)
                reduction.estutilise = True
                reduction.save()
                reservation.save()
                message = "La réduction à été utilisée correctement ("+reduction.typereduction+" de "+str(reduction.valeurreduction)+" "+type+"). Procèder maitenant au paiement avec le client : "+str(reservation.montantreservation)+" euros. Veuillez ensuite valider le paiement de la réservation n° "+id_reservation+"."

    data = {
        "message": message
    }
    return JsonResponse(data)

#---------------- VIEWS COMPARAISON ----------------

def comparaison(request):
    id_produit1 = request.POST.get('produit1')
    id_produit2 = request.POST.get('produit2')
    produit1 = Produit.objects.get(numproduit=id_produit1)
    produit2 = Produit.objects.get(numproduit=id_produit2)

    return render(request, 'read/comparaison.html', {'produit1': produit1, 'produit2': produit2})



#---------------- VIEWS DE A DEFINIR ----------------