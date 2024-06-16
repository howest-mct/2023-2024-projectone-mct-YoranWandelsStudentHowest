CREATE DATABASE  IF NOT EXISTS `musclefuel_dispenser` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `musclefuel_dispenser`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: musclefuel_dispenser
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `DeviceID` int NOT NULL AUTO_INCREMENT,
  `Naam` varchar(45) NOT NULL,
  `Merk` varchar(45) DEFAULT NULL,
  `Beschrijving` varchar(255) DEFAULT NULL,
  `Type` varchar(45) NOT NULL,
  `AankoopKost` float DEFAULT NULL,
  `Meeteenheid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`DeviceID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'HC-SR04','TZT','Afstand meten','Sensor',1.65,'cm'),(2,'HC-SR04','TZT','Afstand meten','Sensor',1.65,'cm'),(3,'5KG-LoadCell','NQP','Gewicht meten','Sensor',5,'gram'),(4,'5KG-LoadCell','NQP','Gewicht meten','Sensor',5,'gram'),(5,'StepperMotor','Oumefar','Stappenmotor om de auger te laten draaien','Actuator',3,NULL),(6,'StepperMotor','Oumefar','Stappenmotor om de auger te laten draaien','Actuator',3,NULL),(7,'RotaryEncoder','Opencircuit','Rotary encoder om de display te kunnen besturen','Sensor',3,'Binair'),(8,'WaterPump','Fockety','Waterpomp om water te pompen','Actuator',1.59,NULL),(9,'PushButton','ELECFREAKS','Button om de machine aan/uit te zetten','Sensor',3.13,'Binair'),(10,'LCD-Display','Displaytech','LCD-Diplay om informatie te tonen aan de gebruiker','Actuator',4.2,NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gebruiker`
--

DROP TABLE IF EXISTS `gebruiker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gebruiker` (
  `GebruikerID` int NOT NULL AUTO_INCREMENT,
  `Gebruikersnaam` varchar(50) NOT NULL,
  `Wachtwoord` varchar(255) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Voornaam` varchar(50) DEFAULT NULL,
  `Achternaam` varchar(50) DEFAULT NULL,
  `Geboortedatum` date DEFAULT NULL,
  `Rol` varchar(20) DEFAULT 'user',
  `AccountStatus` varchar(20) DEFAULT 'actief',
  `Aanmaakdatum` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LaatstIngelogd` datetime DEFAULT NULL,
  PRIMARY KEY (`GebruikerID`),
  UNIQUE KEY `UK_Gebruikersnaam` (`Gebruikersnaam`),
  UNIQUE KEY `UK_Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gebruiker`
--

LOCK TABLES `gebruiker` WRITE;
/*!40000 ALTER TABLE `gebruiker` DISABLE KEYS */;
INSERT INTO `gebruiker` VALUES (1,'testuser','hashedpassword','testuser@example.com','Test','User',NULL,'user','actief','2024-05-24 14:31:47',NULL);
/*!40000 ALTER TABLE `gebruiker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `Volgnummer` int NOT NULL AUTO_INCREMENT,
  `DeviceID` int NOT NULL,
  `GebruikerID` int NOT NULL,
  `Actiedatum` datetime NOT NULL,
  `Waarde` float NOT NULL,
  `Commentaar` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Volgnummer`),
  KEY `FK_deviceID_idx` (`DeviceID`),
  KEY `FK_gebruikerID_idx` (`GebruikerID`),
  CONSTRAINT `FK_deviceID` FOREIGN KEY (`DeviceID`) REFERENCES `device` (`DeviceID`),
  CONSTRAINT `FK_gebruikerID` FOREIGN KEY (`GebruikerID`) REFERENCES `gebruiker` (`GebruikerID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,1,1,'2024-05-23 08:00:00',1,'Fles staat onder machine'),(2,2,1,'2024-05-23 08:05:00',50,'Genoeg water beschikbaar'),(3,3,1,'2024-05-23 08:10:00',200,'Proteïne poeder voldoende'),(4,4,1,'2024-05-23 08:15:00',100,'Creatine poeder voldoende'),(5,8,1,'2024-05-23 08:20:00',300,'Water gepompt'),(6,6,1,'2024-05-23 08:25:00',50,'Proteïne poeder bediend'),(7,6,1,'2024-05-23 08:30:00',30,'Creatine poeder bediend'),(8,9,1,'2024-05-23 08:35:00',1,'Machine aangezet'),(9,10,1,'2024-05-23 08:40:00',1,'LCD scherm bestuurd'),(10,10,1,'2024-05-23 08:45:00',1,'Shake gemaakt'),(11,1,1,'2024-05-23 08:50:00',0,'Geen fles onder machine'),(12,2,1,'2024-05-23 08:55:00',10,'Weinig water beschikbaar'),(13,3,1,'2024-05-23 09:00:00',150,'Proteïne poeder bijna op'),(14,4,1,'2024-05-23 09:05:00',80,'Creatine poeder bijna op'),(15,8,1,'2024-05-23 09:10:00',250,'Water bijna op'),(16,6,1,'2024-05-23 09:15:00',40,'Beetje proteïne poeder gebruikt'),(17,6,1,'2024-05-23 09:20:00',20,'Beetje creatine poeder gebruikt'),(18,9,1,'2024-05-23 09:25:00',0,'Machine uitgezet'),(19,10,1,'2024-05-23 09:30:00',0,'LCD scherm uitgezet'),(20,10,1,'2024-05-23 09:35:00',1,'Shake mislukt'),(21,1,1,'2024-05-23 09:40:00',1,'Fles staat onder machine'),(22,2,1,'2024-05-23 09:45:00',45,'Voldoende water beschikbaar'),(23,3,1,'2024-05-23 09:50:00',220,'Proteïne poeder bijgevuld'),(24,4,1,'2024-05-23 09:55:00',110,'Creatine poeder bijgevuld'),(25,8,1,'2024-05-23 10:00:00',290,'Water gepompt'),(26,6,1,'2024-05-23 10:05:00',55,'Proteïne poeder bediend'),(27,6,1,'2024-05-23 10:10:00',35,'Creatine poeder bediend'),(28,9,1,'2024-05-23 10:15:00',1,'Machine opnieuw aangezet'),(29,10,1,'2024-05-23 10:20:00',1,'LCD scherm bestuurd'),(30,10,1,'2024-05-23 10:25:00',1,'Shake opnieuw gemaakt'),(31,1,1,'2024-05-23 10:30:00',1,'Fles staat onder machine'),(32,2,1,'2024-05-23 10:35:00',50,'Genoeg water beschikbaar'),(33,3,1,'2024-05-23 10:40:00',200,'Proteïne poeder voldoende'),(34,4,1,'2024-05-23 10:45:00',100,'Creatine poeder voldoende'),(35,8,1,'2024-05-23 10:50:00',300,'Water gepompt'),(36,6,1,'2024-05-23 10:55:00',50,'Proteïne poeder bediend'),(37,6,1,'2024-05-23 11:00:00',30,'Creatine poeder bediend'),(38,9,1,'2024-05-23 11:05:00',1,'Machine aangezet'),(39,10,1,'2024-05-23 11:10:00',1,'LCD scherm bestuurd'),(40,10,1,'2024-05-23 11:15:00',1,'Shake gemaakt'),(41,1,1,'2024-05-23 11:20:00',0,'Geen fles onder machine'),(42,2,1,'2024-05-23 11:25:00',10,'Weinig water beschikbaar'),(43,3,1,'2024-05-23 11:30:00',150,'Proteïne poeder bijna op'),(44,4,1,'2024-05-23 11:35:00',80,'Creatine poeder bijna op'),(45,8,1,'2024-05-23 11:40:00',250,'Water bijna op'),(46,6,1,'2024-05-23 11:45:00',40,'Beetje proteïne poeder gebruikt'),(47,6,1,'2024-05-23 11:50:00',20,'Beetje creatine poeder gebruikt'),(48,9,1,'2024-05-23 11:55:00',0,'Machine uitgezet'),(49,10,1,'2024-05-23 12:00:00',0,'LCD scherm uitgezet'),(50,1,1,'2024-05-23 12:05:00',0,'Geen fles onder machine');
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-30 11:05:12
