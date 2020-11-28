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