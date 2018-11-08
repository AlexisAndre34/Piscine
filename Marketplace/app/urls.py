from django.urls import path
from app import views


urlpatterns = [
	path('commerce/create', views.create_commerce, name="create_commerce")
]