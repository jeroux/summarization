import os
import requests
import pandas as pd
import numpy as np
import streamlit as st

from core.ml.qamodel import QABookSummerizerML


PATH = os.path.abspath(os.path.dirname(__file__))
DATAPATH = os.path.join(PATH, "data")

@st.cache
def get_book_id(books):
    selection = books[books["Title"] == title]["Text#"]
    return selection.iloc[0]

@st.cache
def get_books_data():
    books = pd.read_csv(
        os.path.join(DATAPATH, "pg_catalog.csv"),
        sep=",",
        dtype={"Text#": np.int32, "Type": "category", "Language": "category"}, low_memory=False
    )
    books = books[books["Type"] == "Text"]
    titles = books["Title"]
    titles.drop_duplicates(inplace=True)
    titles.dropna(inplace=True)
    return books, titles

books, titles = get_books_data()

st.title("Summarizer")

with st.sidebar:

    with st.form(key='my_form'):
        title = st.form.selectbox("Which book do you want?", titles)
        st.form("How many chapters do you want?", min_value=1, max_value=1000, value=1, step=1, key="nb_chapitres")
        submit_button = st.form_submit_button(label='Submit parameters')



"You selected:", title

expander = st.expander("Bert")
expander.write("Here will come the Bart summary")
expander2 = st.expander("GPT")
expander3 = st.expander("XLM")
expander4 = st.expander('FAQ')

if submit_button:
    book_id = str(get_book_id(books))
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"

    r = requests.get(url)
    fichiers = os.listdir(DATAPATH)
    if book_id + ".html" not in fichiers:
        with open(
                os.path.join(DATAPATH, book_id + ".html"), "w", encoding="utf-8"
        ) as file:
            file.write(r.text)

    summerizer_model = QABookSummerizerML(os.path.join(DATAPATH, book_id + ".html"))
    expander.write("<p align='justify'>" + summerizer_model.bert_summary + "</p>", unsafe_allow_html=True)
    expander2.write("<p align='justify'>" + summerizer_model.gpt_summary + "</p>", unsafe_allow_html=True)
    expander3.write("<p align='justify'>" + summerizer_model.xlm_summary + "</p>", unsafe_allow_html=True)
    expander4.write(summerizer_model.faq)


