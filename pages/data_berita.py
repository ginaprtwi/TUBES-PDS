import pandas as pd
import streamlit as st

df = pd.read_excel("data/fix_data.xlsx")

st.title("Data Berita")
st.text("Seluruh data yang diambil dari media Detik.com.")

st.dataframe(df)
