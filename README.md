# Piscine

#Pour débuter le développement :

Etape 1 : activer l'environnement virtuel

Etape 2 : python manage.py runserver
		(s'assurer que tout ce passe normalement)
		Si django demande de realiser des migrations :
			CTRL + c : pour arrêter le serveur de django
			1 :python manage.py makemigrations
			2 :python manage.py migrate
				(Ces commandes vont créer toutes les tables dans la base de données à partir de models.py)
			
Etape 3: Inserer dans la table 'auth_group' (auto-générée par django)
	En utilisant l'interface phpmyadmin il faut executer la commande sql suivante :
	INSERT INTO `auth_group` (`id`, `name`) VALUES(1, 'commercant'),(2, 'client');
	
	#Cette commande ajoute deux groupes à la table, commercant et client.

