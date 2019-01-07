from django.contrib import admin
from .models import Client, Commercant, Gerer, Produit, Categorie, Commerce, Commande, Reservation, Concerner, Appartenir, Reserver


#Partie : Personnalisation des models pour l'administrateur

class ClientAdmin(admin.ModelAdmin):
    list_display = ('numclient','codepostalclient','villeclient') #On choisit les attributs qui seront affichés sur la page admin
    search_fields = ('numclient','villeclient') #On choisit les éléments qui seront disponibles à la recherche

class CommercantAdmin(admin.ModelAdmin):
    list_display = ('numcommercant','telephonecommercant')

class GererAdmin(admin.ModelAdmin):
    list_display = ('numcommercant',"numcommerce")
    search_fields = ('numcommercant', "numcommerce")

class ProduitAdmin(admin.ModelAdmin):
   list_display   = ('numproduit', 'nomproduit', 'marqueproduit', 'prixproduit','tauxremise')
   search_fields = ('numproduit','marqueproduit', 'nomproduit','numproduit')


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('numcategorie','nomcategorie')
    search_fields = ('numcategorie','nomcategorie')

class CommerceAdmin(admin.ModelAdmin):
    list_display = ('numsiret','nomcommerce','typecommerce','emailcommerce','livraisondisponible','telephonecommerce','codepostalcommerce','villecommerce')
    search_fields = ('numsiret','nomcommerce','typecommerce')


class CommandeAdmin(admin.ModelAdmin):
    list_display = ('numcommande','numclient','numcommerce','montantcommande','datecommande')
    search_fields = ('numcommande','datecommande')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('numreservation','numclient','numcommerce','montantreservation','datereservation','paiementrealise')
    search_fields = ('numreservation','montantreservation','datereservation')

class ConcernerAdmin(admin.ModelAdmin):
    list_display = ('numcategorie','numproduit')
    search_fields = ('numcategorie','numproduit')

class AppartenirAdmin(admin.ModelAdmin):
    list_display = ('numproduit','numcommande')
    search_fields = ('numproduit','numcommande')

class ReserverAdmin(admin.ModelAdmin):
    list_display = ('numproduit','numreservation','quantitereserve')
    search_fields = ('numproduit','numreservation')


#Partie 2

admin.site.register(Client, ClientAdmin) #Permet d'administrer le model 'Client' avec la personnalisation 'ClientAdmin' de la partie 1
admin.site.register(Commercant, CommercantAdmin)
admin.site.register(Gerer, GererAdmin)


admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Commerce, CommerceAdmin)

admin.site.register(Commande, CommandeAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Concerner, ConcernerAdmin)
admin.site.register(Appartenir, AppartenirAdmin)
admin.site.register(Reserver, ReserverAdmin)
