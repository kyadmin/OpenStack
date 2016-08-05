-- MySQL  (x86_64)
--
-- Host: Mysql-server    Database: otomat
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `report_list`
--

DROP TABLE IF EXISTS `report_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_list` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `HostName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Cpu_Utilization` decimal(6,2) unsigned zerofill DEFAULT NULL,
  `Mem_total` bigint(6) DEFAULT NULL,
  `Mem_free` bigint(6) DEFAULT NULL,
  `Mem_used` bigint(6) DEFAULT NULL,
  `Mem_percent` decimal(6,2) DEFAULT NULL,
  `Swap_total` bigint(6) DEFAULT NULL,
  `Swap_free` bigint(6) DEFAULT NULL,
  `Swap_used` bigint(6) DEFAULT NULL,
  `Swap_percent` decimal(6,2) DEFAULT NULL,
  `Disk_total` bigint(6) DEFAULT NULL,
  `Disk_used` bigint(6) DEFAULT NULL,
  `Disk_free` bigint(6) DEFAULT NULL,
  `Disk_percent` decimal(6,2) DEFAULT NULL,
  `Network_traffic_recv` bigint(6) DEFAULT NULL,
  `Network_traffic_sent` bigint(6) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


-- Dump completed on 2014-11-29 20:57:07
