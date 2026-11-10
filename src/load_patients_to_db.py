import logging
import csv
import psycopg2
from pathlib import Path
from getpass import getpass

# Locate the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Locate the cleaned CSV file
CLEANED_FILE = (
    PROJECT_ROOT / "data" / "processed" / "patients_cleaned.csv"
)
# Configure pipeline logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_patients():

    connection = None

    try:
        logging.info("Healthcare ETL pipeline started")
        # Read cleaned patient data
        with open(CLEANED_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            
        logging.info("Records read from CSV: %s", len(rows))
        print(f"Records read from CSV: {len(rows)}")

        # Connect to PostgreSQL
        password = getpass("Enter PostgreSQL password: ")

        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="healthcare_db",
            user="postgres",
            password=password
        )

        cursor = connection.cursor()

        # Insert or update patient records
        query = """
            INSERT INTO patients (
                patient_id,
                first_name,
                last_name,
                date_of_birth,
                gender,
                city,
                email,
                registration_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (patient_id)
            DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                date_of_birth = EXCLUDED.date_of_birth,
                gender = EXCLUDED.gender,
                city = EXCLUDED.city,
                email = EXCLUDED.email,
                registration_date = EXCLUDED.registration_date;
        """

        values = [
            (
                row["patient_id"],
                row["first_name"],
                row["last_name"],
                row["date_of_birth"] or None,
                row["gender"] or None,
                row["city"] or None,
                row["email"] or None,
                row["registration_date"] or None
            )
            for row in rows
        ]

        cursor.executemany(query, values)
        connection.commit()

        print(f"Records processed successfully: {len(rows)}")
        logging.info("Records processed successfully: %s", len(rows))

        # Verify database record count
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_records = cursor.fetchone()[0]

        print(f"Total records in PostgreSQL: {total_records}")
        logging.info("Total records in PostgreSQL: %s", total_records)

        cursor.close()

    except Exception as error:
        if connection:
            connection.rollback()

        print("Loading failed:", error)
        logging.exception("Healthcare ETL pipeline failed")

    finally:
        if connection:
            connection.close()
            print("Database connection closed.")
            logging.info("Database connection closed.")


if __name__ == "__main__":
    load_patients()
