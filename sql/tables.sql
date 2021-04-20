-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: bot_crush
-- ------------------------------------------------------
-- Server version	10.3.25-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Crush`
--

DROP TABLE IF EXISTS `Crush`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Crush` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recv` varchar(255) NOT NULL,
  `notification` tinyint(1) NOT NULL DEFAULT 0,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `send` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`send`) USING BTREE,
  KEY `recv` (`recv`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Tache`
--

DROP TABLE IF EXISTS `Tache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idType` int(11) NOT NULL,
  `idUser` varchar(50) NOT NULL DEFAULT '' COMMENT 'id facebook de l''utilisateur',
  `texte` varchar(500) DEFAULT '' COMMENT 'Si la tâche est envoyer un message ,c''est là qu''on met le texte à envoyer.',
  `fini` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Si la tâche est fini ou pas 1: oui et 2:non',
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `donnee` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idType` (`idType`),
  KEY `idUser` (`idUser`),
  CONSTRAINT `FK_Tache_Tache_type` FOREIGN KEY (`idType`) REFERENCES `Tache_type` (`id`),
  CONSTRAINT `FK_Tache_Utilisateur` FOREIGN KEY (`idUser`) REFERENCES `Utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COMMENT='C''est là qu''on va mettre la liste de toutes l tâches du sélenium.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tache_type`
--

DROP TABLE IF EXISTS `Tache_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tache_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='Les différents type de tâche à faire dans le Sélenium';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Utilisateur`
--

DROP TABLE IF EXISTS `Utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Utilisateur` (
  `id` varchar(50) NOT NULL COMMENT 'Id le olona ao amn le page',
  `username` varchar(255) DEFAULT NULL,
  `username_id` varchar(50) DEFAULT NULL COMMENT 'Id equivalent amn le username facebook ',
  `action` varchar(50) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  `inscrit` tinyint(1) DEFAULT 0,
  `date_inscription` date DEFAULT NULL,
  `sexe` tinyint(1) DEFAULT NULL COMMENT '1 (M), 0(F)',
  `limitCrush` int(11) DEFAULT 3,
  UNIQUE KEY `id_fb` (`id`) USING BTREE,
  UNIQUE KEY `id_username` (`username_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-20  9:50:35
