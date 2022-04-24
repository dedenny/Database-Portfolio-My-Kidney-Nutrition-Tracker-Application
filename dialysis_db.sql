-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Patients` (
  `patient_id` INT NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(128) NOT NULL,
  `first_name` VARCHAR(128) NOT NULL,
  `age` INT NOT NULL,
  `gender` VARCHAR(20) NULL,
  `height` INT NOT NULL,
  `weight` INT NOT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE INDEX `idPatients_UNIQUE` (`patient_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Foods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Foods` (
  `food_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `phosphorous_content` INT NULL,
  `phosphorous_units` VARCHAR(32) NOT NULL,
  `sodium_content` INT NULL,
  `sodium_unit` VARCHAR(32) NOT NULL,
  `calories` INT NULL,
  `calories_unit` VARCHAR(32) NOT NULL,
  `potassium_content` INT NULL,
  `potassium_unit` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`food_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Lab_Results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Lab_Results` (
  `lab_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `phosphorus_lab` FLOAT NULL,
  `phosphorus_lab_unit` VARCHAR(32) NOT NULL,
  `potassium_lab` FLOAT NULL,
  `potassium_lab_unit` VARCHAR(32) NOT NULL,
  `sodium_lab` INT NULL,
  `sodium_lab_unit` VARCHAR(32) NOT NULL,
  `dialysis_adequacy_lab` FLOAT NULL,
  `lab_results_time` DATETIME NULL,
  `Patients_patient_id` INT NOT NULL,
  PRIMARY KEY (`lab_id`, `Patients_patient_id`),
  UNIQUE INDEX `lab_id_UNIQUE` (`lab_id` ASC) VISIBLE,
  INDEX `fk_Lab_Results_Patients1_idx` (`Patients_patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_Lab_Results_Patients1`
    FOREIGN KEY (`Patients_patient_id`)
    REFERENCES `mydb`.`Patients` (`patient_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Dialysis_Forms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Dialysis_Forms` (
  `dialysis_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `location_type` VARCHAR(128) NOT NULL,
  `adequacy_standard` FLOAT NOT NULL,
  `Lab_Results_lab_id` INT NULL,
  PRIMARY KEY (`dialysis_id`, `Lab_Results_lab_id`),
  INDEX `fk_Dialysis_Forms_Lab_Results1_idx` (`Lab_Results_lab_id` ASC) VISIBLE,
  CONSTRAINT `fk_Dialysis_Forms_Lab_Results1`
    FOREIGN KEY (`Lab_Results_lab_id`)
    REFERENCES `mydb`.`Lab_Results` (`lab_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE Dialysis_Forms (
  dialysis_id INT NOT NULL,
  name VARCHAR(128) NOT NULL,
  location_type VARCHAR(128) NOT NULL,
  adequacy_standard FLOAT NOT NULL,
  PRIMARY KEY (dialysis_id);


-- -----------------------------------------------------
-- Table `mydb`.`Patients_Food`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Patients_Food` (
  `Foods_food_id` INT UNSIGNED NOT NULL,
  `Patients_patient_id` INT NOT NULL,
  `patient_food_time` DATETIME NOT NULL,
  PRIMARY KEY (`Foods_food_id`, `Patients_patient_id`),
  INDEX `fk_Food_has_Patients_Patients1_idx` (`Patients_patient_id` ASC) VISIBLE,
  INDEX `fk_Food_has_Patients_Food_idx` (`Foods_food_id` ASC) VISIBLE,
  CONSTRAINT `fk_Food_has_Patients_Food`
    FOREIGN KEY (`Foods_food_id`)
    REFERENCES `mydb`.`Foods` (`food_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Food_has_Patients_Patients1`
    FOREIGN KEY (`Patients_patient_id`)
    REFERENCES `mydb`.`Patients` (`patient_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


insert into patients (patient_id, last_name, first_name, age,gender,height,weight) values 
('100','Smith','Arlene','55','F','64','145'),
('101','Rogers','Christopher','63','M','72','180'),
('102','Harrison','Kayla','68','F','65','125'),
('103','Jackson','Henry','74','M','75','200'),
('104','Wonders','Brenda','91','F','60','92');

INSERT INTO  lab_results (lab_id,phosphorus_lab,phosphorus_lab_unit,potassium_lab,potassium_lab_unit,
sodium_lab,sodium_lab_unit,dialysis_adequacy_lab,lab_results_time,Patients_patient_id) VALUES
('1','3.5','mg/dL','3.4','mEq/L','135','mEq/L','1.2','2022-05-07 23:22:05','3'),
('2','5.5','mg/dL','3','mEq/L','142','mEq/L','1.7','2022-05-08 18:36:10','2'),
('3','6.5','mg/dL','2.8','mEq/L','146','mEq/L','1.1','2022-05-01 20:20:06','4'),
('4','10.5','mg/dL','6.6','mEq/L','144','mEq/L','0.6','2022-05-07 18:01:55','5'),
('5','7.2','mg/dL','4.5','mEq/L','134','mEq/L','2.2','2022-05-11 10:19:25','1');

INSERT INTO dialysis_forms (dialysis_id,name,location_type,adequacy_standard) VALUES
('1','hemodialysis FMC','incenter','1.2'),
('2','peritoneal Baxter','home','1.7');
  
INSERT INTO foods (food_id, name, portion, portion_unit, phosphorus_content, phosphorus_unit, sodium_content, sodium_unit, calories, calories_unit, potassium_content, potassium_unit) VALUES
('1077','Milk,whole’,‘128’,‘grams’, ‘251’,’mg’, ‘94.6’, ‘mg’, ‘152’, ‘kcal’, ‘374’, ‘mg’),
(‘23385’,‘Beef, loin, top loin steak, ‘284’,‘grams’, ‘585’,’mg’, ‘128, ‘mg’, ‘423’, ‘kcal’, ‘801’, ‘mg’),
(‘5746’,‘Chicken, breast,‘174’,‘grams’, ‘419’,’mg’,  ‘81.8, ‘mg’, ‘275’, ‘kcal’, ‘597’, ‘mg’),
(‘1256’,‘Yogurt, Greek, nonfat,‘156’,‘grams’, ‘212’,’mg’,  ’56.2, ‘mg’, ‘92’, ‘kcal’, ‘348’, ‘mg’),
(‘11233’,‘Kale,‘100’,‘grams’, ‘55’,’mg’,  ‘53, ‘mg’, ‘43’, ‘kcal’, ‘348’, ‘mg’);
 
INSERT INTO patients_food (foods_food_id, patients_patient_id, patient_food_time) VALUES
(‘1077’,‘100’, ‘2022-05-10 15:40:11’),
(‘23385’,‘101’, ‘2022-05-20 18:32:04’),
(‘5746’,‘102’, ‘2022-05-15 12:08:12’),
(‘1256’,‘103’, ‘2022-05-11 15:07:55’),
(‘11233’,‘104’, ‘2022-05-16 10:22:28’);

