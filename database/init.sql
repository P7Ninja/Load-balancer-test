-- Mealplan Service
CREATE DATABASE mealplan;
USE mealplan;

CREATE TABLE mealplan (
   planID INT NOT NULL AUTO_INCREMENT,
   userID INT DEFAULT NULL,
   startDate datetime DEFAULT NULL,
   endDate datetime DEFAULT NULL,
   PRIMARY KEY (planID)
);

CREATE TABLE mealsperday (
   id INT NOT NULL AUTO_INCREMENT,
   planID INT DEFAULT NULL,
   meals INT DEFAULT NULL,
   totalCalories DOUBLE DEFAULT NULL,
   totalProtein DOUBLE DEFAULT NULL,
   totalCarbohydrates DOUBLE DEFAULT NULL,
   totalFat DOUBLE DEFAULT NULL,
   PRIMARY KEY (id),
   KEY planID (planID),
   CONSTRAINT mealsperday_ibfk_1 FOREIGN KEY (planID) REFERENCES mealplan (planID) ON DELETE CASCADE
);


CREATE TABLE mealplanrecipes (
   id INT NOT NULL AUTO_INCREMENT,
   planID INT DEFAULT NULL,
   recipeID INT DEFAULT NULL,
   PRIMARY KEY (id),
   KEY planID (planID),
   CONSTRAINT mealplanrecipes_ibfk_1 FOREIGN KEY (planID) REFERENCES mealplan (planID) ON DELETE CASCADE
);

-- User Service
CREATE DATABASE users;
USE users;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    birthday DATE NOT NULL,
    calories DOUBLE NOT NULL,
    fat DOUBLE NOT NULL,
    carbohydrates DOUBLE NOT NULL,
    protein DOUBLE NOT NULL,
    PRIMARY KEY (id)
);

-- Recipe Service
CREATE DATABASE recipes;
USE recipes;

CREATE TABLE recipes (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    servings INT NOT NULL,
    instructions TEXT,
    url VARCHAR(255) UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE energy (
    id INT NOT NULL AUTO_INCREMENT,
    calories DOUBLE NOT NULL,
    fat DOUBLE NOT NULL,
    protein DOUBLE NOT NULL,
    carbohydrates DOUBLE NOT NULL,
    recipe_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY fk_energy_recipe_id (recipe_id) REFERENCES recipes (id)
);

CREATE TABLE items (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE units (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE ingredients (
    id INT NOT NULL AUTO_INCREMENT,
    amount DOUBLE NOT NULL,
    unit_id INT,
    item_id INT,
    recipe_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY fk_ingredients_unit_id (unit_id) REFERENCES units (id),
    FOREIGN KEY fk_ingredients_item_id (item_id) REFERENCES items (id),
    FOREIGN KEY fk_ingredients_recipe_id (recipe_id) REFERENCES recipes (id)
);

CREATE TABLE tags (
    id INT NOT NULL AUTO_INCREMENT,
    tag VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE recipe_tag_association (
    recipe_id INT,
    tag_id INT,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY fk_recipe_tag_association_recipe_id (recipe_id) REFERENCES recipes (id),
    FOREIGN KEY fk_recipe_tag_association_tag_id (tag_id) REFERENCES tags (id)
);

-- Health Service
CREATE DATABASE health;
USE health;

CREATE TABLE healthLog (
    id INT NOT NULL AUTO_INCREMENT,
    userID INT,
    dateStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    height DOUBLE,
    weight DOUBLE,
    fatPercentage DOUBLE,
    musclePercentage DOUBLE,
    waterPercentage DOUBLE,
    PRIMARY KEY (id)
);

-- Inventory Service
CREATE DATABASE inventory;
USE inventory;

CREATE TABLE Inventories (
    Id INT NOT NULL AUTO_INCREMENT,
    UserId INT NOT NULL,
    Name VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Inventories PRIMARY KEY (Id)
);

CREATE TABLE InventoryItems (
    Id INT NOT NULL AUTO_INCREMENT,
    FoodId INT NOT NULL,
    ExpirationDate DATETIME NOT NULL,
    Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    InventoryId INT NULL,
    CONSTRAINT PK_InventoryItems PRIMARY KEY (Id),
    CONSTRAINT FK_InventoryItems_Inventories_InventoryId FOREIGN KEY (InventoryId) REFERENCES Inventories (Id)
);

-- Food Service
CREATE DATABASE food;
USE food;

CREATE TABLE Foods (
    Id INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Price REAL NOT NULL,
    PriceKg REAL NOT NULL,
    Discount REAL NOT NULL,
    Vendor VARCHAR(255) NOT NULL,
    Category VARCHAR(255) NOT NULL,
    Fat REAL NOT NULL,
    Carbs REAL NOT NULL,
    Protein REAL NOT NULL,
    Cal REAL NOT NULL,
    CONSTRAINT PK_Foods PRIMARY KEY (Id)
);
