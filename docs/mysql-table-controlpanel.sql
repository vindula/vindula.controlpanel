SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `myvindulaDB` DEFAULT CHARACTER SET latin1 ;
USE `myvindulaDB` ;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_controlpanel_company_information`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_controlpanel_company_information` ;

CREATE TABLE  `myvindulaDB`.`vin_controlpanel_company_information` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(45) NOT NULL,
  `corporate_name` varchar(45) NOT NULL,
  `cnpj` varchar(45) NOT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `date_creation` datetime NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `stade` varchar(45) DEFAULT NULL,
  `postal_code` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `website` varchar(45) DEFAULT NULL,
  `logo_corporate` longblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_controlpanel_products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_controlpanel_products` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_controlpanel_products` (
  `id` INT NOT NULL  AUTO_INCREMENT ,
  `name` VARCHAR(45) NULL ,
  `title` VARCHAR(45) NULL ,
  `active` TINYINT(1)  NULL ,
  `installed` TINYINT(1)  NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
