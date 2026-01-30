import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Sumber Pemberitaan")
st.text("Distribusi isu kriminalitas berdasarkan sumber media dari berbagai subdomain Detik.com.")


df = pd.read_excel("data/fix_data.xlsx")

# Filter tahun
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
    dftahun = df.iloc[0:0]
    label_waktu = "Tidak ada tahun dipilih"
    st.warning("Silakan pilih minimal satu tahun untuk menampilkan data.", icon="⚠️")
else:
    dftahun = df[df["tahun"].isin(tahun_selected)]
    if len(tahun_selected) == 1:
        label_waktu = f"Tahun {tahun_selected[0]}"
    else:
        label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

total_kasus = len(dftahun)
grouped_jenis = (dftahun.groupby("jenis_kriminal")["judul"].count().sort_values(ascending=False) if not dftahun.empty else pd.Series(dtype=int))
grouped_sumber = (dftahun.groupby("sumber")["judul"].count().sort_values(ascending=False) if not dftahun.empty else pd.Series(dtype=int))

# Sumber dominan
sumber_dominan = grouped_sumber.idxmax() if not grouped_sumber.empty else "-"
sumber_dominan_val = grouped_sumber.max() if not grouped_sumber.empty else 0
persen_sumber = (sumber_dominan_val / total_kasus * 100) if total_kasus > 0 else 0

# top 10 sumber
top10_sumber = grouped_sumber.head(10).index
df_top10 = dftahun[dftahun["sumber"].isin(top10_sumber)]

with st.container(border=True):
    st.markdown(f"**Sumber dominan ({label_waktu})**")
    col_pie, col_table = st.columns([2, 1])
    with col_pie:
        fig, ax = plt.subplots(figsize=(7, 7))
        if not grouped_sumber.empty:
            top_sumber = grouped_sumber.head(10)
            lainnya_val = grouped_sumber.iloc[10:].sum() if len(grouped_sumber) > 10 else 0
            if lainnya_val > 0:
                top_sumber = pd.concat([top_sumber, pd.Series({"Lainnya": lainnya_val})])
            ax.pie(
                top_sumber.values,
                labels=top_sumber.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=plt.cm.Paired(np.linspace(0, 1, len(top_sumber)))
            )
            ax.set_title("Distribusi Sumber Berita Kriminal")
        else:
            ax.text(0.5,0.5,"Tidak ada data", ha="center", va="center")
        st.pyplot(fig, use_container_width=True)

    with col_table:
        st.markdown("**Distribusi Isu Kriminal per Sumber**")
        if not df_top10.empty:
            pivot_df = df_top10.pivot_table(
                index="sumber",
                columns="jenis_kriminal",
                values="judul",
                aggfunc="count",
                fill_value=0
            )
            
            # urutkan isu paling banyak ke paling sedikit
            total_per_jenis = pivot_df.sum(axis=0)
            pivot_df = pivot_df[total_per_jenis.sort_values(ascending=False).index]

            # urutkan sumber paling banyak ke paling sedikit
            total_per_sumber = pivot_df.sum(axis=1)
            pivot_df = pivot_df.loc[total_per_sumber.sort_values(ascending=False).index]
            
            st.dataframe(pivot_df.style.format("{:.0f}"))

            #hitung isu dominan sesuai sumber
            if sumber_dominan in pivot_df.index:
                row_dominan = pivot_df.loc[sumber_dominan]
                isu_teratas = row_dominan.idxmax()
                isu_teratas_val = row_dominan.max()
                persen_isu = isu_teratas_val / row_dominan.sum() * 100
            else:
                isu_teratas = "-"
                isu_teratas_val = 0
                persen_isu = 0
        else:
            st.info("Tidak ada data untuk periode yang dipilih.")
            isu_teratas = "-"
            isu_teratas_val = 0
            persen_isu = 0

#Insight
with st.container(border=True):
    st.markdown(f"**Insight ({label_waktu})**")
    if total_kasus == 0:
        st.markdown(
            "Tidak terdapat data yang dapat dianalisis karena **belum ada tahun yang dipilih**."
        )
    else:
        st.info(f"Berdasarkan hasil analisis pada **{label_waktu}** sumber pemberitaan terbanyak adalah **{sumber_dominan}** **({sumber_dominan_val}** berita, "
            f"**{persen_sumber:.1f}%** dari total), dengan isu paling sering diberitakan adalah **{isu_teratas}** "
            f"(**{isu_teratas_val}** berita, **{persen_isu:.1f}%** dari total di **{sumber_dominan}**). "
            "**Temuan** ini menunjukkan **dominasi media nasional** dalam eksposur isu kriminal serta **perbedaan fokus isu** antar sumber media. "
            "Hal ini berguna untuk mengetahui **kecenderungan fokus isu** tiap media, **dasar pemantauan** media dominan, dan **potensi bias pemberitaan**."
        )

st.warning("📝 Analisis ini berbasis pemberitaan media, bukan berdasarkan data kejadian kriminal resmi.")
