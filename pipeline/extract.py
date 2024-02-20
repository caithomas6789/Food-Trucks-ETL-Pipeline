"""Script to download all the required file about the T3 truck data from an S3 bucket"""
from os import environ, path, mkdir

from datetime import datetime
from dotenv import load_dotenv
from boto3 import client

CURRENT_DATETIME = datetime.now()


def get_object_keys(s3_client: client, bucket: str) -> list[str]:
    """Gets all the keys of all the objects in the bucket"""

    content = s3_client.list_objects(
        Bucket=bucket)["Contents"]

    return [o["Key"] for o in content]


def find_valid_hours() -> list[str]:
    valid_hours = []
    hour = CURRENT_DATETIME.hour

    valid_hours.append(str(hour))
    valid_hours.append(str(hour-1))
    valid_hours.append(str(hour-2))

    return valid_hours


def download_truck_data_files(s3_client: client, bucket: str):
    """Downloads relevant files from S3 to a data/ folder."""

    keys = get_object_keys(s3_client, bucket)
    valid_hours = find_valid_hours()

    for k in keys:
        key_list = k.split("/")
        if key_list[0] == "trucks" and str(CURRENT_DATETIME.year) in key_list[1] and str(CURRENT_DATETIME.month) in key_list[1] and key_list[2] == str(CURRENT_DATETIME.day) and key_list[3] in valid_hours:
            if not path.exists(f"truck_data/"):
                mkdir(f"truck_data")
            if not path.exists("truck_data/trucks"):
                mkdir("truck_data/trucks")

            s3_client.download_file(
                bucket, k, f"truck_data/trucks/{key_list[4]}")
