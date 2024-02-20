# Food-Trucks-ETL-Pipeline
## Case Study
Tasty Truck Treats (T3) is a catering company that specializes in operating a fleet of food trucks in Lichfield and its surrounding areas. The company is dedicated to providing delicious and diverse culinary experiences to its customers. T3 takes pride in its fleet of food trucks, each of which operates semi-independently. This means that each truck has its own unique menu and style, offering a variety of delectable treats to cater to different tastes and preferences. From gourmet burgers and sandwiches to mouthwatering desserts and refreshing beverages, T3 aims to satisfy a wide range of culinary cravings.

While each food truck operates independently on a day-to-day basis, T3 collects overall sales data from each truck at the end of every month, giving an overall view of how their fleet is performing.

Collecting monthly sales data from each truck isn't giving T3 enough detail to really be a data-informed organisation. T3 would like to have an automated pipeline that regularly collects transaction-level data from every truck for central analysis. This data will allow the company to evaluate the performance of each truck, track trends, identify popular items, and make informed decisions about menu adjustments, marketing strategies, and overall fleet management.

## Functionality
This project implements an ETL pipeline that includes loading data from a data bucket, data transformation and storage in a cloud-based environment. AWS services, such as Redshift and Lambda functions, facilitate the cloud-based infrastructure, ensuring scalability and reliability.

## Pipeline Files
In the pipeline folder, you will find files required to run the pipeline.

- `extract.py`
    - This file contains the extract script which extracts data from an AWS S3 bucket.
    - This file does not need to be run independently.
- `transform.py`
    - This file contains the transform script which transforms the extracted data.
    - This file does not need to be run independently.
- `load.py`
    - This file contains the load script which loads the transformed data into an AWS redshift database.
    - This file does not need to be run independently.
- `pipeline.py`
    - This file contains the pipeline script which runs all the required functions from the extract, transform and load scripts.
    - To run this script, use "python3 pipeline.py"
- `schema.sql`
    - This file contains the schema for the tables in the database used to store the data.
- `reset.sh`
    - This file contains the shell script to clear the transaction table in the database.
    - To run this script, use "sh reset.sh"
- `Dockerfile`
    - This file contains the script to create a docker image of all the require files in this folder.

## Dashboard Files
In the dashboard folder, you will find files required to run the dashboard.
- `database.py`
    - This file contains the script which loads required data from the database.
    - This file does not need to be run independently.
- `visualisations.py`
    - This file contains the script which creates all the visualisations required for the dashboard.
    - This file does not need to be run independently.
- `streamlit.py`
    - This file contains the script which loads all the viualisations using streamlit.
    - To run this script, use "streamlit run streamlit.py".
- `wireframe.png`
    - This contains the wireframe used to plan out the dashboard.
- `Dockerfile`
    - This file contains the script to create a docker image of all the require files in this folder.

## Report Files
- `generate_report.py`
    - This file contains the script to generate a report to be send to the user through email.
    - This file does not need to be run independently and needs to be run on AWS as a Lambda function.
- `Dockerfile`
    - This file contains the script to create a docker image of all the require files in this folder.

## Installation and Requirements
It is recommended before stating any installations that you make a new virtual environment. This can be done through commands in order:
- `python3 -m venv venv `
- `source ./venv/bin/activate`

Install all requirements for the pipeline using the command:
`pip3 install -r requirements.txt `

Create a .env file in the pipeline, dashboard and report folders using the command in each folder:
`touch .env`

Required .env variables in each .env file:
- DB_NAME = The name of your database.
- DB_USER = The username to access your database.
- DB_PASSWORD = The password to access your database.
- DB_PORT = The port to access your database.
- DB_HOST = The host name or address of your database server.

- AWS_ACCESS_KEY_ID = The access key for the AWS account you want to host this pipeline on.
- AWS_SECRET_ACCESS_KEY = The secret access key for the AWS account you want to host this pipeline on.
