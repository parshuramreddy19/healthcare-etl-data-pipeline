
import psycopg2
from getpass import getpass

try:
    password = getpass("Enter PostgreSQL password: ")

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="healthcare_db",
        user="postgres",
        password=password
    )

    print("Successfully connected to PostgreSQL!")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients;")
    result = cursor.fetchone()

    print("Total patient records:", result[0])

    cursor.close()
    connection.close()

    print("Database connection closed.")

except Exception as error:
    print("Database connection failed:", error)
