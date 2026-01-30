import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sentimen Pemberitaan")
st.text("Visualisasi ini menampilkan distribusi sentimen berita kriminalitas berdasarkan tahun.")

# Baca data
df = pd.read_excel("data/fix_data.xlsx")

# Filter tahun
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())
tahun_selected = st.pills(
    "Pilih Tahun",
    options=list_tahun,
    default=list_tahun,
    selection_mode="multi"
)

# Filter data berdasarkan tahun
if not tahun_selected:
    df_filtered = pd.DataFrame()
else:
    df_filtered = df[df["tahun"].isin(tahun_selected)]

# Label waktu
if not tahun_selected:
    label_waktu = "Tidak ada tahun dipilih"
elif len(tahun_selected) == 1:
    label_waktu = f"Tahun {tahun_selected[0]}"
else:
    label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

total_berita = len(df_filtered)

# Hitung sentimen
if not df_filtered.empty:
    sentimen_counts = df_filtered["sentimen"].value_counts()
    if not sentimen_counts.empty:
        dominant_sentimen = sentimen_counts.idxmax()
        dominant_sentimen_val = sentimen_counts.max()
        persen_sentimen = dominant_sentimen_val / total_berita * 100
    else:
        dominant_sentimen = "Tidak ada data"
        dominant_sentimen_val = 0
        persen_sentimen = 0
else:
    dominant_sentimen = "Tidak ada data"
    dominant_sentimen_val = 0
    persen_sentimen = 0

# Warna sentimen
warna_sentimen = {
    "Positif": "cornflowerblue",  
    "Negatif": "indianred",       
    "Netral": "lightgray"         
}

# Container visualisasi
with st.container(border=True):
    with st.expander("ℹ️ Keterangan Sentimen Berita"):
        st.markdown("""
        **Negatif:** Menyoroti dampak buruk atau keresahan akibat kriminalitas.  
        **Netral:** Bersifat informatif tanpa penekanan emosi.  
        **Positif:** Menekankan keberhasilan pengungkapan atau tindakan aparat.  
        """)
    st.markdown(f"**Proporsi Sentimen ({label_waktu})**")
    col1, col2 = st.columns(2)

    # Pie chart
    with col1:
        fig1, ax1 = plt.subplots(figsize=(7,7))
        if df_filtered.empty or sentimen_counts.empty:
            ax1.text(0.5,0.5,"Silakan pilih tahun", ha="center", va="center")
        else:
            sentimen_persen = sentimen_counts / sentimen_counts.sum() * 100
            labels_sorted = sentimen_persen.index
            warna_pie = [warna_sentimen.get(s,"gray") for s in labels_sorted]
            ax1.pie(
                sentimen_persen,
                labels=labels_sorted,
                autopct="%1.1f%%",
                startangle=140,
                colors=warna_pie,
                textprops={'color':"black"}
            )
            ax1.set_title("Distribusi Sentimen Keseluruhan")
        st.pyplot(fig1, use_container_width=True)

    # Bar chart per jenis kriminal
    with col2:
        if not df_filtered.empty:
            grouped_isu_sentimen = df_filtered.groupby(["jenis_kriminal","sentimen"])["judul"].count().unstack(fill_value=0)
            stack_order = ["Positif", "Netral", "Negatif"]
            grouped_isu_sentimen = grouped_isu_sentimen.reindex(columns=stack_order, fill_value=0)
            grouped_isu_sentimen["total"] = grouped_isu_sentimen.sum(axis=1)
            grouped_isu_sentimen = grouped_isu_sentimen.sort_values(by="total", ascending=False).drop(columns="total")
            
            fig2, ax2 = plt.subplots(figsize=(8,6))
            warna_bar = [warna_sentimen[s] for s in grouped_isu_sentimen.columns]
            grouped_isu_sentimen.plot(
                kind="bar",
                stacked=True,
                ax=ax2,
                color=warna_bar,
                edgecolor="black"
            )
            ax2.set_ylabel("Jumlah Berita")
            ax2.set_xlabel("Jenis Isu")
            ax2.set_title("Jumlah Berita per Sentimen untuk Setiap Jenis Kriminal")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.info("Silakan pilih tahun")

# Insight
with st.container(border=True):
    st.markdown(f"**Insight ({label_waktu})**")
    if total_berita == 0:
        st.markdown("Tidak terdapat data yang dapat dianalisis karena **belum ada tahun dipilih**.")
    else:
        isu_counts_total = df_filtered["jenis_kriminal"].value_counts()
        if not isu_counts_total.empty:
            isu_teratas = isu_counts_total.idxmax()
            isu_teratas_val = isu_counts_total.max()
        else:
            isu_teratas = "Tidak ada data"
            isu_teratas_val = 0
        
        st.info(
            f"ℹ️ Berdasarkan analisis pada **{label_waktu}**, Sentimen yang paling dominan adalah **{dominant_sentimen}** "
            f"(**{dominant_sentimen_val}** berita, **{persen_sentimen:.1f}%** dari total). "
            f"Jenis kriminal yang paling sering diberitakan adalah **{isu_teratas}** "
            f"(**{isu_teratas_val}** berita)."
        )

st.warning("📝 Analisis ini berbasis pemberitaan media, bukan data kejadian kriminal resmi.")
