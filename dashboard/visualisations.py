"Script to create the dashboard visualisations"

import pandas as pd
import altair as alt


def get_transactions_bar_chart(trucks: pd.DataFrame) -> alt.Chart:
    "Creates a bar chart to represent transactions per truck"
    transactions = trucks.groupby(['truck_id']).count(
    ).sort_values(['total'], ascending=False)
    transactions = transactions.drop(columns=['payment_type_id', 'at'])
    transactions['truck'] = transactions.index.copy()

    transactions_graph = alt.Chart(
        transactions).mark_bar().encode(x="truck", y='total', color='truck')

    return transactions_graph


def get_payment_type_pie_chart(trucks: pd.DataFrame) -> alt.Chart:
    "Creates a pie chart to show proportion of used payment types"
    payment_types = (trucks.groupby('payment_type_id').count() / trucks.count()) * 100
    payment_types['payment_type'] = payment_types.index.copy()
    payment_types = payment_types.replace(1, 'cash')
    payment_types = payment_types.replace(2, 'card')

    payment_type_chart = alt.Chart(payment_types).mark_arc().encode(
        theta='at', color="payment_type")

    return payment_type_chart


def get_income_bar_chart(trucks: pd.DataFrame) -> alt.Chart:
    "Creates a bar chart to represent income per truck"
    income = trucks.groupby('truck_id')['total'].sum().to_frame()
    income['truck'] = income.index.copy()
    income['total'] = income['total'] / 100

    income_chart = alt.Chart(income).mark_bar().encode(
        x="truck", y='total', color='truck')

    return income_chart


def get_trucks_transaction_by_hour_line_graph(trucks: pd.DataFrame) -> alt.Chart:
    "Creates a line graph to represent truck transactions per hour"
    trucks['at'] = pd.to_datetime(trucks['at'])

    trucks_by_hour = trucks.groupby(
        trucks['at'].dt.hour).at.count().to_frame()
    trucks_by_hour['hour'] = trucks_by_hour.index.copy()

    graph_by_hour = alt.Chart(trucks_by_hour).mark_line().encode(
        x="hour", y='at')

    return graph_by_hour


def get_average_transactions_bar_chart(trucks: pd.DataFrame) -> alt.Chart:
    "Creates a bar chart to represent average transactions per truck"
    avg_trucks = trucks.groupby('truck_id')['total'].mean().to_frame()
    avg_trucks['truck'] = avg_trucks.index.copy()
    avg_trucks['total'] = avg_trucks['total'] / 100

    return alt.Chart(avg_trucks).mark_bar().encode(
        x="truck", y='total', color='truck')
