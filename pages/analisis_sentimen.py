import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sentimen Pemberitaan")
st.text("Visualisasi ini menampilkan distribusi sentimen berita kriminalitas berdasarkan tahun dan jenis isu.")

# Load data
df = pd.read_excel("data/fix_dataa.xlsx")
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")

# List filter
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())

# Container filter
with st.container(border=True):
    col1, col2 = st.columns([2, 4])
    
    with col1:
        # Tahun pakai pills
        tahun_selected = st.pills(
            "Pilih Tahun",
            options=list_tahun,
            default=list_tahun,
            selection_mode="multi"
        )
    
    with col2:
        # Filter jenis isu pakai popover
        list_jenis = sorted(df[df["tahun"].isin(tahun_selected)]["jenis_kriminal"].dropna().unique()) \
            if len(tahun_selected) > 0 else []
        
        with st.popover("Pilih Jenis Isu", width="stretch"):
            jenis_selected = st.multiselect(
                "Pilih Jenis Isu",
                options=list_jenis,
                default=list_jenis, 
                key="jenis_selected",
            )
            st.button("Semua Isu",on_click=lambda: st.session_state.update({"jenis_selected": list(list_jenis)}))

# Filter data sesuai pilihan
df_filtered = df[
    (df["tahun"].isin(tahun_selected)) &
    (df["jenis_kriminal"].isin(jenis_selected))
] if len(tahun_selected) > 0 else pd.DataFrame()

# Label waktu
if not tahun_selected:
    label_waktu = "Tidak ada tahun dipilih"
elif len(tahun_selected) == 1:
    label_waktu = f"Tahun {tahun_selected[0]}"
else:
    label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

# Total berita
total_berita = len(df_filtered)

# PIE & BAR CHART SEJAJAR
with st.container(border=True):
    col1, col2 = st.columns(2)

    # Pie chart
    with col1:
        st.subheader(f"Proporsi Sentimen ({label_waktu})")
        fig1, ax1 = plt.subplots(figsize=(6,6))
        if not df_filtered.empty:
            sentimen_counts_all = df_filtered["sentimen"].value_counts()
            sentimen_persen_all = df_filtered["sentimen"].value_counts(normalize=True) * 100
            dominant_sentimen_all = sentimen_counts_all.idxmax()
    
            ax1.pie(
                sentimen_persen_all,
                labels=sentimen_persen_all.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=plt.cm.Paired(np.linspace(0,1,len(sentimen_persen_all)))
            )
            ax1.set_title("Distribusi Sentimen Keseluruhan")
        else:
            dominant_sentimen_all = "-"
            ax1.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")
        st.pyplot(fig1)

    # Bar chart
    with col2:
        st.subheader(f"Jumlah Berita per Isu ({label_waktu})")
        if not df_filtered.empty:
            grouped_isu_sentimen = df_filtered.groupby(["jenis_kriminal", "sentimen"])["judul"].count().unstack(fill_value=0)
    
            fig2, ax2 = plt.subplots(figsize=(8,6))
            grouped_isu_sentimen.plot(kind="bar", stacked=True, ax=ax2, colormap="Paired")
            ax2.set_ylabel("Jumlah Berita")
            ax2.set_xlabel("Jenis Isu")
            ax2.set_title("Jumlah Berita per Sentimen untuk Setiap Isu")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig2)
        else:
            st.info("Tidak ada data untuk ditampilkan.")

# Insight di bawah chart
st.subheader("Insight")
if total_berita == 0:
    st.markdown("Insight belum dapat ditampilkan karena **tidak ada data yang dianalisis**.")
else:
    # Top isu
    top_isi = grouped_isu_sentimen.sum(axis=1).idxmax()
    top_isi_val = grouped_isu_sentimen.sum(axis=1).max()

    st.markdown(f"""
- Fokus monitoring pada **{top_isi}** karena paling banyak diberitakan.  
- Jika **negatif lebih tinggi**, perlu perhatian atau intervensi terkait isu kriminal tersebut.  
- Jika **positif lebih tinggi**, bisa digunakan sebagai indikasi penegakan hukum atau keberhasilan tindakan polisi.
""")
