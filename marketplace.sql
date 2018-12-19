-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Mar 18 Décembre 2018 à 23:24
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `marketplace`
--

-- --------------------------------------------------------

--
-- Structure de la table `appartenir`
--

CREATE TABLE `appartenir` (
  `id` int(11) NOT NULL,
  `quantitecommande` int(11) NOT NULL,
  `livraisondemande` tinyint(1) NOT NULL,
  `numcommande` int(11) NOT NULL,
  `numproduit` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `appartenir`
--

INSERT INTO `appartenir` (`id`, `quantitecommande`, `livraisondemande`, `numcommande`, `numproduit`) VALUES
(1, 10, 0, 1, 7),
(2, 2, 0, 1, 8);

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'commercant'),
(2, 'client');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(1, 1, 29),
(2, 1, 30),
(3, 1, 31),
(4, 1, 32),
(5, 1, 46),
(6, 1, 47),
(7, 1, 48),
(8, 1, 52),
(9, 1, 53),
(10, 1, 54),
(11, 1, 55),
(12, 1, 61),
(13, 1, 62),
(14, 1, 63),
(15, 1, 64),
(16, 1, 69),
(17, 1, 73),
(18, 1, 74),
(19, 1, 75),
(20, 1, 76),
(21, 2, 37),
(22, 2, 48),
(23, 2, 50),
(24, 2, 51),
(25, 2, 52),
(26, 2, 56),
(27, 2, 57),
(28, 2, 58),
(29, 2, 61),
(30, 2, 62),
(31, 2, 63),
(32, 2, 64),
(33, 2, 72),
(34, 2, 76);

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add gerer', 7, 'add_gerer'),
(26, 'Can change gerer', 7, 'change_gerer'),
(27, 'Can delete gerer', 7, 'delete_gerer'),
(28, 'Can view gerer', 7, 'view_gerer'),
(29, 'Can add categorie', 8, 'add_categorie'),
(30, 'Can change categorie', 8, 'change_categorie'),
(31, 'Can delete categorie', 8, 'delete_categorie'),
(32, 'Can view categorie', 8, 'view_categorie'),
(33, 'Can add concerner', 9, 'add_concerner'),
(34, 'Can change concerner', 9, 'change_concerner'),
(35, 'Can delete concerner', 9, 'delete_concerner'),
(36, 'Can view concerner', 9, 'view_concerner'),
(37, 'Can add reservation', 10, 'add_reservation'),
(38, 'Can change reservation', 10, 'change_reservation'),
(39, 'Can delete reservation', 10, 'delete_reservation'),
(40, 'Can view reservation', 10, 'view_reservation'),
(41, 'Can add reserver', 11, 'add_reserver'),
(42, 'Can change reserver', 11, 'change_reserver'),
(43, 'Can delete reserver', 11, 'delete_reserver'),
(44, 'Can view reserver', 11, 'view_reserver'),
(45, 'Can add commercant', 12, 'add_commercant'),
(46, 'Can change commercant', 12, 'change_commercant'),
(47, 'Can delete commercant', 12, 'delete_commercant'),
(48, 'Can view commercant', 12, 'view_commercant'),
(49, 'Can add client', 13, 'add_client'),
(50, 'Can change client', 13, 'change_client'),
(51, 'Can delete client', 13, 'delete_client'),
(52, 'Can view client', 13, 'view_client'),
(53, 'Can add produit', 14, 'add_produit'),
(54, 'Can change produit', 14, 'change_produit'),
(55, 'Can delete produit', 14, 'delete_produit'),
(56, 'Can view produit', 14, 'view_produit'),
(57, 'Can add commande', 15, 'add_commande'),
(58, 'Can change commande', 15, 'change_commande'),
(59, 'Can delete commande', 15, 'delete_commande'),
(60, 'Can view commande', 15, 'view_commande'),
(61, 'Can add commenter', 16, 'add_commenter'),
(62, 'Can change commenter', 16, 'change_commenter'),
(63, 'Can delete commenter', 16, 'delete_commenter'),
(64, 'Can view commenter', 16, 'view_commenter'),
(65, 'Can add appartenir', 17, 'add_appartenir'),
(66, 'Can change appartenir', 17, 'change_appartenir'),
(67, 'Can delete appartenir', 17, 'delete_appartenir'),
(68, 'Can view appartenir', 17, 'view_appartenir'),
(69, 'Can add reduction', 18, 'add_reduction'),
(70, 'Can change reduction', 18, 'change_reduction'),
(71, 'Can delete reduction', 18, 'delete_reduction'),
(72, 'Can view reduction', 18, 'view_reduction'),
(73, 'Can add commerce', 19, 'add_commerce'),
(74, 'Can change commerce', 19, 'change_commerce'),
(75, 'Can delete commerce', 19, 'delete_commerce'),
(76, 'Can view commerce', 19, 'view_commerce');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$120000$OE9ysdGZqPDa$LIaYu/ttbS6hKK6ouB3qdBchZtepaNlr+ip06xLA5cQ=', '2018-12-17 11:45:32.894191', 0, 'CommercantTest', 'Commercant', 'Test', 'commercant.test@test.com', 0, 1, '2018-11-08 13:00:18.962952'),
(2, 'pbkdf2_sha256$120000$4ngyfFabaQiQ$9uzChQ7jaMVmbw4spBzFYY9ztuUWRsfaI1VRFb1y974=', '2018-12-17 11:48:00.957484', 0, 'ClientTest', 'Client', 'Test', 'client.test@test.com', 0, 1, '2018-12-11 12:11:09.987169');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `categorie`
--

CREATE TABLE `categorie` (
  `numcategorie` int(11) NOT NULL,
  `nomcategorie` varchar(30) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `categorie`
--

INSERT INTO `categorie` (`numcategorie`, `nomcategorie`) VALUES
(1, 'Chaussure'),
(2, 'Multimédia'),
(3, 'Vêtements'),
(4, 'Mobilier'),
(5, 'Voiture'),
(6, 'Alimentaire'),
(7, 'Telephone'),
(8, 'Ordinateur'),
(9, 'Sport');

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `datenaissanceclient` date NOT NULL,
  `pointsclient` int(11) NOT NULL,
  `telephoneclient` varchar(15) NOT NULL,
  `codepostalclient` int(11) NOT NULL,
  `villeclient` varchar(30) NOT NULL,
  `rueclient` varchar(30) NOT NULL,
  `numclient_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `client`
--

INSERT INTO `client` (`id`, `datenaissanceclient`, `pointsclient`, `telephoneclient`, `codepostalclient`, `villeclient`, `rueclient`, `numclient_id`) VALUES
(1, '1998-10-11', 0, '0654239855', 25420, 'Bart', '56 toute de Mende', 2);

-- --------------------------------------------------------

--
-- Structure de la table `commande`
--

CREATE TABLE `commande` (
  `numcommande` int(11) NOT NULL,
  `montantcommande` double NOT NULL,
  `datecommande` date NOT NULL,
  `numclient` int(11) NOT NULL,
  `numcommerce` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `commande`
--

INSERT INTO `commande` (`numcommande`, `montantcommande`, `datecommande`, `numclient`, `numcommerce`) VALUES
(1, 228, '2018-12-15', 1, 987654321);

-- --------------------------------------------------------

--
-- Structure de la table `commenter`
--

CREATE TABLE `commenter` (
  `id` int(11) NOT NULL,
  `commentaire` longtext NOT NULL,
  `note` int(11) NOT NULL,
  `datecommentaire` date NOT NULL,
  `numclient` int(11) NOT NULL,
  `numproduit` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `commercant`
--

CREATE TABLE `commercant` (
  `id` int(11) NOT NULL,
  `telephonecommercant` varchar(15) NOT NULL,
  `numcommercant_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `commercant`
--

INSERT INTO `commercant` (`id`, `telephonecommercant`, `numcommercant_id`) VALUES
(1, '0653214897', 1);

-- --------------------------------------------------------

--
-- Structure de la table `commerce`
--

CREATE TABLE `commerce` (
  `numsiret` bigint(20) NOT NULL,
  `nomcommerce` varchar(30) NOT NULL,
  `typecommerce` varchar(30) NOT NULL,
  `emailcommerce` varchar(254) NOT NULL,
  `livraisondisponible` tinyint(1) NOT NULL,
  `telephonecommerce` varchar(15) NOT NULL,
  `codepostalcommerce` int(11) NOT NULL,
  `villecommerce` varchar(30) NOT NULL,
  `ruecommerce` varchar(30) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `commerce`
--

INSERT INTO `commerce` (`numsiret`, `nomcommerce`, `typecommerce`, `emailcommerce`, `livraisondisponible`, `telephonecommerce`, `codepostalcommerce`, `villecommerce`, `ruecommerce`) VALUES
(123456789, 'Dartyzer', 'Multumédia', 'darty.zer@test.com', 0, '0531498757', 34300, 'Agde', '10 avenue joffre'),
(987654321, 'Decathlon', 'Sport', 'decthlon@test.com', 1, '0512365842', 34200, 'Sète', '5 faubourg de Besançon'),
(326598741, 'Courrire', 'Chaussure', 'courrire@test.com', 0, '0235987456', 34000, 'Montpellier', '12 avenue charles de gaule'),
(784512369, 'Ikeo', 'Mobilier', 'ikeo@test.com', 0, '0235697415', 34000, 'Monptellier', '5 rue de la soif'),
(875421963, 'Leclerc', 'Divers', 'leclerc@test.com', 1, '0235987416', 34500, 'Béziers', '45 rue de la malouette'),
(789456123, 'PSA', 'Automobile', 'psa@test.com', 0, '0265987415', 34400, 'Lunel', '98 rue des écoliers');

-- --------------------------------------------------------

--
-- Structure de la table `concerner`
--

CREATE TABLE `concerner` (
  `id` int(11) NOT NULL,
  `numcategorie` int(11) NOT NULL,
  `numproduit` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'app', 'gerer'),
(8, 'app', 'categorie'),
(9, 'app', 'concerner'),
(10, 'app', 'reservation'),
(11, 'app', 'reserver'),
(12, 'app', 'commercant'),
(13, 'app', 'client'),
(14, 'app', 'produit'),
(15, 'app', 'commande'),
(16, 'app', 'commenter'),
(17, 'app', 'appartenir'),
(18, 'app', 'reduction'),
(19, 'app', 'commerce');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2018-11-08 12:55:58.338398'),
(2, 'auth', '0001_initial', '2018-11-08 12:55:59.822201'),
(3, 'admin', '0001_initial', '2018-11-08 12:56:00.237977'),
(4, 'admin', '0002_logentry_remove_auto_add', '2018-11-08 12:56:00.251745'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2018-11-08 12:56:00.262725'),
(6, 'app', '0001_initial', '2018-11-08 12:56:05.169401'),
(7, 'contenttypes', '0002_remove_content_type_name', '2018-11-08 12:56:05.335548'),
(8, 'auth', '0002_alter_permission_name_max_length', '2018-11-08 12:56:05.417964'),
(9, 'auth', '0003_alter_user_email_max_length', '2018-11-08 12:56:05.481280'),
(10, 'auth', '0004_alter_user_username_opts', '2018-11-08 12:56:05.496240'),
(11, 'auth', '0005_alter_user_last_login_null', '2018-11-08 12:56:05.617424'),
(12, 'auth', '0006_require_contenttypes_0002', '2018-11-08 12:56:05.624403'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2018-11-08 12:56:05.641385'),
(14, 'auth', '0008_alter_user_username_max_length', '2018-11-08 12:56:05.788196'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2018-11-08 12:56:05.865338'),
(16, 'sessions', '0001_initial', '2018-11-08 12:56:06.096188'),
(17, 'app', '0002_auto_20181112_1322', '2018-11-12 12:23:06.184939');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('k9yx2x32t99hqmszg1w9uqxozs74lvga', 'MWNkZWUyZjE4N2RlNTFmNmE1OTZkMmU0ZWI2ZmU1ODE3NjBhYTVlZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTRiYWQ3ZTcyOWUxNWM4YWFkMTllM2ZmZDY0ODg1Y2Q1M2ZjNzRlYyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-11-26 18:14:06.419725'),
('ck361b8zywejaln2xdcwllpdm3ty5a7v', 'YzBkYWMyZjU5NTc2MjdhMDZkY2VkZmY3YWM5MGU4ZWYzZTNiMmU5Nzp7Il9hdXRoX3VzZXJfaGFzaCI6ImI0ZDMzZjRhZjliNWI4OTNmMDcwOTVhNmU5MTRmMDI0M2UzOTQzMjEiLCJwYW5pZXIiOltdLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIiwicmVzZXJ2YXRpb24iOltdfQ==', '2018-12-31 13:13:04.661138');

-- --------------------------------------------------------

--
-- Structure de la table `gerer`
--

CREATE TABLE `gerer` (
  `id` int(11) NOT NULL,
  `numcommercant` int(11) NOT NULL,
  `numcommerce` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `gerer`
--

INSERT INTO `gerer` (`id`, `numcommercant`, `numcommerce`) VALUES
(4, 1, 123456789),
(5, 1, 987654321),
(6, 1, 326598741),
(7, 1, 784512369),
(8, 1, 875421963),
(9, 1, 789456123);

-- --------------------------------------------------------

--
-- Structure de la table `produit`
--

CREATE TABLE `produit` (
  `numproduit` int(11) NOT NULL,
  `nomproduit` varchar(30) NOT NULL,
  `marqueproduit` varchar(30) NOT NULL,
  `descriptifproduit` longtext NOT NULL,
  `caracteristiquesproduit` longtext NOT NULL,
  `prixproduit` double NOT NULL,
  `tauxremise` double NOT NULL,
  `quantitestock` int(11) NOT NULL,
  `quantitedisponible` int(11) NOT NULL,
  `datelimitereservation` int(11) DEFAULT NULL,
  `idcommerce` bigint(20) NOT NULL,
  `numcategorie` int(11) NOT NULL,
  `photoproduit1` varchar(100) DEFAULT NULL,
  `photoproduit2` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `produit`
--

INSERT INTO `produit` (`numproduit`, `nomproduit`, `marqueproduit`, `descriptifproduit`, `caracteristiquesproduit`, `prixproduit`, `tauxremise`, `quantitestock`, `quantitedisponible`, `datelimitereservation`, `idcommerce`, `numcategorie`, `photoproduit1`, `photoproduit2`) VALUES
(6, 'IphoneX', 'Apple', 'IphoneX de chez Apple', 'Mobile sous OS Apple - iOS 11 - 4G+\r\nÉcran tactile 14,7 cm (5,8\'\') - Super Retina 2 436 x 1 125 pixels\r\nProcesseur A11 Bionic - 64 Go de mémoire\r\nAppareil photo double capteur 12 mégapixels grand angle et téléobjectif - Vidéo UHD 4K', 899, 0, 12, 12, 20, 123456789, 7, 'media/iphone_X1.jpg', 'media/iphone_X2.jpg'),
(5, 'PC portable HP 17-BY013NF', 'HP', 'PC portable HP', 'Modèle du processeur : Core™ i3-7020U\r\nNombre de coeur(s) : 2\r\nFréquence : 2,3 GHz\r\nMémoire cache : 3 Mo\r\nType d\'écran : WLED 17,3" HD\r\nTaille d\'écran (pouces) : 17,3 \'\'\r\nRésolution maximale : 1600 x 900 pixels', 549, 0, 12, 12, 20, 123456789, 8, 'media/ph_hp1.jpg', 'media/pc_hp2.jpg'),
(4, 'One Plus 6T', 'OnePlus', 'Le dernier téléphone de chez One Plus', 'Processeur : Snapdragon 845\r\nMémoire vive : 6 Go\r\nÉcran : 6,41 pouces\r\nBatterie : 3700 mAh\r\nFréquence du processeur : 2,8 GHz\r\nFabriquant du processeur : Qualcomm\r\nInstruction processeur : ARMv8\r\nGPU : Adreno 630\r\nDéfinition : 2340 x 1080 pixels\r\nMémoire : 128 Go, 256 Go\r\nPoids : 185 g', 560, 0, 10, 10, 10, 123456789, 7, 'media/oneplus6t1.png', 'media/OnePlus6T2.jpg'),
(7, 'RAQUETTE DE TENNIS TR160 LITE', 'Artengo', 'RAQUETTE DE TENNIS TR160 LITE', 'Conçu pour le joueur débutant recherchant une raquette résistante avec un bon compromis entre légèreté et puissance.', 20, 0, 12, 12, 20, 987654321, 9, 'media/raquette_artengo1.jpg', 'media/raquette_artengo2.jpg'),
(8, 'Nike casquette noir', 'Nike', 'CASQUETTES ADULTE NIKE SPORTS DE RAQUETTES NOIRE NIKE', 'Conçu pour le joueur de tennis DEBUTANT CONFIRME EXPERT pratiquant en extérieur et recherchant une protection contre le soleil.', 14, 0, 20, 20, 10, 987654321, 3, 'media/casquette_nike1.jpg', 'media/casquette_nike2.jpg'),
(9, 'CONVERSE CHUCK TAYLOR ALL STAR', 'Converse', 'Chuck Taylor All Star Ox Core : l\'icône de toute une génération !', 'Créée en 1917 et rendue célèbre par le basketteur du même nom, la Chuck Taylor All Star est LA chaussure emblématique de Converse. La silhouette unique de ce modèle, conçu en toile et doté dune semelle en caoutchouc, est indémodable. Devenue un incontournable du dressing des sneakers-addict, elle est idéale pour adopter un style casual au quotidien. Elle a ensuite été développée dans une version', 65, 0, 10, 10, 20, 326598741, 1, 'media/converse1.jpg', 'media/converse2.jpg'),
(10, 'VANS OLD SKOOL LITE', 'Vans', 'Avec la Old Skool Lite, Vans a épuré la classique Old Skool. Sur les mêmes bases que la première, cette version Lite offre un shape plus plat et des lignes plus claires pour un style encore plus moderne. Un must-have pour un look casual au quotidien !', 'BORDEAUX/BLANC', 85, 0, 10, 10, 20, 326598741, 1, 'media/vans1.jpg', 'media/vans2.jpg'),
(11, 'FLYSTA', 'Ikeo', 'L’étagère FLYSTA est légèrement plus petite que d’autres meubles, elle s’adapte donc parfaitement aux petits espaces. Vous pouvez utiliser des boîtes pour la personnaliser.', 'Étagère, blanc', 39.95, 0, 10, 10, 20, 784512369, 4, 'media/flysta1.JPG', 'media/flysta2.JPG'),
(12, 'MOSJÖ', 'Ikeo', '1 tablette réglable. Le passe-câbles à l\'arrière permet de regrouper tous les câbles en un seul et même endroit.', 'Banc TV, brun noir', 29.95, 0, 10, 10, 20, 784512369, 4, 'media/mosjo1.JPG', 'media/mosjo2.JPG'),
(13, '8 PAUPIETTES DE VEAU “TENDRIAD', 'TENDRIADE', 'Paupiette de veau', 'Le kg : 9,61 €', 9.99, 10, 20, 20, 5, 875421963, 6, 'media/paupiette1.jpg', 'media/paupiette2.jpg'),
(14, 'TRUITE FUMÉE AU BOIS DE HÊTRE', 'LANDVIKA', '8 tranches minimum.', '200 g\r\nLe kg : 17,10 €', 4.89, 30, 20, 20, 2, 875421963, 6, 'media/saumon.jpg', ''),
(15, 'SUV 3008', 'Peugeot', 'Voiture peugeot', 'SÉCURITÉ\r\nAirbags frontaux,latéraux et rideaux\r\nDétection de sous-gonflage indirecte\r\nProjecteurs halogènes\r\nCONFORT\r\nRétroviseurs extérieurs électriques et dégivrants\r\nAir conditionné manuel\r\nLunette arrière et Vitrages latéraux arrière teintés\r\nPlancher de coffre deux positions\r\nESTHÉTIQUE\r\nDécors de planche de bord et panneaux de portes Carbone\r\nJantes 17" avec enjoliveurs \'Miami\'', 27000, 0, 10, 10, 30, 789456123, 5, 'media/30081.jpg', 'media/30082.jpg');

-- --------------------------------------------------------

--
-- Structure de la table `reduction`
--

CREATE TABLE `reduction` (
  `codereduction` int(11) NOT NULL,
  `typereduction` varchar(15) NOT NULL,
  `valeurreduction` double NOT NULL,
  `estutilise` tinyint(1) NOT NULL,
  `numclient` int(11) NOT NULL,
  `numcommerce` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `reservation`
--

CREATE TABLE `reservation` (
  `numreservation` int(11) NOT NULL,
  `montantreservation` double NOT NULL,
  `datereservation` date NOT NULL,
  `numclient` int(11) NOT NULL,
  `numcommerce` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `reserver`
--

CREATE TABLE `reserver` (
  `id` int(11) NOT NULL,
  `quantitereserve` int(11) NOT NULL,
  `numproduit` int(11) NOT NULL,
  `numreservation` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `appartenir`
--
ALTER TABLE `appartenir`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `appartenir_numproduit_numcommande_863a1845_uniq` (`numproduit`,`numcommande`),
  ADD KEY `appartenir_numcommande_dfc66219` (`numcommande`),
  ADD KEY `appartenir_numproduit_9ee5b58a` (`numproduit`);

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  ADD KEY `auth_user_groups_group_id_97559544` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  ADD KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`);

--
-- Index pour la table `categorie`
--
ALTER TABLE `categorie`
  ADD PRIMARY KEY (`numcategorie`);

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numclient_id` (`numclient_id`);

--
-- Index pour la table `commande`
--
ALTER TABLE `commande`
  ADD PRIMARY KEY (`numcommande`),
  ADD KEY `commande_numclient_83b48097` (`numclient`),
  ADD KEY `commande_numcommerce_0ac0e9ea` (`numcommerce`);

--
-- Index pour la table `commenter`
--
ALTER TABLE `commenter`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `commenter_numproduit_numclient_0ca2b601_uniq` (`numproduit`,`numclient`),
  ADD KEY `commenter_numclient_871c738c` (`numclient`),
  ADD KEY `commenter_numproduit_fdf18edc` (`numproduit`);

--
-- Index pour la table `commercant`
--
ALTER TABLE `commercant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numcommercant_id` (`numcommercant_id`);

--
-- Index pour la table `commerce`
--
ALTER TABLE `commerce`
  ADD PRIMARY KEY (`numsiret`);

--
-- Index pour la table `concerner`
--
ALTER TABLE `concerner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `concerner_numproduit_numcategorie_88ab9eeb_uniq` (`numproduit`,`numcategorie`),
  ADD KEY `concerner_numcategorie_dd6d4438` (`numcategorie`),
  ADD KEY `concerner_numproduit_5674a29e` (`numproduit`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `gerer`
--
ALTER TABLE `gerer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gerer_numcommercant_numcommerce_87d31269_uniq` (`numcommercant`,`numcommerce`),
  ADD KEY `gerer_numcommercant_73ca9c95` (`numcommercant`),
  ADD KEY `gerer_numcommerce_483a6560` (`numcommerce`);

--
-- Index pour la table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`numproduit`),
  ADD KEY `produit_idcommerce_ccd91926` (`idcommerce`),
  ADD KEY `produit_numcategorie_7179c34c` (`numcategorie`);

--
-- Index pour la table `reduction`
--
ALTER TABLE `reduction`
  ADD PRIMARY KEY (`codereduction`),
  ADD KEY `reduction_numclient_70f29ce1` (`numclient`),
  ADD KEY `reduction_numcommerce_41f192de` (`numcommerce`);

--
-- Index pour la table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`numreservation`),
  ADD KEY `reservation_numclient_b43b1c40` (`numclient`),
  ADD KEY `reservation_numcommerce_b438bd94` (`numcommerce`);

--
-- Index pour la table `reserver`
--
ALTER TABLE `reserver`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reserver_numproduit_numreservation_8d7b8f74_uniq` (`numproduit`,`numreservation`),
  ADD KEY `reserver_numproduit_aeb728ba` (`numproduit`),
  ADD KEY `reserver_numreservation_b7eee760` (`numreservation`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `appartenir`
--
ALTER TABLE `appartenir`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;
--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `categorie`
--
ALTER TABLE `categorie`
  MODIFY `numcategorie` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT pour la table `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `commande`
--
ALTER TABLE `commande`
  MODIFY `numcommande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `commenter`
--
ALTER TABLE `commenter`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `commercant`
--
ALTER TABLE `commercant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `concerner`
--
ALTER TABLE `concerner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT pour la table `gerer`
--
ALTER TABLE `gerer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT pour la table `produit`
--
ALTER TABLE `produit`
  MODIFY `numproduit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT pour la table `reduction`
--
ALTER TABLE `reduction`
  MODIFY `codereduction` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `numreservation` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `reserver`
--
ALTER TABLE `reserver`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;