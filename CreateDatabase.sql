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
-- Table `mydb`.`CompanyType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompanyType` (
  `CompanyTypeID` INT NOT NULL AUTO_INCREMENT,
  `CompanyType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`CompanyTypeID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`AreaServed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`AreaServed` (
  `AreaServedID` INT NOT NULL AUTO_INCREMENT,
  `AreaServed` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`AreaServedID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Companies` (
  `CompanyID` INT NOT NULL AUTO_INCREMENT,
  `CompanyName` VARCHAR(45) NOT NULL,
  `Founded` DATE NOT NULL,
  `HeadQuarters` VARCHAR(45) NOT NULL,
  `NumberOfEmployees` INT NULL,
  `ParentCompany` VARCHAR(45) NULL,
  `Website` VARCHAR(45) NULL,
  `CompanyType_CompanyTypeID` INT NOT NULL,
  `AreaServed_AreaServedID` INT NOT NULL,
  PRIMARY KEY (`CompanyID`),
  INDEX `fk_Companies_CompanyType1_idx` (`CompanyType_CompanyTypeID` ASC) VISIBLE,
  INDEX `fk_Companies_AreaServed1_idx` (`AreaServed_AreaServedID` ASC) VISIBLE,
  CONSTRAINT `fk_Companies_CompanyType1`
    FOREIGN KEY (`CompanyType_CompanyTypeID`)
    REFERENCES `mydb`.`CompanyType` (`CompanyTypeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Companies_AreaServed1`
    FOREIGN KEY (`AreaServed_AreaServedID`)
    REFERENCES `mydb`.`AreaServed` (`AreaServedID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`GameType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GameType` (
  `GameTypeID` INT NOT NULL AUTO_INCREMENT,
  `GameType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`GameTypeID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CompanyRole`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompanyRole` (
  `idCompanyRole` INT NOT NULL AUTO_INCREMENT,
  `CompanyRole` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCompanyRole`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ControllerSupportType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ControllerSupportType` (
  `ControllerSupportTypeID` INT NOT NULL AUTO_INCREMENT,
  `SupportType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ControllerSupportTypeID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Games` (
  `GameID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Price` DECIMAL(2) NULL,
  `Metacritic` INT NULL,
  `Recommendations` INT NULL,
  `NumDLC` INT NULL,
  `ReleaceDate` DATE NULL,
  `ControllerSupportType_ControllerSupportTypeID` INT NOT NULL,
  `GameType_GameTypeID` INT NOT NULL,
  PRIMARY KEY (`GameID`),
  INDEX `fk_Games_ControllerSupportType1_idx` (`ControllerSupportType_ControllerSupportTypeID` ASC) VISIBLE,
  INDEX `fk_Games_GameType1_idx` (`GameType_GameTypeID` ASC) VISIBLE,
  CONSTRAINT `fk_Games_ControllerSupportType1`
    FOREIGN KEY (`ControllerSupportType_ControllerSupportTypeID`)
    REFERENCES `mydb`.`ControllerSupportType` (`ControllerSupportTypeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Games_GameType1`
    FOREIGN KEY (`GameType_GameTypeID`)
    REFERENCES `mydb`.`GameType` (`GameTypeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Company` (
  `CompanyID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Founded` DATE NULL,
  `HeadQuarters` VARCHAR(45) NULL,
  `NumberOfEmployees` INT NULL,
  `ParentCompany` VARCHAR(45) NULL,
  `Website` VARCHAR(45) NULL,
  `Type` VARCHAR(45) NULL,
  `AreaServed` VARCHAR(45) NULL,
  `People` VARCHAR(45) NULL,
  `CompanyIndustry` VARCHAR(45) NULL,
  PRIMARY KEY (`CompanyID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Platforms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Platforms` (
  `Platform` VARCHAR(45) NOT NULL,
  `Games_GameID` INT NOT NULL,
  PRIMARY KEY (`Platform`, `Games_GameID`),
  INDEX `fk_Platforms_Games1_idx` (`Games_GameID` ASC) VISIBLE,
  CONSTRAINT `fk_Platforms_Games1`
    FOREIGN KEY (`Games_GameID`)
    REFERENCES `mydb`.`Games` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Categories` (
  `Category` VARCHAR(45) NOT NULL,
  `Games_GameID` INT NOT NULL,
  PRIMARY KEY (`Category`, `Games_GameID`),
  INDEX `fk_Categories_Games1_idx` (`Games_GameID` ASC) VISIBLE,
  CONSTRAINT `fk_Categories_Games1`
    FOREIGN KEY (`Games_GameID`)
    REFERENCES `mydb`.`Games` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CompanyIndustry`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompanyIndustry` (
  `IndustryType` VARCHAR(45) NOT NULL,
  `Companies_CompanyID` INT NOT NULL,
  INDEX `fk_CompanyIndustry_Companies1_idx` (`Companies_CompanyID` ASC) VISIBLE,
  CONSTRAINT `fk_CompanyIndustry_Companies1`
    FOREIGN KEY (`Companies_CompanyID`)
    REFERENCES `mydb`.`Companies` (`CompanyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`People`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`People` (
  `PersonName` VARCHAR(45) NOT NULL,
  `Companies_CompanyID` INT NOT NULL,
  INDEX `fk_People_Companies1_idx` (`Companies_CompanyID` ASC) VISIBLE,
  CONSTRAINT `fk_People_Companies1`
    FOREIGN KEY (`Companies_CompanyID`)
    REFERENCES `mydb`.`Companies` (`CompanyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Game` (
  `GameID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Price` DECIMAL(2) NULL,
  `Metacritic` INT NULL,
  `Recommendations` INT NULL,
  `NumDLC` INT NULL,
  `ReleaceDate` DATE NULL,
  `ControllerSupport` VARCHAR(45) NULL,
  `GameType` VARCHAR(45) NULL,
  `[Categories]` VARCHAR(45) NULL,
  `[Platforms]` VARCHAR(45) NULL,
  `{Developer}` VARCHAR(45) NULL,
  `{Publisher}` VARCHAR(45) NULL,
  PRIMARY KEY (`GameID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Company` (
  `CompanyID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Founded` DATE NULL,
  `HeadQuarters` VARCHAR(45) NULL,
  `NumberOfEmployees` INT NULL,
  `ParentCompany` VARCHAR(45) NULL,
  `Website` VARCHAR(45) NULL,
  `Type` VARCHAR(45) NULL,
  `AreaServed` VARCHAR(45) NULL,
  `People` VARCHAR(45) NULL,
  `CompanyIndustry` VARCHAR(45) NULL,
  PRIMARY KEY (`CompanyID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Game` (
  `GameID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Price` DECIMAL(2) NULL,
  `Metacritic` INT NULL,
  `Recommendations` INT NULL,
  `NumDLC` INT NULL,
  `ReleaceDate` DATE NULL,
  `ControllerSupport` VARCHAR(45) NULL,
  `GameType` VARCHAR(45) NULL,
  `[Categories]` VARCHAR(45) NULL,
  `[Platforms]` VARCHAR(45) NULL,
  `{Developer}` VARCHAR(45) NULL,
  `{Publisher}` VARCHAR(45) NULL,
  PRIMARY KEY (`GameID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Game` (
  `GameID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Price` DECIMAL(2) NULL,
  `Metacritic` INT NULL,
  `Recommendations` INT NULL,
  `NumDLC` INT NULL,
  `ReleaceDate` DATE NULL,
  `ControllerSupport` VARCHAR(45) NULL,
  `GameType` VARCHAR(45) NULL,
  `[Categories]` VARCHAR(45) NULL,
  `[Platforms]` VARCHAR(45) NULL,
  `{Developer}` VARCHAR(45) NULL,
  `{Publisher}` VARCHAR(45) NULL,
  PRIMARY KEY (`GameID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
