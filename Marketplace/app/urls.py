from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
	path('commerce/create', views.create_commerce, name="create_commerce"),
	path('commerce/read/<int:idcommerce>', views.read_commerce, name="read_commerce"),
	path('commerce/delete/<int:idcommerce>', views.delete_commerce, name="delete_commerce"),
	path('commercant/update/', views.update_commercant, name="updatecommercant"),
	path('client/update/', views.update_client, name="updateclient"),
	path('produit/create/<int:idcommerce>', views.create_produit, name='create_produit')
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)