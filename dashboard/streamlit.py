"""A Streamlit dashboard about trucks"""

from os import environ

from dotenv import load_dotenv
import streamlit as st

from visualisations import get_transactions_bar_chart, get_payment_type_pie_chart, get_income_bar_chart, get_trucks_transaction_by_hour_line_graph, get_average_transactions_bar_chart
from database import get_database_connection, load_all_transactions, load_selected_transactions

if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection(environ)

    trucks = load_all_transactions(conn)

    st.title("T3 Trucks Dashboard")

    selected_trucks = st.sidebar.multiselect("Selected trucks", trucks['truck_id'].unique(), default=trucks['truck_id'].unique())

    if selected_trucks:
        trucks = load_selected_transactions(conn, selected_trucks)
        st.metric("Total Transaction for the week:", str(trucks['total'].count()))

        cols = st.columns(2)

        with cols[0]:
            st.altair_chart(get_transactions_bar_chart(
                trucks), use_container_width=True)
        with cols[1]:
            st.altair_chart(get_trucks_transaction_by_hour_line_graph(trucks),
                            use_container_width=True)

        st.metric("Total Income for the week:",
                str(trucks['total'].sum() / 100))

        cols_2 = st.columns(2)

        with cols_2[0]:
            st.altair_chart(get_income_bar_chart(
                trucks), use_container_width=True)

        with cols_2[1]:
            st.altair_chart(get_average_transactions_bar_chart(
                trucks), use_container_width=True)

        st.write("Payment Types:")
        st.altair_chart(get_payment_type_pie_chart(trucks))
