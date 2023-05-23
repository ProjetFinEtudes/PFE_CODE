CREATE DATABASE IF NOT EXISTS recsys;
USE recsys;

CREATE TABLE IF NOT EXISTS auth(
    uid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user(
    uid INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    genre CHAR(1) NOT NULL,
    FOREIGN KEY (uid) REFERENCES auth(uid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS ingredients;
CREATE TABLE ingredients(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes(
    id int NOT NULL,
    name varchar(255) NOT NULL,
    minutes int DEFAULT NULL,
    contributor_id int DEFAULT NULL,
    submitted date DEFAULT NULL,
    description text,
    n_steps int DEFAULT NULL,
    nutrition varchar(255) DEFAULT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS steps;
CREATE TABLE steps(
    id int NOT NULL AUTO_INCREMENT,
    recipe_id int NOT NULL,
    step_number int NOT NULL,
    description text,
    PRIMARY KEY (id),
    KEY recipe_id (recipe_id),
    CONSTRAINT steps_ibfk_1 FOREIGN KEY (recipe_id) REFERENCES recipes (id)
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS recipe_ingredients;
CREATE TABLE recipe_ingredients (
    recipe_id int NOT NULL,
    ingredient_id int NOT NULL,
    quantity varchar(255) DEFAULT NULL,
    PRIMARY KEY (recipe_id,ingredient_id),
    KEY ingredient_id (ingredient_id),
    CONSTRAINT recipe_ingredients_ibfk_1 FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    CONSTRAINT recipe_ingredients_ibfk_2 FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

DROP TABLE IF EXISTS recipe_steps;
CREATE TABLE recipe_steps (
    recipe_id int NOT NULL,
    step_id int NOT NULL,
    PRIMARY KEY (recipe_id,step_id),
    KEY step_id (step_id),
    CONSTRAINT recipe_steps_ibfk_1 FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    CONSTRAINT recipe_steps_ibfk_2 FOREIGN KEY (step_id) REFERENCES steps (id)
);

DROP TABLE IF EXISTS recipe_tags;
CREATE TABLE recipe_tags (
    recipe_id int NOT NULL,
    tag_id int NOT NULL,
    PRIMARY KEY (recipe_id,tag_id),
    KEY tag_id (tag_id),
    CONSTRAINT recipe_tags_ibfk_1 FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    CONSTRAINT recipe_tags_ibfk_2 FOREIGN KEY (tag_id) REFERENCES tags (id)
);




