"""Script which combines all the truck data into one .csv file and cleans it"""

import glob
import shutil
import pandas as pd


def clean_dataframe(df: pd.DataFrame):
    """Removes any rows in the data which contain invalid values, 
    converts the total into pennies and 
    replaces the cash and card values with their payment_type_id"""

    invalid_values = ['blank', 'NULL', "", "0",
                      "ERR", "VOID", "0.00", 'None', 0.0]

    df = df[df.total.isin(invalid_values) == False]
    df = df.dropna()
    df['total'] = (df['total'].astype(float) * 100).astype(int)
    df = df[df['total'] < 10000]
    df = df[df['total'] > 0]
    df = df.replace('cash', 1)
    df = df.replace('card', 2)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df


def combine_transaction_data_files():
    """Loads and combines relevant files from the data/ folder.

    Produces a single combined file in the data/ folder."""

    csv_files = glob.glob("./truck_data/trucks/*.csv")
    csv = []
    trucks_df = pd.DataFrame()
    count = 1

    for file in csv_files:
        single_df = pd.read_csv(file)
        single_df['truck_id'] = count
        count += 1
        csv.append(single_df)

    trucks_df = pd.concat(csv)
    trucks_df.reset_index(drop=True, inplace=True)
    shutil.rmtree('./truck_data/trucks')

    trucks_df = clean_dataframe(trucks_df)

    trucks_df.to_csv("./truck_data/truck.csv", index=False)
