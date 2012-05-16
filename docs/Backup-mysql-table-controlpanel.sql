SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `myvindulaDB` DEFAULT CHARACTER SET latin1 ;
USE `myvindulaDB` ;

-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_controlpanel_company_information`
--

DROP TABLE IF EXISTS `vin_controlpanel_company_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_controlpanel_company_information` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(45) NOT NULL,
  `corporate_name` varchar(45) NOT NULL,
  `cnpj` varchar(45) NOT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `date_creation` datetime NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `stade` varchar(45) DEFAULT NULL,
  `postal_code` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `website` varchar(45) DEFAULT NULL,
  `logo_corporate` longblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_controlpanel_company_information`
--

LOCK TABLES `vin_controlpanel_company_information` WRITE;
/*!40000 ALTER TABLE `vin_controlpanel_company_information` DISABLE KEYS */;
INSERT INTO `vin_controlpanel_company_information` VALUES (1,'Vindula','Vindula Tecnologia','58.577.785/0001-45','(11) 4455-2233','Av dom Pedro II','2011-12-06 17:19:17','Santo Andre','São Paulo','09155-555','suporte@vindula.com.br','www.vindula.com.br','');
/*!40000 ALTER TABLE `vin_controlpanel_company_information` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:09:15
