SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `ArtistDB` DEFAULT CHARACTER SET utf8 ;
USE `ArtistDB` ;

-- -----------------------------------------------------
-- Table `ArtistDB`.`LOCATION`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`LOCATION` (
  `locationID` INT NOT NULL ,
  `city` VARCHAR(45) NULL ,
  `state` VARCHAR(45) NULL ,
  `country` VARCHAR(45) NULL ,
  `imageLocation` VARCHAR(75) NULL ,
  PRIMARY KEY (`locationID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`ARTIST`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`ARTIST` (
  `artistID` INT NOT NULL AUTO_INCREMENT ,
  `stageName` VARCHAR(45) NULL ,
  `name` VARCHAR(75) NULL ,
  `imageLocation` VARCHAR(75) NULL ,
  `LOCATION_locationID` INT NOT NULL ,
  PRIMARY KEY (`artistID`) ,
  INDEX `fk_ARTIST_LOCATION1` (`LOCATION_locationID` ASC) ,
  CONSTRAINT `fk_ARTIST_LOCATION1`
    FOREIGN KEY (`LOCATION_locationID` )
    REFERENCES `ArtistDB`.`LOCATION` (`locationID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`LABEL`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`LABEL` (
  `lableID` INT NOT NULL AUTO_INCREMENT ,
  `lableName` VARCHAR(45) NULL ,
  `lableFounder` VARCHAR(45) NULL ,
  `dateFounded` DATE NULL ,
  PRIMARY KEY (`lableID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`ALBUM`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`ALBUM` (
  `albumID` INT NOT NULL AUTO_INCREMENT ,
  `lableID` INT NOT NULL ,
  `title` VARCHAR(45) NULL ,
  `releaseDate` DATE NULL ,
  `numberOfTracks` INT NULL ,
  `numSold` INT NULL ,
  `imageLocation` VARCHAR(75) NULL ,
  PRIMARY KEY (`albumID`) ,
  INDEX `fk_ALB_LABEL1` (`lableID` ASC) ,
  CONSTRAINT `fk_ALBUM_LABEL1`
    FOREIGN KEY (`lableID` )
    REFERENCES `ArtistDB`.`LABEL` (`lableID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`ASSOC_ARTIST`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`ASSOC_ARTIST` (
  `artistID` INT NOT NULL ,
  `assoc_ID` INT NOT NULL ,
  PRIMARY KEY (`artistID`, `assoc_ID`) ,
  INDEX `fk_ARTIST_ASSOC` (`artistID` ASC, `assoc_ID` ASC) ,
  CONSTRAINT `fk_ASSOC_ARTIST_ARTIST`
    FOREIGN KEY (`artistID`)
    REFERENCES `ArtistDB`.`ARTIST` (`artistID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
CONSTRAINT `fk_ASSOC_ARTIST_ARTIST2`
    FOREIGN KEY (`assoc_ID` )
    REFERENCES `ArtistDB`.`ARTIST` (`artistID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`TOUR`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`TOUR` (
  `tourID` INT NOT NULL AUTO_INCREMENT ,
  `tourName` VARCHAR(75) NOT NULL ,
  PRIMARY KEY (`tourID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`PERFORMANCE`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`PERFORMANCE` (
  `performanceID` INT NOT NULL ,
  `date` DATE NOT NULL ,
  `venue` VARCHAR(75) NOT NULL ,
  `tourID` int NOT NULL ,
  PRIMARY KEY (`performanceID`) ,
  INDEX `fk_Tour_Performance` (`tourID` ASC) ,
  CONSTRAINT `fk_Tour`
    FOREIGN KEY (`tourID` )
    REFERENCES `ArtistDB`.`TOUR` (`tourID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`GENRE`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`GENRE` (
  `genreID` INT NOT NULL AUTO_INCREMENT ,
  `genreName` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`genreID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`ARTIST_GENRE`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`ARTIST_GENRE` (
  `artistID` INT NOT NULL ,
  `genreID` INT NOT NULL ,
  PRIMARY KEY (`artistID`, `genreID`) ,
  INDEX `fk_Artist-Genre` (`genreID` ASC) ,
  CONSTRAINT `fk_Artist-Genre_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `ArtistDB`.`ARTIST` (`artistID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Artist-Genre_Genre1`
    FOREIGN KEY (`genreID` )
    REFERENCES `ArtistDB`.`GENRE` (`genreID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`TOUR_ARTIST`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`TOUR_ARTIST` (
  `artistID` INT NOT NULL ,
  `tourID` INT NOT NULL ,
  PRIMARY KEY (`artistID`, `tourID`) ,
  INDEX `fk_TOUR_ARTIST_ind` (`tourID` ASC) ,
  CONSTRAINT `fk_TOUR_ARTIST_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `ArtistDB`.`ARTIST` (`artistID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TOUR_ARTIST_TOUR1`
    FOREIGN KEY (`tourID` )
    REFERENCES `ArtistDB`.`TOUR` (`tourID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ArtistDB`.`ALBUM_ARTIST`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ArtistDB`.`ALBUM_ARTIST` (
  `artistID` INT NOT NULL ,
  `albumID` INT NOT NULL ,
  PRIMARY KEY (`artistID`, `albumID`) ,
  INDEX `fk_ARTIST_ALBUM_ind` (`albumID` ASC) ,
  CONSTRAINT `fk_ALBUM_ARTIST_ARTIST1`
    FOREIGN KEY (`artistID` )
    REFERENCES `ArtistDB`.`ARTIST` (`artistID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ALBUM_ARTIST_ALBUM1`
    FOREIGN KEY (`albumID` )
    REFERENCES `ArtistDB`.`ALBUM` (`albumID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
