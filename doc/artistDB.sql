SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `artistdb` ;
CREATE SCHEMA IF NOT EXISTS `artistdb` DEFAULT CHARACTER SET utf8 ;
USE `artistdb` ;

-- -----------------------------------------------------
-- Table `artistdb`.`label`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`label` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`label` (
  `ID` INT(11) NOT NULL AUTO_INCREMENT ,
  `lableName` VARCHAR(45) NULL DEFAULT NULL ,
  `lableFounder` VARCHAR(45) NULL DEFAULT NULL ,
  `dateFounded` DATE NULL DEFAULT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`album`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`album` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`album` (
  `ID` INT(11) NOT NULL AUTO_INCREMENT ,
  `lableID` INT(11) NULL ,
  `title` VARCHAR(45) NULL DEFAULT NULL ,
  `releaseDate` DATE NULL DEFAULT NULL ,
  `numberOfTracks` INT(11) NULL DEFAULT NULL ,
  `numSold` INT(11) NULL DEFAULT NULL ,
  `imageLocation` VARCHAR(1200) NULL DEFAULT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ALB_LABEL1` (`lableID` ASC) ,
  CONSTRAINT `fk_ALBUM_LABEL1`
    FOREIGN KEY (`lableID` )
    REFERENCES `artistdb`.`label` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`location`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`location` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`location` (
  `ID` INT(11) NOT NULL ,
  `city` VARCHAR(45) NULL DEFAULT NULL ,
  `state` VARCHAR(45) NULL DEFAULT NULL ,
  `country` VARCHAR(45) NULL DEFAULT NULL ,
  `imageLocation` VARCHAR(1200) NULL DEFAULT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`artist` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`artist` (
  `ID` INT(11) NOT NULL AUTO_INCREMENT ,
  `stageName` VARCHAR(45) NULL DEFAULT NULL ,
  `name` VARCHAR(75) NULL DEFAULT NULL ,
  `imageLocation` VARCHAR(1200) NULL DEFAULT NULL ,
  `locationID` INT(11) NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ARTIST_LOCATION1` (`locationID` ASC) ,
  CONSTRAINT `fk_ARTIST_LOCATION1`
    FOREIGN KEY (`locationID` )
    REFERENCES `artistdb`.`location` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`album_artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`album_artist` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`album_artist` (
  `artistID` INT(11) NOT NULL ,
  `albumID` INT(11) NOT NULL ,
  PRIMARY KEY (`artistID`, `albumID`) ,
  INDEX `fk_ARTIST_ALBUM_ind` (`albumID` ASC) ,
  CONSTRAINT `fk_ALBUM_ARTIST_ALBUM1`
    FOREIGN KEY (`albumID` )
    REFERENCES `artistdb`.`album` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ALBUM_ARTIST_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`genre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`genre` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`genre` (
  `ID` INT(11) NOT NULL AUTO_INCREMENT ,
  `genreName` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`artist_genre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`artist_genre` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`artist_genre` (
  `artistID` INT(11) NOT NULL ,
  `genreID` INT(11) NOT NULL ,
  PRIMARY KEY (`artistID`, `genreID`) ,
  INDEX `fk_Artist-Genre` (`genreID` ASC) ,
  CONSTRAINT `fk_Artist-Genre_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Artist-Genre_Genre1`
    FOREIGN KEY (`genreID` )
    REFERENCES `artistdb`.`genre` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`assoc_artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`assoc_artist` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`assoc_artist` (
  `artistID` INT(11) NOT NULL ,
  `assoc_ID` INT(11) NOT NULL ,
  PRIMARY KEY (`artistID`, `assoc_ID`) ,
  INDEX `fk_ARTIST_ASSOC` (`artistID` ASC, `assoc_ID` ASC) ,
  INDEX `fk_ASSOC_ARTIST_ARTIST2` (`assoc_ID` ASC) ,
  CONSTRAINT `fk_ASSOC_ARTIST_ARTIST`
    FOREIGN KEY (`artistID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ASSOC_ARTIST_ARTIST2`
    FOREIGN KEY (`assoc_ID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`tour`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`tour` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`tour` (
  `ID` INT(11) NOT NULL AUTO_INCREMENT ,
  `tourName` VARCHAR(75) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`performance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`performance` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`performance` (
  `ID` INT(11) NOT NULL ,
  `date` DATE NOT NULL ,
  `venue` VARCHAR(75) NOT NULL ,
  `tourID` INT(11) NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_Tour_Performance` (`tourID` ASC) ,
  CONSTRAINT `fk_Tour`
    FOREIGN KEY (`tourID` )
    REFERENCES `artistdb`.`tour` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`tour_artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`tour_artist` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`tour_artist` (
  `artistID` INT(11) NOT NULL ,
  `tourID` INT(11) NOT NULL ,
  PRIMARY KEY (`artistID`, `tourID`) ,
  INDEX `fk_TOUR_ARTIST_ind` (`tourID` ASC) ,
  CONSTRAINT `fk_TOUR_ARTIST_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TOUR_ARTIST_TOUR1`
    FOREIGN KEY (`tourID` )
    REFERENCES `artistdb`.`tour` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `artistdb`.`MEMBERSHIP`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `artistdb`.`MEMBERSHIP` ;

CREATE  TABLE IF NOT EXISTS `artistdb`.`MEMBERSHIP` (
  `groupID` INT(11) NOT NULL ,
  `artistID` INT(11) NOT NULL ,
  `current` TINYINT(1) NULL ,
  PRIMARY KEY (`groupID`, `artistID`) ,
  INDEX `fk_MEMBERSHIP_artist2` (`artistID` ASC) ,
  CONSTRAINT `fk_MEMBERSHIP_artist1`
    FOREIGN KEY (`groupID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MEMBERSHIP_artist2`
    FOREIGN KEY (`artistID` )
    REFERENCES `artistdb`.`artist` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
