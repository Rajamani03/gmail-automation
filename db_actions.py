import mysql.connector

def connect_db(host, user, password):
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    return conn

def intialise_db(conn):
    cursor = conn.cursor()

    # Create database if it doesn't exist
    database_name = "email_actions"
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))

    # Switch to the database
    conn.database = database_name

    # Create table if it doesn't exist
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS emails (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        message_id VARCHAR(255) NOT NULL,
        from_email VARCHAR(255),
        received_date DATETIME,
        subject VARCHAR(255),
        body TEXT
    )
    """
    cursor.execute(table_creation_query)

    # Close cursor and connection
    cursor.close()

def insert_email(conn, email_data):
    cursor = conn.cursor()

    # Insert values from the array into the table
    insert_query = """
    INSERT INTO emails (message_id, from_email, received_date, subject, body) 
    VALUES (%s, %s, %s, %s, %s)
    """

    for email in email_data:
        email_format = (email.message_id, email.from_id, email.received_date, email.subject, email.message)
        cursor.execute(insert_query, email_format)

    # Commit changes to the database
    conn.commit()

    # Close cursor and connection
    cursor.close()