# ************************************************************
# Sequel Ace SQL dump
# Version 20029
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: 127.0.0.1 (MySQL 8.0.27)
# Database: db_kompol
# Generation Time: 2022-02-20 08:14:13 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table tbl_ahp_partai
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tbl_ahp_partai`;

CREATE TABLE `tbl_ahp_partai` (
  `ahp_partai_id` int unsigned NOT NULL AUTO_INCREMENT,
  `partai_id` int NOT NULL,
  `komunikator_jumlah_partai` double DEFAULT NULL,
  `komunikator_sentiment_partai` double DEFAULT NULL,
  `popularitas_partai` double DEFAULT NULL,
  `laporan_jumlah_partai` double DEFAULT NULL,
  `laporan_sentiment_partai` double DEFAULT NULL,
  `integritas_jumlah_partai` double DEFAULT NULL,
  `integritas_sentiment_partai` double DEFAULT NULL,
  `score` double DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`ahp_partai_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `tbl_ahp_partai` WRITE;
/*!40000 ALTER TABLE `tbl_ahp_partai` DISABLE KEYS */;

INSERT INTO `tbl_ahp_partai` (`ahp_partai_id`, `partai_id`, `komunikator_jumlah_partai`, `komunikator_sentiment_partai`, `popularitas_partai`, `laporan_jumlah_partai`, `laporan_sentiment_partai`, `integritas_jumlah_partai`, `integritas_sentiment_partai`, `score`, `created_at`, `update_at`)
VALUES
	(1,1,90,80,80,80,80,80,80,80,'2022-02-20 10:07:17',NULL),
	(2,2,100,80,50,70,90,50,60,90,'2022-02-20 10:07:17',NULL),
	(3,3,100,60,40,80,100,50,50,70,'2022-02-20 10:07:17',NULL),
	(4,4,100,70,60,80,40,10,50,60,'2022-02-20 10:07:17',NULL);

/*!40000 ALTER TABLE `tbl_ahp_partai` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
