"""Script which connects the entire ETL pipeline scripts"""

from os import environ

from dotenv import load_dotenv
from boto3 import client

import extract
import transform
import load

if __name__ == "__main__":
    load_dotenv()

    con = load.get_redshift_connection()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    try:
        extract.download_truck_data_files(s3, "sigma-resources-truck")
        transform.combine_transaction_data_files()
        load.upload_transaction_data(con)
    except ValueError:
        print("No transactions available")
