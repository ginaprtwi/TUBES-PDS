import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Isu & Wilayah Dominan")
st.text("Visualisasi ini menunjukkan isu kriminal dan wilayah dengan intensitas pemberitaan tertinggi.")

df = pd.read_excel("data/fix_data.xlsx")

#Filter Tahun
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())

with st.container(border=True):
    tahun_selected = st.pills(
        "Pilih Tahun",
        options=list_tahun,
        default=list_tahun,
        selection_mode="multi",
    )

# Biar ga error kalau ga pilih tahun
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

#Total kasus
total_kasus = len(dftahun)
grouped_jenis = (dftahun.groupby("jenis_kriminal")["judul"].count().sort_values(ascending=False) if not dftahun.empty else pd.Series(dtype=int))
grouped_prov = (dftahun.groupby("provinsi")["judul"].count().sort_values(ascending=False) if not dftahun.empty else pd.Series(dtype=int))

kriminal_dominan = grouped_jenis.idxmax() if not grouped_jenis.empty else "-"
top_prov_nama = grouped_prov.idxmax() if not grouped_prov.empty else "-"
top_prov_val = grouped_prov.max() if not grouped_prov.empty else 0
bottom_prov_nama = grouped_prov.idxmin() if not grouped_prov.empty else "-"


with st.container(border=True):
    st.markdown(f"**Isu & Wilayah Dominan({label_waktu})**")
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 7))
        if not dftahun.empty:
            df_pivot = dftahun.pivot_table(
                index="jenis_kriminal",
                columns="tahun",
                values="judul",
                aggfunc="count"
            ).fillna(0)

            #urutkan
            df_pivot['total'] = df_pivot.sum(axis=1)
            df_pivot = df_pivot.sort_values(by='total', ascending=False).drop(columns='total')

            warna = plt.cm.Blues(np.linspace(0.35, 0.85, df_pivot.shape[1]))

            df_pivot.plot(
                kind="bar",
                stacked=True,
                ax=ax1,
                edgecolor="black",
                color=warna
            )

        ax1.set_title("Distribusi Jenis Kriminal")
        ax1.set_ylabel("Jumlah Isu")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=False)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        #buat urutin line grafik nya
        top_10_p = grouped_prov.head(10).sort_values(ascending=False).index
        df_top = dftahun[dftahun["provinsi"].isin(top_10_p)]
        if not grouped_prov.empty:
            df_pivot_prov = df_top.pivot_table(
                index="provinsi",
                columns="tahun",
                values="judul",
                aggfunc="count"
            ).fillna(0)

            warna_line = plt.cm.Blues(np.linspace(0.4, 0.8, len(df_pivot_prov.columns)))
            for i, col in enumerate(df_pivot_prov.columns):
                ax2.plot(
                    df_pivot_prov.index,
                    df_pivot_prov[col],
                    marker="o",
                    color=warna_line[i],
                    label=str(col)
                )

            ax2.legend(title="Tahun")
            ax2.set_title("Top 10 Wilayah dengan Isu Kriminal Terbanyak")
            ax2.set_ylabel("Jumlah Isu")
            plt.xticks(rotation=45, ha="right")
            ax2.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig2, use_container_width=False)

#Insight
with st.container(border=True):
    st.markdown(f"**Insight ({label_waktu})**")
    if total_kasus == 0:
        st.markdown(
            "Tidak terdapat data yang dapat dianalisis karena **belum ada tahun yang dipilih**."
        )
    else:
        st.info(
    f"ℹ️ Berdasarkan hasil analisis pada **{label_waktu}**, tercatat **{total_kasus}** isu kriminalitas yang diberitakan oleh **Detik.com**. "
    f"Isu kriminal yang paling dominan adalah **{kriminal_dominan}**, dengan **{top_prov_nama}** sebagai wilayah yang paling sering diberitakan "
    f"**({top_prov_val}** isu), sementara **{bottom_prov_nama}** memiliki intensitas pemberitaan terendah. "
    "**Temuan** ini berguna untuk mengidentifikasi **pola dominasi isu** dan **wilayah dalam pemberitaan kriminalitas**, terutama untuk wilayah yang **jarang terekspos media**."
)

st.warning("📝 Analisis ini berbasis pemberitaan media, bukan berdasarkan data kejadian kriminal resmi.")
