"""Script which generates an html report of the day before's data"""

from os import _Environ, environ

from dotenv import load_dotenv
from redshift_connector import connect
from redshift_connector.core import Connection

def handler(event=None, context=None) -> dict:
    """Handler for the lambda function"""
    con = get_database_connection(environ)

    report_dict = {'values_of_transaction': {
        'total': load_total_value_of_transactions(con),
        'trucks': load_value_for_each_truck(con)
    },
            'number_of_transactions': {
        'total': load_total_number_of_transactions(con),
        'trucks': load_transaction_for_each_truck(con)
    }}

    return {'html_string': convert_to_html(report_dict)}

def get_database_connection(config: _Environ) -> Connection:
    """Returns a database connection."""
    return connect(
        host=config["DB_HOST"],
        database=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        port=config["DB_PORT"]
    )

def get_number_of_trucks(con: Connection) -> int:
    """Retrieves the number of trucks being used"""
    with con.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM cai_schema.truck;")
        return cur.fetchall()[0][0]


def load_total_value_of_transactions(con: Connection) -> dict:
    """Loads the value for the total value of every transaction"""
    with con.cursor() as cur:
        cur.execute("""SELECT SUM(total)
                    FROM cai_schema.transaction 
                    WHERE EXTRACT(DAY FROM at) = EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 1;""")
        return cur.fetchall()[0][0]

def load_total_number_of_transactions(con: Connection) -> dict:
    """Loads the value for the count of transactions"""
    with con.cursor() as cur:
        cur.execute("""SELECT COUNT(*)
                    FROM cai_schema.transaction 
                    WHERE EXTRACT(DAY FROM at) = EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 1;""")
        return cur.fetchall()[0][0]

def load_value_for_each_truck(con: Connection) -> dict:
    """Loads the transaction value for each separate truck"""
    trucks_dict = {}
    trucks = get_number_of_trucks(conn)

    with con.cursor() as cur:
        for i in range(trucks):
            cur.execute(f"""SELECT SUM(total)
                        FROM cai_schema.transaction 
                        WHERE truck_id = {i+1} 
                        AND EXTRACT(DAY FROM at) = EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 1;""")
            trucks_dict[i+1] = cur.fetchall()[0][0]

        return trucks_dict

def load_transaction_for_each_truck(con: Connection) -> dict:
    """Loads the number of transactions for each separate truck"""
    trucks_dict = {}
    trucks = get_number_of_trucks(con)

    with con.cursor() as cur:
        for i in range(trucks):
            cur.execute(f"""SELECT COUNT(*)
                        FROM cai_schema.transaction 
                        WHERE truck_id = {i+1} 
                        AND EXTRACT(DAY FROM at) = EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 1;""")
            trucks_dict[i+1] = cur.fetchall()[0][0]

        return trucks_dict

def convert_to_html(report_dict: dict):
    """Converts the report dictionary into HTML"""
    html_string = f"""
    <h1>Tasty Truck Treats Report</h1>
    <h2>Number of Transactions</h2>
    <p>Total: {report_dict['number_of_transactions']['total']}</p>
    <ul>
    <li>Truck 1: {report_dict['number_of_transactions']['trucks'][1]}</li>
    <li>Truck 2: {report_dict['number_of_transactions']['trucks'][2]}</li>
    <li>Truck 3: {report_dict['number_of_transactions']['trucks'][3]}</li>
    <li>Truck 4: {report_dict['number_of_transactions']['trucks'][4]}</li>
    <li>Truck 5: {report_dict['number_of_transactions']['trucks'][5]}</li>
    <li>Truck 6: {report_dict['number_of_transactions']['trucks'][6]}</li>
    </ul>
    <h2>Value of Transactions</h2>
    <p>Total: £{report_dict['values_of_transaction']['total'] / 100}</p>
    <ul>
    <li>Truck 1: £{report_dict['values_of_transaction']['trucks'][1] / 100}</li>
    <li>Truck 2: £{report_dict['values_of_transaction']['trucks'][2] / 100}</li>
    <li>Truck 3: £{report_dict['values_of_transaction']['trucks'][3] / 100}</li>
    <li>Truck 4: £{report_dict['values_of_transaction']['trucks'][4] / 100}</li>
    <li>Truck 5: £{report_dict['values_of_transaction']['trucks'][5] / 100}</li>
    <li>Truck 6: £{report_dict['values_of_transaction']['trucks'][6] / 100}</li>
    """

    return html_string

if __name__ == "__main__":
    load_dotenv()

    conn = get_database_connection(environ)

    report = {'values_of_transaction': {
        'total': load_total_value_of_transactions(conn),
        'trucks': load_value_for_each_truck(conn)
    },
            'number_of_transactions': {
        'total': load_total_number_of_transactions(conn),
        'trucks': load_transaction_for_each_truck(conn)
    }}
