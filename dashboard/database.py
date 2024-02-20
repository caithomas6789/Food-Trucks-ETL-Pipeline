"Script to connect to the Redshift database"

from os import _Environ

from redshift_connector import connect
from redshift_connector.core import Connection
from pandas import DataFrame

def get_database_connection(config: _Environ) -> Connection:
    """Returns a database connection."""
    print("Making new database connection!")
    return connect(
        host=config["DB_HOST"],
        database=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        port=config["DB_PORT"]
    )

def load_all_transactions(conn: Connection) -> DataFrame:
    """Returns a dataframe containing all the truck transactions"""

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM cai_schema.transaction;")
        return cur.fetch_dataframe()

def load_selected_transactions(conn: Connection, selected_trucks: list[int]) -> DataFrame:
    """Returns a dataframe containing all selected truck transaction"""

    selected_trucks = tuple(selected_trucks)

    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM cai_schema.transaction WHERE truck_id IN {selected_trucks};")
        return cur.fetch_dataframe()
