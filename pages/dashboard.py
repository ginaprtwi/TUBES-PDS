import streamlit as st
import pandas as pd

st.title("Dashboard")
st.text("Ringkasan Pemberitaan Kriminalitas di Indonesia berdasarkan media online Detik.com (2024-2025)")

df = pd.read_excel("data/fix_data.xlsx")

jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax().capitalize()
prov_terbanyak = df["provinsi"].value_counts().idxmax()
sumber_teraktif = df["sumber"].value_counts().idxmax()

#urutin sesuai tgl
df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")

#rekomendasi
jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax()
topik = df[df["jenis_kriminal"] == jenis_terbanyak]
topik = topik.sort_values("tanggal", ascending=False)
rekomendasi = topik.head(3)


col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.caption("Jumlah Berita")
        st.markdown(f"**{len(df)}**")

with col2:
    with st.container(border=True):
        st.caption("Isu Dominan")
        st.markdown(f"**{jenis_terbanyak}**")

with col3:
    with st.container(border=True):
        st.caption("Wilayah Dominan")
        st.markdown(f"**{prov_terbanyak}**")

with col4:
    with st.container(border=True):
        st.caption("Sumber Dominan")
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
                st.markdown(f"**{row['judul'].title()}**")
                st.caption(f"{row['tanggal'].strftime('%d-%m-%Y')} | {row['sumber']}")

            with col2:
                st.markdown(f"[Baca selengkapnya]({row['link']})")

        