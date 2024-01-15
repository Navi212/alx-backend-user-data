#!/usr/bin/env python3
"""
The `filtered_logger` supplies a class `RedactingFormatter`
that inherits from `logging.Formatter`.
It also supplies other methods that implements custom formatting
"""
import os
import logging
import mysql.connector
import re
from typing import List, Tuple


PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filter_datum:   A function that formats a string with
                    a specified seperator

    Args:
    fields:         A list of strings to redact
    redaction:      A string to be used for redaction
    message:        A string to format
    seperator:      A string to be used as seperator

    Return:
    str:            A formatted string
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format:     A method that accepts a record arg
                    and formats it with the format method
                    of the parent class `logging.Formatter`

        Args:
        record:     A log record being a dictionary

        Return:
        str:        A formatted string
        """
        log = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    get_logger:     A function that takes no argument and
                    returns a logger object

    Return:
    logging.Logger: A logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db:     A function that connects to a secured database
                and returns a connector to the database

    Return:
    mysql.connector.connection.MySQLConnection: connector object
    """
    connector = mysql.connector.connect(
            user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
            password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
            host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
            database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return connector


def main() -> None:
    """
    main:   A function that queries the `user` table and returns
            a formatted output.

    Return:
    None
    """
    db_connection = get_db()
    logger = get_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        msg = (f"name={row[0]}; "
               f"email={row[1]}; "
               f"phone={row[2]}; "
               f"ssn={row[3]}; "
               f"password={row[4]}; "
               f"ip={row[5]}; "
               f"last_login={row[6]}; "
               f"user_agent={row[7]}")
        logger.info(msg)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
