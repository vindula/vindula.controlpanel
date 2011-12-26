SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `myvindulaDB` DEFAULT CHARACTER SET latin1 ;
USE `myvindulaDB` ;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_controlpanel_company_information`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_controlpanel_company_information` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_controlpanel_company_information` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `short_name` VARCHAR(45) NOT NULL ,
  `corporate_name` VARCHAR(45) NOT NULL ,
  `cnpj` VARCHAR(45) NOT NULL ,
  `phone_number` VARCHAR(45) NULL ,
  `address` VARCHAR(45) NULL ,
  `date_creation` DATETIME NOT NULL ,
  `city` VARCHAR(45) NULL ,
  `stade` VARCHAR(45) NULL ,
  `postal_code` VARCHAR(45) NULL ,
  `email` VARCHAR(45) NULL ,
  `website` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
