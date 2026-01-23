import streamlit as st
import pandas as pd

st.title("Dashboard")
st.caption("Ringkasan isu kriminal yang sering diberitakan di Indonesia berdasarkan media online Detik.com (2024-2025)")

df = pd.read_excel("fix_dataa.xlsx")

jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax().capitalize()
kota_terbanyak = df["kota"].value_counts().idxmax().capitalize()
sumber_teraktif = df["sumber"].value_counts().idxmax()

#hitung tren isu 2024-2025
jumlah_per_tahun = df["tahun"].value_counts()
ambil_2024 = jumlah_per_tahun.get(2024)
ambil_2025 = jumlah_per_tahun.get(2025)
delta = ambil_2025 - ambil_2024
delta_persen = (delta / ambil_2024) * 100

#hitung tren kota
kota_2024 = df[df["tahun"] == 2024]["kota"].value_counts()
kota_2025 = df[df["tahun"] == 2025]["kota"].value_counts()
tren_kota = df["kota"].value_counts().idxmax()
delta_kota = kota_2025.get(tren_kota) - kota_2024.get(tren_kota)
delta_persen = ((delta_kota / kota_2024.get(tren_kota, 1)) * 100)

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

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.caption("Tren Isu 2024-2025")
        st.metric(
            label="Jumlah Data Tahun 2025",
            value=f"{ambil_2025:,}",
            delta=f"{delta_persen:.2f}%",
            delta_color="normal",
            width="content"
        )  
with col2:
    with st.container(border=True):
        st.caption("Tren Kecenderungan Framing Pemberitaan 24-25")
        st.metric(
            label="Negatif",
            value=f"{ambil_2025:,}",
            delta=f"{delta_persen:.2f}%",
            delta_color="normal",
            width="content"
        ) 

with st.container(border=True):
    st.caption("Rekomendasi Berita berdasarkan isu dominan")
    for i in range(len(rekomendasi)):
        judul = rekomendasi["judul"].values[i]
        link  = rekomendasi["link"].values[i]
        st.markdown(f"{i+1}. [{judul}]({link})")