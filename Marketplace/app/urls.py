from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
	path('commerce/create', views.create_commerce, name="create_commerce"),
	path('commerce/read/<int:idcommerce>', views.read_commerce, name="read_commerce"),
	path('commerce/readByCommercant/', views.read_commerce_by_commercant, name="read_commerce_by_commercant"),
	path('commerce/delete/<int:idcommerce>', views.delete_commerce, name="delete_commerce"),
	path('commerce/update/<int:idcommerce>', views.update_commerce, name="update_commerce"),
	path('commerce/listeProduit/<int:idcommerce>', views.produit_by_commerce, name="produit_by_commerce"),
	path('commercant/update/', views.update_commercant, name="updatecommercant"),
	path('client/update/', views.update_client, name="updateclient"),
	path('produit/read/<int:pk>', views.read_produit, name="read_produit"),
	path('produit/create/<int:idcommerce>', views.create_produit, name='create_produit'),
	path('produit/delete/<int:pk>', views.delete_produit, name="delete_produit"),
	path('produit/update/<int:pk>', views.update_produit, name="updateproduit"),
	path('produit/readByVille/<str:ville>/<int:page>', views.produit_by_ville, name="read_produit_by_ville"),
	path('produit/readByCommerce/<int:idcommerce>/<int:page>', views.produit_by_commerce, name="read_produit_by_commerce"),
	path('produit/readByCategorie/<int:numcategorie>/<int:page>', views.produit_by_categorie, name = "read_produit_by_categorie"),
	path('commande/<int:idcommande>', views.read_commande, name="read_commande"),
	path('commandes/commerce/<int:idcommerce>', views.read_mescommandesCommerce, name="list_commandes_commerce"),
	path('reservation/<int:idreservation>', views.read_reservation, name="read_reservation"),
	path('reservations/commerce/<int:idcommerce>', views.read_mesreservationsCommerce, name="list_reservations_commerce"),
	path('reservation/paiement/<int:idreservation>', views.paiement_reservation, name="paiement_reservation"),
	path('reservation/paiement/reduction/', views.valider_reduction, name="validation_reduction"),
	path('dashboard/', views.dashboard_commercant, name="dashboard_commercant")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)