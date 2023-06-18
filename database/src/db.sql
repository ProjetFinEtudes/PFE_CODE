
CREATE DATABASE IF NOT EXISTS recsys;
USE recsys;

DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id_auth` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) UNIQUE NOT NULL,
  `password` text NOT NULL
);

DROP TABLE IF EXISTS `ingredients`;

CREATE TABLE `ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);
DROP TABLE IF EXISTS `recipe_ingredients`;

CREATE TABLE `recipe_ingredients` (
  `recipe_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `quantity` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`recipe_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`),
  CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`)
);
DROP TABLE IF EXISTS `recipe_steps`;

CREATE TABLE `recipe_steps` (
  `recipe_id` int NOT NULL,
  `step_id` int NOT NULL,
  PRIMARY KEY (`recipe_id`,`step_id`),
  KEY `step_id` (`step_id`),
  CONSTRAINT `recipe_steps_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`),
  CONSTRAINT `recipe_steps_ibfk_2` FOREIGN KEY (`step_id`) REFERENCES `steps` (`id`)
);
DROP TABLE IF EXISTS `recipe_tags`;

CREATE TABLE `recipe_tags` (
  `recipe_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`recipe_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `recipe_tags_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`),
  CONSTRAINT `recipe_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
);

DROP TABLE IF EXISTS `recipes`;

CREATE TABLE `recipes` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `minutes` int DEFAULT NULL,
  `contributor_id` int DEFAULT NULL,
  `submitted` date DEFAULT NULL,
  `description` text,
  `n_steps` int DEFAULT NULL,
  `nutrition` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `steps`;
CREATE TABLE `steps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `recipe_id` int NOT NULL,
  `step_number` int NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `recipe_id` (`recipe_id`),
  CONSTRAINT `steps_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`)
);
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birth_date` DATE NOT NULL,
  `genre` char(1) NOT NULL,
  `id_auth` INT NOT NULL,
  CONSTRAINT `fk_auth` FOREIGN KEY (`id_auth`) REFERENCES `auth`(`id_auth`)
);
DROP TABLE IF EXISTS `chatmessage`;
CREATE TABLE `chatmessage` (
  `uid` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `fromu` varchar(100) NOT NULL,
  `text` varchar(10000) NOT NULL,
  `user_uid` INT NOT NULL,
  CONSTRAINT `fk_user_uid` FOREIGN KEY (`user_uid`) REFERENCES `user`(`uid`)
);

DROP TABLE IF EXISTS `user_tags`;

CREATE TABLE `user_tags` (
  `id_user` INT NOT NULL,
  `id_tag` INT NOT NULL,
  PRIMARY KEY (`id_user`, `id_tag`),
  CONSTRAINT `user_tags_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`uid`),
  CONSTRAINT `user_tags_ibfk_2` FOREIGN KEY (`id_tag`) REFERENCES `tags` (`id`)
);