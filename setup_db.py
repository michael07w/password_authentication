import os.path
import sqlite3
from os import path
from sqlite3 import Error



def create_connection(db_file):
    """Create connection to SQLite database.

    Args:
        db_file (str): Name of database to connect to.

    Returns:
        Connection object: Connection to SQLite database.
    """
    conn = None

    try:
        # create database file or connect to existing
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn



def get_tables(conn):
    """Returns the tables in SQLite database.

    Args:
        conn (Connection object): Connection to SQLite database.

    Returns:
        List: Tables in the SQLite database.
    """
    cur = conn.cursor()
    cur.execute("""SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%';
                """)
    tables = cur.fetchall()

    return tables



def get_rows_in_users(conn):
    """Returns the number of rows in the users table.

    Args:
        conn (Connection object): Connection to SQLite database.

    Returns:
        int: Number of rows in the users table.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    num_of_rows = len(cur.fetchall())

    return num_of_rows



def create_table(conn, create_table_sql):
    """Creates table using passed SQL statement.

    Args:
        conn (Connection object): Connection to SQLite database.
        create_table_sql (str): CREATE TABLE statement.
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def delete_table(conn):
    """Deletes users table from SQLite database.

    Args:
        conn (Connection object): Connection to SQLite database.
    """
    try:
        cur = conn.cursor()
        cur.execute("DROP TABLE users;")
    except Error as e:
        print(e)



def main():
    database_name = 'ppab6.db'

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    username VARCHAR, password_hash VARCHAR
                                );"""

    # check if database exists
    if path.exists(database_name):
        # create database connection
        conn = create_connection(database_name)

        # get tables in this database
        tables = get_tables(conn)

        # get number of rows in users table
        rows_in_table = get_rows_in_users(conn)

        # ask user if they wish to erase and recreate, or use existing table
        print(
        """Database exists and contains these tables:\n{}
        \nThe users table contains {} rows.
        """.format(tables, rows_in_table)
            )
        reset_table = input("Would you like to delete/recreate table? (Y/N): ")

        # if yes, delete table and recreate
        if 'y' in reset_table.lower():
            delete_table(conn)
            create_table(conn, sql_create_users_table)

        # close database connection
        conn.close()

    else:
        # create database connection
        conn = create_connection(database_name)

        # create table
        if conn is not None:
            create_table(conn, sql_create_users_table)

            # close database connection
            conn.close()
        else:
            print("Cannot create database connection!")



if __name__ == '__main__':
    main()
