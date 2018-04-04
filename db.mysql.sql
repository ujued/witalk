use uoope_tech;
-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: uoope.com    Database: uoope_tech
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.26-MariaDB-0+deb9u1

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
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `forum_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES (1,1,0)
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(800) COLLATE utf8mb4_unicode_ci NOT NULL,
  `author_id` int(11) NOT NULL,
  `post_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `topic_id` int(11) NOT NULL,
  `user_agent` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer_trash`
--

DROP TABLE IF EXISTS `answer_trash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer_trash` (
  `id` int(11) NOT NULL,
  `content` varchar(800) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `topic_id` int(11) DEFAULT NULL,
  `user_agent` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_trash`
--

LOCK TABLES `answer_trash` WRITE;
/*!40000 ALTER TABLE `answer_trash` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer_trash` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `append_topic`
--

DROP TABLE IF EXISTS `append_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `append_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `append_content` text,
  `topic_id` int(11) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `append_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `append_topic`
--

LOCK TABLES `append_topic` WRITE;
/*!40000 ALTER TABLE `append_topic` DISABLE KEYS */;
/*!40000 ALTER TABLE `append_topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bag`
--

DROP TABLE IF EXISTS `bag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `goods_name` varchar(45) DEFAULT NULL,
  `goods_id` varchar(45) DEFAULT NULL,
  `pack_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bag`
--

LOCK TABLES `bag` WRITE;
/*!40000 ALTER TABLE `bag` DISABLE KEYS */;
/*!40000 ALTER TABLE `bag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `trade` int(11) DEFAULT NULL,
  `trade_info` varchar(255) DEFAULT NULL,
  `trade_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collection`
--

DROP TABLE IF EXISTS `collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `collect_id` int(11) DEFAULT NULL,
  `collect_cate` char(1) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `collect_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collection`
--

LOCK TABLES `collection` WRITE;
/*!40000 ALTER TABLE `collection` DISABLE KEYS */;
/*!40000 ALTER TABLE `collection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum`
--

DROP TABLE IF EXISTS `forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum`
--

LOCK TABLES `forum` WRITE;
/*!40000 ALTER TABLE `forum` DISABLE KEYS */;
INSERT INTO `forum` VALUES (1,'轻松问答','为领域新手设置的版块，某技术领域不懂的问题到这里提问，没有成见，摒弃羞涩，“树叶”有专攻。来，率性问吧！你一定可以得到满意答案。','2018-02-14 21:35:15'),(2,'程序员',NULL,'2018-02-17 22:00:32'),(3,'Java',NULL,'2018-02-23 11:32:42'),(4,'Python',NULL,'2018-02-23 11:32:43'),(5,'C/C++',NULL,'2018-02-23 11:32:44'),(6,'Golang',NULL,'2018-02-23 11:32:45'),(7,'Lisp',NULL,'2018-02-23 11:32:46'),(8,'C#',NULL,'2018-02-23 11:32:47'),(9,'Perl',NULL,'2018-02-23 11:32:48'),(10,'Javascript',NULL,'2018-02-23 11:32:49'),(11,'Linux',NULL,'2018-02-23 11:32:50'),(12,'分布式',NULL,'2018-02-23 11:32:51'),(13,'网络',NULL,'2018-02-23 11:32:52'),(14,'二手市场','这里提供网路交易意向信息。原则上WITALK不介入交易，请大家注意鉴别信息真伪，<a href=\"/new/50\">点击这里</a>曝光歹徒非法行径。<br />纷繁复杂的陌生网络世界，诚信难能可贵，且行且珍惜。','2018-02-23 11:32:53'),(15,'网购信息',NULL,'2018-02-23 11:32:54'),(16,'杂谈灌水',NULL,'2018-02-23 13:05:08'),(17,'Spring',NULL,'2018-02-23 13:14:18'),(18,'Struts2',NULL,'2018-02-23 13:14:19'),(19,'Mybatis',NULL,'2018-02-23 13:14:20'),(20,'Hibernate',NULL,'2018-02-23 13:14:20'),(21,'Flask',NULL,'2018-02-23 13:14:21'),(22,'Node.js',NULL,'2018-02-23 13:14:22'),(23,'MVC',NULL,'2018-02-23 13:14:22'),(24,'HTML5',NULL,'2018-02-23 13:14:23'),(25,'区块链',NULL,'2018-02-23 13:14:49'),(26,'MySQL',NULL,'2018-02-23 13:17:29'),(27,'Redis',NULL,'2018-02-23 13:17:30'),(28,'大数据',NULL,'2018-02-23 13:17:31'),(29,'心理学',NULL,'2018-02-23 13:19:22'),(30,'PHP',NULL,'2018-02-24 12:18:55'),(31,'Gradle',NULL,'2018-02-24 14:40:59'),(32,'Maven',NULL,'2018-02-24 14:41:00'),(33,'电影',NULL,'2018-02-26 21:44:14'),(34,'音乐',NULL,'2018-02-26 21:44:15'),(35,'WITALK',NULL,'2018-02-26 21:44:16'),(36,'面试',NULL,'2018-02-26 22:00:49'),(37,'脑洞时刻',NULL,'2018-02-26 22:00:50'),(38,'读书',NULL,'2018-02-26 22:00:50'),(39,'Android',NULL,'2018-03-01 11:08:50'),(40,'Apple',NULL,'2018-03-01 11:08:50'),(41,'Google',NULL,'2018-03-01 11:08:51'),(42,'共享单车',NULL,'2018-03-02 17:05:24'),(43,'恋爱',NULL,'2018-03-02 17:05:24'),(44,'二次元',NULL,'2018-03-18 20:56:19'),(45,'Nginx',NULL,'2018-03-27 17:51:05'),(46,'Vue.js',NULL,'2018-03-27 17:51:06'),(47,'正则表达式',NULL,'2018-03-27 18:06:57'),(48,'Lua',NULL,'2018-03-28 17:42:47'),(49,'游戏开发',NULL,'2018-03-28 17:44:05'),(50,'事实真相',NULL,'2018-03-29 10:37:56'),(51,'文学',NULL,'2018-03-30 22:34:51');
/*!40000 ALTER TABLE `forum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `send_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `readed` smallint(1) DEFAULT '0',
  `first_del_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `upload_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `size` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signin_record`
--

DROP TABLE IF EXISTS `signin_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signin_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `endless_days` int(11) DEFAULT '1',
  `max_days` int(11) DEFAULT '1',
  `last_signin_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signin_record`
--

LOCK TABLES `signin_record` WRITE;
/*!40000 ALTER TABLE `signin_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `signin_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `author_id` int(11) NOT NULL,
  `forum_id` int(11) NOT NULL,
  `post_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `price` int(11) DEFAULT '0',
  `view_count` int(11) DEFAULT '0',
  `user_agent` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,'你的WITALK社区成功启动啦！','',1,1,'2018-02-17 22:04:07',0,1,NULL)
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_trash`
--

DROP TABLE IF EXISTS `topic_trash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_trash` (
  `id` int(11) NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `content` text,
  `author_id` int(11) DEFAULT NULL,
  `forum_id` int(11) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `view_count` int(11) DEFAULT NULL,
  `user_agent` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_trash`
--

LOCK TABLES `topic_trash` WRITE;
/*!40000 ALTER TABLE `topic_trash` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_trash` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `password` char(32) NOT NULL,
  `email` varchar(120) NOT NULL,
  `register_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `gender` char(1) DEFAULT 'M',
  `age` smallint(6) DEFAULT '18',
  `points` int(11) DEFAULT '10',
  `avatar` varchar(225) DEFAULT 'https://uoope.com/r/uoope_tech/avatar.png',
  `signature` varchar(255) DEFAULT NULL,
  `my_page` varchar(255) DEFAULT NULL,
  `github_name` varchar(45) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `referee` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','e10adc3949ba59abbe56e057f20f883e','ujued@uoope.com','2018-02-17 22:04:07','M',23,92,'https://witalk.cc/r/avatar/hya.png','虽不能行万里路，但也要读万卷书。','https://uoope.com','ujued','济南',NULL)
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-03 17:58:22
