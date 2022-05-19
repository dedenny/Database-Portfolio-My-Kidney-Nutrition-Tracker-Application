-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `Patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Patients` (
  `patient_id` INT NULL AUTO_INCREMENT,
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
-- Table `Foods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Foods` (
  `food_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `food_name` VARCHAR(128) NOT NULL,
  `phosphorous_content` INT NULL,
  `sodium_content` INT NULL,
  `calories` INT NULL,
  `potassium_content` INT NULL,
  `amount` INT NULL,
  PRIMARY KEY (`food_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Lab_Results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Lab_Results` (
  `lab_id` INT NULL AUTO_INCREMENT,
  `phosphorus_lab` FLOAT NULL,
  `potassium_lab` FLOAT NULL,
  `sodium_lab` INT NULL,
  `dialysis_adequacy_lab` FLOAT NULL,
  `lab_results_time` DATETIME NULL,
  PRIMARY KEY (`lab_id`),
  UNIQUE INDEX `lab_id_UNIQUE` (`lab_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Dialysis_Forms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Dialysis_Forms` (
  `dialysis_id` INT UNSIGNED NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `location_type` VARCHAR(128) NOT NULL,
  `adequacy_standard` FLOAT NOT NULL,
  PRIMARY KEY (`dialysis_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Patients_Food`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Patients_Food` (
  `food_patient_id` INT NOT NULL,
  `Foods_food_id` INT UNSIGNED NOT NULL,
  `Patients_patient_id` INT NOT NULL,
  `patient_food_time` DATETIME NOT NULL,
  PRIMARY KEY (`food_patient_id`),
  INDEX `fk_Food_has_Patients_Patients1_idx` (`Patients_patient_id` ASC) VISIBLE,
  INDEX `fk_Food_has_Patients_Food_idx` (`Foods_food_id` ASC) VISIBLE,
  CONSTRAINT `fk_Food_has_Patients_Food`
    FOREIGN KEY (`Foods_food_id`)
    REFERENCES `Foods` (`food_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Food_has_Patients_Patients1`
    FOREIGN KEY (`Patients_patient_id`)
    REFERENCES `Patients` (`patient_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

ALTER TABLE users ADD grade_id SMALLINT UNSIGNED NOT NULL DEFAULT 0;
ALTER TABLE users ADD CONSTRAINT fk_grade_id FOREIGN KEY (grade_id) REFERENCES grades(id);
