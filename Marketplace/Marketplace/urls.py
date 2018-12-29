"""Marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('signup/commercant', views.signup_commercant, name='signupCommercant'),
    path('signup/client', views.signup_client, name='signupClient'),
    path('moncompte/', views.read_moncompte, name="moncompte"),
    path('moncompte/commandes', views.read_mescommandesClient, name="mescommandesClient"),
    path('moncompte/reservations', views.read_mesreservationsClient, name="mesreservationsClient"),
    path('moncompte/reduction/creation/<int:idcommerce>', views.create_reduction, name="create_reduction"),
	path('search/', views.search, name="search"),
	path('search/<str:keyword>/<int:page>', views.search, name="search"),
    path('panier/afficher/', views.afficher_panier, name="afficher_panier"),
    path('panier/ajout/<int:idproduit>', views.ajout_panier, name="ajout_panier"),
    path('panier/supprimer/<int:idproduit>', views.supprimer_panier, name="supprimer_panier"),
    path('panier/quantite/<int:idproduit>', views.quantite_panier, name="quantite_less_panier"),
    path('panier/verfication/', views.verification_commande, name="verification_panier"),
    path('commande/valide', views.validation_commande, name="validation_commande"),
    path('panier/reset/', views.reset_panier, name="reset_panier"),
    path('reservation/afficher/', views.afficher_reservation, name="afficher_reservation"),
    path('reservation/ajout/<int:idproduit>', views.ajout_reservation, name="ajout_reservation"),
    path('reservation/supprimer/<int:idproduit>', views.supprimer_reservation, name="supprimer_reservation"),
    path('reservation/quantite/<int:idproduit>', views.quantite_reservation, name="quantite_less_reservation"),
    path('reservation/verification', views.verification_reservation, name="verification_reservation"),
    path('reservation/valide', views.validation_reservations, name="validation_reservation"),
    path('reservation/reset/', views.reset_reservation, name="reset_reservation"),
    path('carte/commerces', views.list_commerces_carte, name="commerces_carte"),
    path('carte/commerces/affichage', views.carte_commerces, name="commerces_carte_affichage"),
    path('carte/commerces/search', views.carte_search, name="commerces_carte_search"),
  path('gestion/', include('app.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
