-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_pinturas
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_pinturas` ;

-- -----------------------------------------------------
-- Schema esquema_pinturas
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_pinturas` DEFAULT CHARACTER SET utf8 ;
USE `esquema_pinturas` ;

-- -----------------------------------------------------
-- Table `esquema_pinturas`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_pinturas`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `apellido` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_pinturas`.`pinturas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_pinturas`.`pinturas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `autor_id` INT NOT NULL,
  `titulo` VARCHAR(255) NULL,
  `descripcion` TEXT NULL,
  `precio` FLOAT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pinturas_usuarios_idx` (`autor_id` ASC) VISIBLE,
  CONSTRAINT `fk_pinturas_usuarios`
    FOREIGN KEY (`autor_id`)
    REFERENCES `esquema_pinturas`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_pinturas`.`pinturas_favoritas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_pinturas`.`pinturas_favoritas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `pintura_id` INT NOT NULL,
  PRIMARY KEY (`id`, `usuario_id`, `pintura_id`),
  INDEX `fk_usuarios_has_pinturas_pinturas1_idx` (`pintura_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_pinturas_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_pinturas_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_pinturas`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_pinturas_pinturas1`
    FOREIGN KEY (`pintura_id`)
    REFERENCES `esquema_pinturas`.`pinturas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
