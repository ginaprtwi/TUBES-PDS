import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sentimen Pemberitaan")
st.text("Visualisasi ini menampilkan distribusi sentimen berita kriminalitas berdasarkan tahun dan jenis isu.")

df = pd.read_excel("data/fix_data.xlsx")

#filter
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())
with st.container(border=True):
    col1, col2 = st.columns([2,4])
    with col1:
        tahun_selected = st.pills(
            "Pilih Tahun",
            options=list_tahun,
            default=list_tahun,
            selection_mode="multi"
        )

# HANDLE ERROR thn ga dipilih
if not tahun_selected:
    st.warning("⚠️ Silakan pilih minimal satu tahun untuk menampilkan analisis.")
    st.stop()

df_filtered = df[df["tahun"].isin(tahun_selected)]

# LABEL WAKTU
if len(tahun_selected) == 1:
    label_waktu = f"Tahun {tahun_selected[0]}"
else:
    label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

total_berita = len(df_filtered)

sentimen_counts = df_filtered["sentimen"].value_counts()
dominant_sentimen = sentimen_counts.idxmax()
dominant_sentimen_val = sentimen_counts.max()
persen_sentimen = dominant_sentimen_val / total_berita * 100

df_sentimen_dom = df_filtered[df_filtered["sentimen"] == dominant_sentimen]
isu_counts = df_sentimen_dom["jenis_kriminal"].value_counts()

isu_teratas = isu_counts.idxmax()
isu_teratas_val = isu_counts.max()
persen_isu = isu_teratas_val / len(df_sentimen_dom) * 100


with st.container(border=True):
    with st.expander("ℹ️ Keterangan Sentimen Berita"):
        st.markdown("""
        **Negatif:** Menyoroti dampak buruk atau keresahan akibat kriminalitas  
        **Netral:** Bersifat informatif tanpa penekanan emosi  
        **Positif:** Menekankan keberhasilan pengungkapan atau tindakan aparat  
        """)

    st.markdown(f"**Proporsi Sentimen & Isu ({label_waktu})**")
    col1, col2 = st.columns([1.5,3])

    warna_sentimen = {
        "Positif": "cornflowerblue",
        "Negatif": "indianred",
        "Netral": "lightgray"
    }

    with col1:
        fig1, ax1 = plt.subplots(figsize=(4,4))
        sentimen_persen = df_filtered["sentimen"].value_counts(normalize=True) * 100

        ax1.pie(
            sentimen_persen,
            labels=sentimen_persen.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=[warna_sentimen[s] for s in sentimen_persen.index],
            textprops={'color':"black"}
        )
        ax1.set_title("Distribusi Sentimen Keseluruhan (Semua Isu)")
        st.pyplot(fig1, use_container_width=True)

    with col2:
        grouped_isu_sentimen = (
            df_filtered
            .groupby(["jenis_kriminal", "sentimen"])["judul"]
            .count()
            .unstack(fill_value=0)
        )

        # urutan sentimen konsisten
        sentimen_order = ["Positif", "Netral", "Negatif"]
        grouped_isu_sentimen = grouped_isu_sentimen.reindex(
            columns=sentimen_order, fill_value=0
        )

        # urutkan isu berdasarkan total berita
        grouped_isu_sentimen["total"] = grouped_isu_sentimen.sum(axis=1)
        grouped_isu_sentimen = (
            grouped_isu_sentimen
            .sort_values("total", ascending=False)
            .drop(columns="total")
        )

        fig2, ax2 = plt.subplots(figsize=(14, 8))

        x = np.arange(len(grouped_isu_sentimen.index))
        width = 0.25

        for i, sentimen in enumerate(sentimen_order):
            ax2.bar(
                x + i * width,
                grouped_isu_sentimen[sentimen],
                width,
                label=sentimen,
                color=warna_sentimen[sentimen],
                edgecolor="black"
            )

        ax2.set_xlabel("Jenis Isu")
        ax2.set_ylabel("Jumlah Berita")
        ax2.set_title("Jumlah Berita per Sentimen untuk Setiap Isu")

        ax2.set_xticks(x + width)
        ax2.set_xticklabels(grouped_isu_sentimen.index, rotation=45, ha="right")

        ax2.legend(title="Sentimen")
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=False)


# insight
with st.container(border=True):
    st.markdown(f"**Insight ({label_waktu})**")
    if total_berita == 0:
        st.markdown(
            "Tidak terdapat data yang dapat dianalisis karena **belum ada tahun yang dipilih**."
        )
    else:
        st.info(
            f"ℹ️ Berdasarkan analisis pada **{label_waktu}**, Sentimen yang paling dominan adalah "
            f"**{dominant_sentimen}** (**{dominant_sentimen_val}** berita, "
            f"**{persen_sentimen:.1f}%** dari total). "
            f"Isu kriminal yang paling sering diberitakan dalam sentimen ini adalah "
            f"**{isu_teratas}** (**{isu_teratas_val}** berita, "
            f"**{persen_isu:.1f}%** dari total sentimen dominan). "
            "**Temuan** ini menunjukan bahwa **pemberitaan kriminal** lebih banyak "
            "**menyoroti dampak buruk** dibanding proses **keberhasilan penyelesaian kasus**. "
            "Hal ini berguna untuk memahami **kecenderungan**, **keseimbangan** dan "
            "**persepsi publik** terhadap isu kriminalitas."
        )
st.warning("📝 Analisis ini berbasis pemberitaan media, bukan berdasarkan data kejadian kriminal resmi.")
