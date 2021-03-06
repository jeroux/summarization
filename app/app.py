import os

import numpy as np
import pandas as pd
import requests
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
    return books, tuple(titles.values)


# @st.cache(hash_funcs={bs4.element.ContentMetaAttributeValue: lambda x: 10101010101})
def generate_summary(book_id):
    summerizer_model = QABookSummerizerML(os.path.join(DATAPATH, book_id + ".html"), chapters_summary_limit=slider)
    text1 = "<p align='justify'>" + summerizer_model.bert_summary + "</p>"
    text2 = "<p align='justify'>" + summerizer_model.gpt_summary + "</p>"
    text3 = "<p align='justify'>" + summerizer_model.xlm_summary + "</p>"
    text4 = summerizer_model.faq()
    return text1, text2, text3, text4, summerizer_model


t1 = t2 = t3 = t4 = t5 = ''
books, titles = get_books_data()
st.title("Summarizer")

with st.sidebar.form(key='my_form'):
    title = st.selectbox("Which book do you want?", titles)
    slider = st.slider("How many chapters maximum do you want to summarize?", min_value=1, max_value=200, value=200,
                       step=1,
                       key="nb_chapitres")
    question = st.text_input("Do you have a question on the book?")
    submit_button = st.form_submit_button(label='Submit parameters')


"You selected:", title

# expander = st.expander("Bert")
# expander.write("Here will come the Bart summary")
# expander2 = st.expander("GPT")
expander3 = st.expander("facebook/bart-large-xsum")
expander4 = st.expander('FAQ')


if submit_button:
    book_id = str(get_book_id(books))
    fichiers = os.listdir(DATAPATH)
    if book_id + ".html" not in fichiers:
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"
        r = requests.get(url)
        with open(
                os.path.join(DATAPATH, book_id + ".html"), "w", encoding="utf-8"
        ) as file:
            file.write(r.text)

    t1, t2, t3, t4, summerizer_model = generate_summary(book_id)
    answer = summerizer_model.qa(question) if question else "No question asked"
    t5 = f"<p align='justify'>Question: {question}</p><p align='justify'>Answer: {answer}</p>"


# expander.write(t1, unsafe_allow_html=True)
# expander2.write(t2, unsafe_allow_html=True)
expander3.write(t3, unsafe_allow_html=True)
expander4.write(t4, unsafe_allow_html=True)
expander4.write(t5, unsafe_allow_html=True)
