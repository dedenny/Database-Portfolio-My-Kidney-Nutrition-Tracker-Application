-- MariaDB dump 10.19  Distrib 10.6.7-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.6.7-MariaDB

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
-- Table structure for table `dialysis_forms`
--

DROP TABLE IF EXISTS `dialysis_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dialysis_forms` (
  `dialysis_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `location_type` varchar(128) NOT NULL,
  `adequacy_standard` float NOT NULL,
  `kidney_doctor` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`dialysis_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dialysis_forms`
--

LOCK TABLES `dialysis_forms` WRITE;
/*!40000 ALTER TABLE `dialysis_forms` DISABLE KEYS */;
INSERT INTO `dialysis_forms` VALUES (1,'hemodialysis FMC','incenter',1.2,'Dr. House'),(2,'peritoneal Baxter','home',1.7,'Dr. Grey');
/*!40000 ALTER TABLE `dialysis_forms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foods`
--

DROP TABLE IF EXISTS `foods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `foods` (
  `food_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `food_name` varchar(128) NOT NULL,
  `phosphorous_content` int(11) DEFAULT NULL,
  `sodium_content` int(11) DEFAULT NULL,
  `calories` int(11) DEFAULT NULL,
  `potassium_content` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foods`
--

LOCK TABLES `foods` WRITE;
/*!40000 ALTER TABLE `foods` DISABLE KEYS */;
INSERT INTO `foods` VALUES (1,'Milk,whole',251,94,152,374,128),(2,'Beef, loin, top loin steak',585,128,423,801,284),(3,'Chicken, breast',419,81,275,597,174),(4,'Yogurt, Greek, nonfat',212,56,92,348,156),(5,'Kale',55,53,43,348,100);
/*!40000 ALTER TABLE `foods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_results`
--

DROP TABLE IF EXISTS `lab_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lab_results` (
  `lab_id` int(11) NOT NULL AUTO_INCREMENT,
  `phosphorus_lab` float DEFAULT NULL,
  `potassium_lab` float DEFAULT NULL,
  `sodium_lab` int(11) DEFAULT NULL,
  `dialysis_adequacy_lab` float DEFAULT NULL,
  `lab_results_time` datetime DEFAULT NULL,
  `Patients_patient_id` int(11) NOT NULL,
  `Dialysis_Forms_dialysis_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`lab_id`,`Patients_patient_id`,`Dialysis_Forms_dialysis_id`),
  UNIQUE KEY `lab_id_UNIQUE` (`lab_id`),
  KEY `fk_Lab_Results_Patients1_idx` (`Patients_patient_id`),
  KEY `fk_Lab_Results_Dialysis_Forms1_idx` (`Dialysis_Forms_dialysis_id`),
  CONSTRAINT `fk_Lab_Results_Dialysis_Forms1` FOREIGN KEY (`Dialysis_Forms_dialysis_id`) REFERENCES `dialysis_forms` (`dialysis_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Lab_Results_Patients1` FOREIGN KEY (`Patients_patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_results`
--

LOCK TABLES `lab_results` WRITE;
/*!40000 ALTER TABLE `lab_results` DISABLE KEYS */;
INSERT INTO `lab_results` VALUES (1,3.5,3.4,135,1.2,'2022-05-07 23:22:05',3,1),(2,5.5,3,142,1.7,'2022-05-08 18:36:10',2,2),(3,6.5,2.8,146,1.1,'2022-05-01 20:20:06',4,1),(4,10.5,6.6,144,0.6,'2022-05-07 18:01:55',5,2),(5,7.2,4.5,134,2.2,'2022-05-11 10:19:25',1,1);
/*!40000 ALTER TABLE `lab_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patients` (
  `patient_id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(128) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `height` int(11) NOT NULL,
  `weight` int(11) NOT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `idPatients_UNIQUE` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'Smith','Arlene',55,'F',64,145),(2,'Rogers','Christopher',63,'M',72,180),(3,'Harrison','Kayla',68,'F',65,125),(4,'Jackson','Henry',74,'M',75,200),(5,'Wonders','Brenda',91,'F',60,92);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_food`
--

DROP TABLE IF EXISTS `patients_food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patients_food` (
  `Foods_food_id` int(10) unsigned NOT NULL,
  `Patients_patient_id` int(11) NOT NULL,
  `patient_food_time` datetime NOT NULL,
  PRIMARY KEY (`Foods_food_id`,`Patients_patient_id`),
  KEY `fk_Food_has_Patients_Patients1_idx` (`Patients_patient_id`),
  KEY `fk_Food_has_Patients_Food_idx` (`Foods_food_id`),
  CONSTRAINT `fk_Food_has_Patients_Food` FOREIGN KEY (`Foods_food_id`) REFERENCES `foods` (`food_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_Food_has_Patients_Patients1` FOREIGN KEY (`Patients_patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_food`
--

LOCK TABLES `patients_food` WRITE;
/*!40000 ALTER TABLE `patients_food` DISABLE KEYS */;
INSERT INTO `patients_food` VALUES (1,5,'2022-05-16 10:22:28'),(2,4,'2022-05-11 15:07:55'),(3,3,'2022-05-15 12:08:12'),(4,2,'2022-05-20 18:32:04'),(5,1,'2022-05-10 15:40:11');
/*!40000 ALTER TABLE `patients_food` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-27 20:25:02
