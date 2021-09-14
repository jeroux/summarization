TEST_VALUE = "Hello World!"

import os
import requests
import pandas as pd
import numpy as np
import streamlit as st

PATH = os.path.abspath(os.path.dirname(__file__))
DATAPATH = os.path.join(PATH, "data")


def get_book_id():
    selection = books[books['Title'] == title]['Text#']
    return selection.iloc[0]


books = pd.read_csv(os.path.join(DATAPATH, "pg_catalog.csv"), sep=',', dtype={
    "Text#":np.int32,
    "Type": "category",
    "Language": "category"})
books.iloc[:,"Issued"]= pd.to_datetime(books["Issued"], yearfirst=True)
titles = books['Title']
titles.drop_duplicates(inplace=True)
titles.dropna(inplace=True)

st.title('Summarizer')

title = st.sidebar.selectbox(
    'Which book do you want?',
    titles)

'You selected:', title

left_column, right_column = st.columns(2)
pressed = left_column.button('confirm')
if pressed:
    book_id = str(get_book_id())
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"

    r = requests.get(url)
    fichiers = os.listdir(DATAPATH)
    if book_id+'.html' not in fichiers:
        with open(os.path.join(DATAPATH, book_id+'.html'), 'w') as file:
            file.write(r.text)

expander = st.expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")
