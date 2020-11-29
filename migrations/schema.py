from sqlalchemy import create_engine, text
from os import environ

engine = create_engine(environ.get('DATABASE_URI_DEV'))

with engine.connect() as conn:
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user ;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `user` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            `username` VARCHAR(50) NOT NULL,
            `email` VARCHAR(50) NOT NULL,
            `password` VARCHAR(256) NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `username` (`username`),
            INDEX `email` (`email`)
        )
        ENGINE=InnoDB
        ;
        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user_balance ;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `user_balance` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            `user_id` INT(11) NOT NULL,
            `balance` INT(11) NOT NULL,
            `balance_achieve` INT(11) NOT NULL,
            `last_transaction_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            INDEX `user_id` (`user_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user_balance_history ;
        """
    ))

    conn.execute(text(
        """
        CREATE TABLE `user_balance_history` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            `user_balance_id` INT(11) NOT NULL,
            `balance_before` INT(11) NOT NULL,
            `balance_after` INT(11) NOT NULL,
            `activity` VARCHAR(50) NOT NULL,
            `type` ENUM('debit','credit') NOT NULL,
            `ip` VARCHAR(50) NOT NULL,
            `location` VARCHAR(100) NOT NULL,
            `user_agent` VARCHAR(50) NOT NULL,
            `author` VARCHAR(50) NOT NULL,
            `transaction_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            INDEX `user_balance_id` (`user_balance_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS bank_balance;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `bank_balance_history` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            `bank_balance_id` INT(11) NOT NULL,
            `balance_before` INT(11) NOT NULL,
            `balance_after` INT(11) NOT NULL,
            `activity` VARCHAR(50) NOT NULL,
            `type` ENUM('debit','kredit') NOT NULL,
            `ip` VARCHAR(50) NOT NULL,
            `location` VARCHAR(50) NOT NULL,
            `user_agent` VARCHAR(50) NOT NULL,
            `author` VARCHAR(50) NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `balance_bank_id` (`bank_balance_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;

        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS bank_balance_history;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `bank_balance_history` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            `balance_bank_id` INT(11) NOT NULL,
            `balance_before` INT(11) NOT NULL,
            `balance_after` INT(11) NOT NULL,
            `activity` VARCHAR(50) NOT NULL,
            `type` ENUM('debit','kredit') NOT NULL,
            `ip` VARCHAR(50) NOT NULL,
            `location` VARCHAR(50) NOT NULL,
            `user_agent` VARCHAR(50) NOT NULL,
            `author` VARCHAR(50) NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `balance_bank_id` (`balance_bank_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    ))

    print("success..")