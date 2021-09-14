TEST_VALUE = "Hello World!"

import os

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import streamlit as st

PATH = os.path.abspath(os.path.dirname(__file__))
DATAPATH = os.path.join(PATH, "data")

books = pd.read_csv(os.path.join(DATAPATH, "pg_catalog.csv"), sep=',')
titles = books['Title']
titles.drop_duplicates(inplace=True)
titles.dropna(inplace=True)

st.title('Summarizer')

option = st.sidebar.selectbox(
    'Which number do you like best?',
    titles)

'You selected:', option

left_column, right_column = st.columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")
