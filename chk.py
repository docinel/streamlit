import streamlit as st
import pandas as pd

st.write("Hello, *World!* :sunglasses:")

df = st.dataframe(
    {
        "first column": [1, 2, 3, 4],
        "second column": [10, 20, 30, 40],
        "third column": [100, 200, 300, 400],
    }
)

st.sidebar.write("Hello, *World!* :sunglasses:")


pri_col =st.sidebar(
    "Choose Primary Column:",
     options=df["first column"].unique(),
     )

def_select = df.query("first column == @pri_col")