import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sentimen Pemberitaan")
st.text("Visualisasi ini menampilkan distribusi sentimen berita kriminalitas berdasarkan tahun dan jenis isu.")

df = pd.read_excel("data/fix_data.xlsx")

#filter tahun
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
    with col2:
        list_jenis = sorted(df[df["tahun"].isin(tahun_selected)]["jenis_kriminal"].dropna().unique()) if tahun_selected else []
        with st.popover("Pilih Jenis Isu", width="stretch"):
            jenis_selected = st.multiselect(
                "Pilih Jenis Isu",
                options=list_jenis,
                default=list_jenis,
                key="jenis_selected"
            )
            st.button("Semua Isu", on_click=lambda: st.session_state.update({"jenis_selected": list(list_jenis)}))

#filter isu
df_filtered = df[
    (df["tahun"].isin(tahun_selected)) & 
    (df["jenis_kriminal"].isin(jenis_selected))
] if tahun_selected else pd.DataFrame()

#label waktu
if not tahun_selected:
    label_waktu = "Tidak ada tahun dipilih"
elif len(tahun_selected) == 1:
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
isu_terendah = isu_counts.idxmin()
isu_terendah_val = isu_counts.min()
persen_isu_terendah = isu_terendah_val / len(df_sentimen_dom) * 100

with st.container(border=True):
    with st.expander("ℹ️ Keterangan Sentimen Berita"):
        st.markdown("""
        **Negatif:** Menyoroti dampak buruk atau keresahan akibat kriminalitas.  
        **Netral:** Bersifat informatif tanpa penekanan emosi.  
        **Positif:** Menekankan keberhasilan pengungkapan atau tindakan aparat.  
""")
    st.markdown(f"**Proporsi Sentimen & Isu ({label_waktu})**")
    col1, col2 = st.columns(2)
    #Warna per sentimen
    warna_sentimen = {
        "Positif": "cornflowerblue",  
        "Negatif": "indianred",       
        "Netral": "lightgray"         
    }
    with col1:
        fig1, ax1 = plt.subplots(figsize=(7,7))
        if not tahun_selected:
            ax1.text(0.5,0.5,"Tidak ada data", ha="center", va="center")
        else:
            df_pie = df[df["tahun"].isin(tahun_selected)]
            sentimen_counts = df_pie["sentimen"].value_counts()
            sentimen_persen = sentimen_counts / sentimen_counts.sum() * 100
            labels_sorted = sentimen_persen.index
            warna_pie = [warna_sentimen[s] for s in labels_sorted]

            ax1.pie(
                sentimen_persen,
                labels=labels_sorted,
                autopct="%1.1f%%",
                startangle=140,
                colors=warna_pie,
                textprops={'color':"black"}
            )
            ax1.set_title("Distribusi Sentimen Keseluruhan (Semua Isu)")
        st.pyplot(fig1, use_container_width=True)

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
            ax2.set_title("Jumlah Berita per Sentimen untuk Setiap Isu")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.info("Tidak ada data untuk ditampilkan.")

#insight
with st.container(border=True):
    st.markdown(f"**Insight ({label_waktu})**")
    if total_berita == 0:
        st.markdown("Tidak terdapat data yang dapat dianalisis karena **belum ada tahun atau isu yang dipilih**.")
    else:
        st.info(
            f"ℹ️ Berdasarkan analisis pada **{label_waktu}**, Sentimen yang paling dominan adalah **{dominant_sentimen}** "
            f"(**{dominant_sentimen_val}** berita, **{persen_sentimen:.1f}%** dari total). "
            f"Isu kriminal yang paling sering diberitakan dalam sentimen ini adalah **{isu_teratas}** "
            f"(**{isu_teratas_val}** berita, **{persen_isu:.1f}%** dari total sentimen dominan). "
            "**Temuan** ini menunjukan bahwa **pemberitaan kriminal** lebih banyak **menyoroti dampak buruk** dibanding proses **keberhasilan penyelesaian kasus**. "
            "Hal ini berguna untuk memahami **kecenderungan**, **keseimbangan** dan **persepsi publik** terhadap isu kriminalitas."
        )

st.warning("📝 Analisis ini berbasis pemberitaan media, bukan berdasarkan data kejadian kriminal resmi.")
