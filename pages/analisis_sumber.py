import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sumber dan Pola Pemberitaan")
st.text("Visualisasi ini menggambarkan pola pemberitaan isu kriminalitas berdasarkan jenis, wilayah, dan sumber media.")
df = pd.read_excel("data/fix_dataa.xlsx")

#filter tahun
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())

with st.container(border=True):
    tahun_selected = st.pills(
        "Pilih Tahun",
        options=list_tahun,
        default=list_tahun,
        selection_mode="multi",
    )

if not tahun_selected:
    dftahun = df.iloc[0:0]  # dataframe kosong
    label_waktu = "Tidak ada tahun dipilih"
    st.warning("Silakan pilih minimal satu tahun untuk menampilkan data.", icon="⚠️")
else:
    dftahun = df[df["tahun"].isin(tahun_selected)]
    if len(tahun_selected) == 1:
        label_waktu = f"Tahun {tahun_selected[0]}"
    else:
        label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

total_kasus = len(dftahun)

grouped_jenis = (dftahun.groupby("jenis_kriminal")["judul"].count().sort_values(ascending=False)
    if not dftahun.empty else pd.Series(dtype=int))
grouped_kota = (
    dftahun.groupby("kota")["judul"].count().sort_values(ascending=False)
    if not dftahun.empty else pd.Series(dtype=int))
grouped_sumber = (
    dftahun.groupby("sumber")["judul"].count().sort_values(ascending=False)
    if not dftahun.empty else pd.Series(dtype=int))

kriminal_dominan = grouped_jenis.idxmax() if not grouped_jenis.empty else "-"
top_kota_nama = grouped_kota.idxmax() if not grouped_kota.empty else "-"
top_kota_val = grouped_kota.max() if not grouped_kota.empty else 0
bottom_kota_nama = grouped_kota.idxmin() if not grouped_kota.empty else "-"

sumber_dominan = grouped_sumber.idxmax() if not grouped_sumber.empty else "-"
sumber_dominan_val = grouped_sumber.max() if not grouped_sumber.empty else 0
persen_sumber = (sumber_dominan_val / total_kasus * 100) if total_kasus > 0 else 0

#sumber
st.subheader(f"Sumber Berita dan Pola Pemberitaan ({label_waktu})")

col_pie, col_insight = st.columns([2, 1])

# PIE CHART
with col_pie:
    with st.container(border=True):
        fig3, ax3 = plt.subplots(figsize=(7, 7))

        if not grouped_sumber.empty:
            top_sumber = grouped_sumber.head(10)
            lainnya_val = grouped_sumber.iloc[10:].sum() if len(grouped_sumber) > 10 else 0

            if lainnya_val > 0:
                top_sumber = pd.concat([top_sumber, pd.Series({"Lainnya": lainnya_val})])

            ax3.pie(
                top_sumber.values,
                labels=top_sumber.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=plt.cm.Paired(np.linspace(0, 1, len(top_sumber)))
            )
            ax3.set_title("Distribusi Sumber Berita Kriminal")
        else:
            ax3.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

        st.pyplot(fig3)

#sumber berita
with col_insight:
    with st.container(border=True):
        st.markdown("### Insight")

        if total_kasus == 0:
            st.markdown(
                "Insight sumber berita belum dapat ditampilkan karena **tidak ada data yang dianalisis**."
            )
        else:
            st.markdown(f"""
            📰 **Sumber dominan**: **{sumber_dominan}**  
            📊 **Jumlah berita**: **{sumber_dominan_val}**  
            📈 **Kontribusi**: sekitar **{persen_sumber:.1f}%** dari total berita

            Dominasi ini menunjukkan bahwa **{sumber_dominan}** berperan signifikan
            dalam penyebaran isu kriminalitas pada periode analisis.
            """)
