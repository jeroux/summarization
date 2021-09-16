import os
import requests
import pandas as pd
import numpy as np
import streamlit as st

from core.extract_html import BreakDownBook
from core.ml.transformersML import Bart

PATH = os.path.abspath(os.path.dirname(__file__))
DATAPATH = os.path.join(PATH, "data")


def get_book_id():
    selection = books[books["Title"] == title]["Text#"]
    return selection.iloc[0]


books = pd.read_csv(
    os.path.join(DATAPATH, "pg_catalog.csv"),
    sep=",",
    dtype={"Text#": np.int32, "Type": "category", "Language": "category"}, low_memory=False
)
titles = books["Title"]
titles.drop_duplicates(inplace=True)
titles.dropna(inplace=True)

st.title("Summarizer")

title = st.sidebar.selectbox("Which book do you want?", titles)

"You selected:", title

left_column, right_column = st.columns(2)
pressed = left_column.button("confirm")
expander = st.expander("Bart")
expander.write("Here will come the Bart summary")

if pressed:
    book_id = str(get_book_id())
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"

    r = requests.get(url)
    fichiers = os.listdir(DATAPATH)
    if book_id + ".html" not in fichiers:
        with open(
                os.path.join(DATAPATH, book_id + ".html"), "w", encoding="utf-8"
        ) as file:
            file.write(r.text)

    book = BreakDownBook(os.path.join(DATAPATH, book_id + ".html"))
    bart = Bart(book.text)
    expander.write(bart.summary)
