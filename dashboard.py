import streamlit as st
import pandas as pd

st.title("Dashboard")
st.caption("Ringkasan isu kriminal yang sering diberitakan di Indonesia berdasarkan media online Detik.com")

df = pd.read_excel("fix_data.xlsx")
jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax().capitalize()
kota_terbanyak = df["kota"].value_counts().idxmax().capitalize()
sumber_teraktif = df["sumber"].value_counts().idxmax()
topik = df[df["jenis_kriminal"] == jenis_terbanyak]
topik = topik.sort_values("tanggal", ascending=False)
rekomendasi = topik.head(3)

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.caption("Total Data Berita")
        st.markdown(f"**{len(df)}**")

with col2:
    with st.container(border=True):
        st.caption("Isu Dominan")
        st.markdown(f"**{jenis_terbanyak}**")

with col3:
    with st.container(border=True):
        st.caption("Wilayah Dominan")
        st.markdown(f"**{kota_terbanyak}**")

with col4:
    with st.container(border=True):
        st.caption("Sumber Berita Teraktif")
        st.markdown(f"**{sumber_teraktif}**")

with st.container(border=True):
    st.caption("Rekomendasi Berita berdasarkan isu dominan")
    for i in range(len(rekomendasi)):
        judul = rekomendasi["judul"].values[i]
        link  = rekomendasi["link"].values[i]
        st.markdown(f"{i+1}. [{judul}]({link})")