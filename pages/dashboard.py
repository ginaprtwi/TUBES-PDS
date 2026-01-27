import streamlit as st
import pandas as pd

st.title("Dashboard")
st.text("Ringkasan isu kriminal yang sering diberitakan di Indonesia berdasarkan media online Detik.com periode 2024-2025")

df = pd.read_excel("data/fix_dataa.xlsx")

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

df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax()
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
    st.text("Rekomendasi Berita berdasarkan isu dominan")

    if rekomendasi.empty:
        st.info("Tidak ada rekomendasi berita untuk ditampilkan.")
    else:
        for _, row in rekomendasi.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])  
            with col1:
                st.markdown(f"**{row['judul']}**")
                st.caption(f"{row['tanggal'].strftime('%d-%m-%Y')} | {row['sumber']}")

            with col2:
                st.markdown(f"[Baca selengkapnya]({row['link']})")

        