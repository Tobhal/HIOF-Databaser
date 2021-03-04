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
  `CompanyTypeName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`CompanyTypeID`),
  UNIQUE INDEX `CompanyType_UNIQUE` (`CompanyTypeName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`AreaServed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`AreaServed` (
  `AreaServedID` INT NOT NULL AUTO_INCREMENT,
  `AreaServed` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`AreaServedID`),
  UNIQUE INDEX `AreaServed_UNIQUE` (`AreaServed` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Companies` (
  `CompanyID` INT NOT NULL AUTO_INCREMENT,
  `CompanyName` VARCHAR(45) NOT NULL,
  `Founded` DATE NOT NULL,
  `HeadQuarters` VARCHAR(200) NOT NULL,
  `NumberOfEmployees` INT NULL,
  `ParentCompany` VARCHAR(500) NULL,
  `Website` VARCHAR(100) NULL,
  `CompanyType_CompanyTypeID` INT NULL,
  `AreaServed_AreaServedID` INT NULL,
  PRIMARY KEY (`CompanyID`),
  INDEX `fk_Companies_CompanyType1_idx` (`CompanyType_CompanyTypeID` ASC) VISIBLE,
  INDEX `fk_Companies_AreaServed1_idx` (`AreaServed_AreaServedID` ASC) VISIBLE,
  UNIQUE INDEX `CompanyName_UNIQUE` (`CompanyName` ASC) VISIBLE,
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
  `GameTypeName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`GameTypeID`),
  UNIQUE INDEX `GameType_UNIQUE` (`GameTypeName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CompanyRoles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompanyRoles` (
  `CompanyRoleID` INT NOT NULL AUTO_INCREMENT,
  `CompanyRoleName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`CompanyRoleID`),
  UNIQUE INDEX `CompanyRole_UNIQUE` (`CompanyRoleName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ControllerSupportType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ControllerSupportType` (
  `ControllerSupportTypeID` INT NOT NULL AUTO_INCREMENT,
  `SupportType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ControllerSupportTypeID`),
  UNIQUE INDEX `SupportType_UNIQUE` (`SupportType` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Games` (
  `GameID` INT NOT NULL,
  `Name` VARCHAR(100) NOT NULL,
  `Price` DECIMAL(4,1) NULL,
  `Metacritic` INT NULL,
  `Recommendations` INT NULL,
  `NumDLC` INT NULL,
  `ReleaceDate` DATE NULL,
  `ControllerSupportType_ControllerSupportTypeID` INT NOT NULL,
  `GameType_GameTypeID` INT NOT NULL,
  PRIMARY KEY (`GameID`),
  INDEX `fk_Games_ControllerSupportType1_idx` (`ControllerSupportType_ControllerSupportTypeID` ASC) VISIBLE,
  INDEX `fk_Games_GameType1_idx` (`GameType_GameTypeID` ASC) VISIBLE,
  UNIQUE INDEX `GameID_UNIQUE` (`GameID` ASC) VISIBLE,
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC) VISIBLE,
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
-- Table `mydb`.`GameCompany`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GameCompany` (
  `Games_GameID` INT NOT NULL,
  `Companies_CompanyID` INT NOT NULL,
  `CompanyRole_CompanyRoleID` INT NOT NULL,
  PRIMARY KEY (`Games_GameID`, `Companies_CompanyID`, `CompanyRole_CompanyRoleID`),
  INDEX `fk_Publisher_Companies1_idx` (`Companies_CompanyID` ASC) VISIBLE,
  INDEX `fk_Company_CompanyRole1_idx` (`CompanyRole_CompanyRoleID` ASC) VISIBLE,
  INDEX `fk_Company_Games1_idx` (`Games_GameID` ASC) VISIBLE,
  CONSTRAINT `fk_Publisher_Companies1`
    FOREIGN KEY (`Companies_CompanyID`)
    REFERENCES `mydb`.`Companies` (`CompanyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Company_CompanyRole1`
    FOREIGN KEY (`CompanyRole_CompanyRoleID`)
    REFERENCES `mydb`.`CompanyRoles` (`CompanyRoleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Company_Games1`
    FOREIGN KEY (`Games_GameID`)
    REFERENCES `mydb`.`Games` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Platform`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Platform` (
  `PlatformID` INT NOT NULL AUTO_INCREMENT,
  `PlatformName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`PlatformID`),
  UNIQUE INDEX `PlatformName_UNIQUE` (`PlatformName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Platforms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Platforms` (
  `Games_GameID` INT NOT NULL,
  `Platform_PlatformID` INT NOT NULL,
  INDEX `fk_Platforms_Games1_idx` (`Games_GameID` ASC) VISIBLE,
  INDEX `fk_Platforms_Platform1_idx` (`Platform_PlatformID` ASC) VISIBLE,
  CONSTRAINT `fk_Platforms_Games1`
    FOREIGN KEY (`Games_GameID`)
    REFERENCES `mydb`.`Games` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Platforms_Platform1`
    FOREIGN KEY (`Platform_PlatformID`)
    REFERENCES `mydb`.`Platform` (`PlatformID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Category` (
  `CategoryID` INT NOT NULL AUTO_INCREMENT,
  `CategoryName` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `CategoryName_UNIQUE` (`CategoryName` ASC) VISIBLE,
  PRIMARY KEY (`CategoryID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Categories` (
  `Games_GameID` INT NOT NULL,
  `Category_CategoryID` INT NOT NULL,
  INDEX `fk_Categories_Games1_idx` (`Games_GameID` ASC) VISIBLE,
  INDEX `fk_Categories_Category1_idx` (`Category_CategoryID` ASC) VISIBLE,
  CONSTRAINT `fk_Categories_Games1`
    FOREIGN KEY (`Games_GameID`)
    REFERENCES `mydb`.`Games` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Categories_Category1`
    FOREIGN KEY (`Category_CategoryID`)
    REFERENCES `mydb`.`Category` (`CategoryID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Industry`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Industry` (
  `IndustryID` INT NOT NULL AUTO_INCREMENT,
  `IndustryName` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `IndustryID_UNIQUE` (`IndustryName` ASC) VISIBLE,
  PRIMARY KEY (`IndustryID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CompanyIndustry`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CompanyIndustry` (
  `Companies_CompanyID` INT NOT NULL,
  `Industry_IndustryID` INT NOT NULL,
  INDEX `fk_CompanyIndustry_Companies1_idx` (`Companies_CompanyID` ASC) VISIBLE,
  INDEX `fk_CompanyIndustry_Industry1_idx` (`Industry_IndustryID` ASC) VISIBLE,
  CONSTRAINT `fk_CompanyIndustry_Companies1`
    FOREIGN KEY (`Companies_CompanyID`)
    REFERENCES `mydb`.`Companies` (`CompanyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_CompanyIndustry_Industry1`
    FOREIGN KEY (`Industry_IndustryID`)
    REFERENCES `mydb`.`Industry` (`IndustryID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`People`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`People` (
  `PersonName` VARCHAR(100) NOT NULL,
  `Companies_CompanyID` INT NOT NULL,
  INDEX `fk_People_Companies1_idx` (`Companies_CompanyID` ASC) VISIBLE,
  UNIQUE INDEX `PersonName_UNIQUE` (`PersonName` ASC) VISIBLE,
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
