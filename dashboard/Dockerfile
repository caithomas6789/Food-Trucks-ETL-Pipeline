FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY database.py .

COPY visualisations.py .

COPY streamlit.py .

CMD streamlit run streamlit.py