"""Script which loads all the cleaned truck data into Redshift"""

from os import environ

from csv import reader
import redshift_connector
from dotenv import load_dotenv


def get_redshift_connection():
    """Establishes a connection with Redshift"""
    try:
        return redshift_connector.connect(
            host=environ.get('DB_HOST'),
            database=environ.get('DB_NAME'),
            port=environ.get('DB_PORT'),
            user=environ.get('DB_USER'),
            password=environ.get('DB_PASSWORD')
        )
    except:
        print("Error connecting to database!")


def load_truck_data() -> list[list[str]]:
    """Loads the data from the .csv file and returns it as a list of lists"""

    with open("truck_data/truck.csv", 'r') as file:
        return list(reader(file))[1:]


def upload_transaction_data(con: redshift_connector):
    """Uploads transaction data to the database."""

    rows = load_truck_data()

    for row in rows:

        query = f"""
        INSERT INTO cai_schema.transaction
        (at,
        payment_type_id,
        total,truck_id) 
        VALUES ('{row[0]}', {int(row[1])}, {int(row[2])}, {int(row[3])});"""

        with con.cursor() as cur:
            cur.execute(query)

        con.commit()
