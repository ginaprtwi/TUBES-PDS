import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

st.title("Visualisasi Data Kriminal")

# =======================
# LOAD DATA
# =======================
df = pd.read_excel("fix_data.xlsx")

# Rapikan nama kolom
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Pastikan nama kolom kriminal
df = df.rename(columns={"nis_kriminal": "jenis_kriminal"})

# =======================
# FILTER TAHUN
# =======================
tahun_list = sorted(df["tahun"].unique())
tahun_pilih = st.selectbox("Pilih Tahun", tahun_list)

df_tahun = df[df["tahun"] == tahun_pilih]

# =======================
# GROUPING
# =======================
grouped_jenis = df_tahun.groupby("jenis_kriminal")["judul"].count()
grouped_kota = df_tahun.groupby("kota")["judul"].count()
grouped_sumber = df_tahun.groupby("sumber")["judul"].count()

# Ambil TOP 10 kota agar grafik garis jelas
top_kota = grouped_kota.sort_values(ascending=False).head(10)

# =======================
# TAMPILAN
# =======================
col1, col2, col3 = st.columns(3)

# -------- BAR JENIS KRIMINAL --------
with col1:
    st.subheader("Jenis Kriminal Terbanyak")

    plt.figure(figsize=(8,6))
    plt.bar(grouped_jenis.index, grouped_jenis.values, color="orange")
    plt.xlabel("Jenis Kriminal")
    plt.ylabel("Jumlah Isu")
    plt.title("Jumlah Isu Berdasarkan Jenis Kriminal")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(plt)
    plt.clf()

# -------- GRAFIK GARIS KOTA --------
with col2:
    st.subheader("Kota Terbanyak Kriminal")

    plt.figure(figsize=(8,6))
    plt.plot(top_kota.index, top_kota.values, marker="o")
    plt.xlabel("Kota")
    plt.ylabel("Jumlah Isu")
    plt.title("Top 10 Kota dengan Isu Kriminal Terbanyak")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(plt)
    plt.clf()
    
with col3:
    top_sumber = grouped_sumber.sort_values(ascending=False).head(5)
    lainnya = grouped_sumber.sum() - top_sumber.sum()
    top_sumber["Lainnya"] = lainnya
# -------- PIE CHART SUMBER BERITA --------
    st.subheader(f"Distribusi Sumber Berita Tahun {tahun_pilih}")
    plt.figure(figsize=(7,7))
    plt.pie(
        top_sumber.values,
        labels=top_sumber.index,
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Proporsi Sumber Berita")

    st.pyplot(plt)
    plt.clf()
# Ambil TOP 5 agar pie chart jelas




# ==========================================
# GRAFIK HISTORI JENIS KRIMINAL PER TAHUN
# ==========================================
st.divider()
st.subheader("Jenis Kriminalitas Per Tahun")

# Menghitung jumlah per Tahun dan Jenis Kriminal
# Gunakan seluruh data (df) agar terlihat perbandingannya antar tahun
df_grouped = df.groupby(['tahun', 'jenis_kriminal']).size().unstack(fill_value=0)

# Visualisasi Grouped Bar Chart
fig, ax = plt.subplots(figsize=(15, 7))

# Mengatur warna latar belakang (Sage Green)
ax.set_facecolor('#88b388') 
fig.patch.set_facecolor('#88b388')

# Membuat bar bertumpuk atau berjajar (di sini berjajar agar macam kriminalitas jelas)
df_grouped.plot(kind='bar', ax=ax, width=0.8, edgecolor='#1a3617')

# Kustomisasi Grid (Garis putih horizontal)
ax.yaxis.grid(True, color='white', linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Menghilangkan bingkai
for spine in ax.spines.values():
    spine.set_visible(False)

# Mengatur Label Sumbu X (Tahun) dan Y (Jumlah)
plt.xticks(rotation=0, color='white', fontweight='bold')
plt.yticks(color='white', fontweight='bold')
ax.set_xlabel("Tahun", color='white', fontweight='bold')
ax.set_ylabel("Jumlah Insiden", color='white', fontweight='bold')

# Judul Grafik
ax.set_title("Kejahatan yang Dilaporkan berdasarkan Tahun & Kategori", loc='left', color='white', 
             fontsize=16, fontweight='bold', pad=20)

# Mengatur Legend agar tidak menutupi grafik
plt.legend(title="Jenis Kriminal", bbox_to_anchor=(1.03, 1), loc='upper left', frameon=True)

# Menampilkan di Streamlit
st.pyplot(fig)

# ==========================================
# GRAFIK GARIS MULTI-KATEGORI (PER JENIS)
# ==========================================
st.divider()
st.subheader("Tren Jenis Kriminalitas dari Tahun ke Tahun")

# Visualisasi Multi-Line Chart
fig3, ax3 = plt.subplots(figsize=(15, 8))

# Mengatur warna latar belakang agar seragam
ax3.set_facecolor('#88b388') 
fig3.patch.set_facecolor('#88b388')

# Membuat grafik garis untuk setiap kolom (jenis kriminal)
# Gunakan marker agar setiap titik tahun terlihat jelas
df_grouped.plot(kind='line', ax=ax3, marker='o', linewidth=2.5, markersize=8)

# Kustomisasi Grid (Garis putih horizontal)
ax3.yaxis.grid(True, color='white', linestyle='-', linewidth=0.5)
ax3.set_axisbelow(True)

# Menghilangkan bingkai
for spine in ax3.spines.values():
    spine.set_visible(False)

# Mengatur Label Sumbu X dan Y
plt.xticks(df_grouped.index, color='white', fontweight='bold')
plt.yticks(color='white', fontweight='bold')
ax3.set_xlabel("Tahun", color='white', fontweight='bold')
ax3.set_ylabel("Jumlah Insiden", color='white', fontweight='bold')

# Judul Grafik
ax3.set_title("Perbandingan Tren antar Jenis Kriminalitas", loc='left', 
              color='white', fontsize=16, fontweight='bold', pad=20)

# Mengatur Legend di samping agar tidak menutupi garis
plt.legend(title="Jenis Kriminal", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

# Menampilkan di Streamlit
st.pyplot(fig3)

# ==========================================
# GRAFIK GARIS TREN SELURUH KOTA & TAHUN (INTERAKTIF)
# ==========================================
st.divider()
st.subheader("Tren Kriminalitas per Kota")

# Mendapatkan daftar seluruh kota unik
semua_kota = sorted(df['kota'].unique())

# Logika Tombol "Pilih Semua" menggunakan Session State
if 'kota_terpilih' not in st.session_state:
    st.session_state.kota_terpilih = [] # Default awal kosong

def pilih_semua():
    st.session_state.kota_terpilih = semua_kota

def hapus_semua():
    st.session_state.kota_terpilih = []

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    st.button("Pilih Semua Kota", on_click=pilih_semua)
with col_btn2:
    st.button("Kosongkan Pilihan", on_click=hapus_semua)

# Widget Multi-select dengan nilai dari session_state
kota_pilihan = st.multiselect(
    "Cari dan Pilih Kota untuk Membandingkan:", 
    options=semua_kota, 
    key='kota_terpilih' # Menghubungkan widget dengan session_state
)

# Filter data berdasarkan pilihan
df_filtered_kota = df[df['kota'].isin(kota_pilihan)]

# Cek jika data tidak kosong, maka buat grafik
if not df_filtered_kota.empty:
    df_kota_all = df_filtered_kota.groupby(['tahun', 'kota']).size().unstack(fill_value=0)

    fig5, ax5 = plt.subplots(figsize=(15, 8))

    # Tema Warna Hijau Sage
    ax5.set_facecolor('#88b388') 
    fig5.patch.set_facecolor('#88b388')

    # Plotting
    df_kota_all.plot(kind='line', ax=ax5, marker='o', linewidth=2, markersize=6, colormap='tab20')

    # Desain Grid & Spines
    ax5.yaxis.grid(True, color='white', linestyle='-', linewidth=0.5)
    ax5.set_axisbelow(True)
    for spine in ax5.spines.values():
        spine.set_visible(False)

    # Labeling
    plt.xticks(df_kota_all.index, color='white', fontweight='bold')
    plt.yticks(color='white', fontweight='bold')
    ax5.set_xlabel("Tahun", color='white', fontweight='bold')
    ax5.set_ylabel("Jumlah Kasus", color='white', fontweight='bold')
    ax5.set_title(f"Perbandingan Tren Kriminalitas ({len(kota_pilihan)} Kota)", 
                  loc='left', color='white', fontsize=16, fontweight='bold', pad=20)

    # Legend
    plt.legend(title="Daftar Kota", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, fontsize='small')

    st.pyplot(fig5)
else:
    # Tampilan saat grafik kosong
    st.info("Grafik kosong. Silakan pilih satu atau beberapa kota melalui menu di atas atau klik 'Pilih Semua Kota'.")

# ==========================================
# PIE CHART SELURUH SUMBER BERITA
# ==========================================
st.divider()
st.subheader("Distribusi Seluruh Sumber Berita")

# Menghitung jumlah per sumber berita
df_sumber_all = df['sumber'].value_counts()

# Opsional: Ambil Top 10 agar Pie Chart tidak terlalu penuh
top_n = 10
if len(df_sumber_all) > top_n:
    sumber_top = df_sumber_all.head(top_n)
    sumber_lainnya = pd.Series({'Lainnya': df_sumber_all.iloc[top_n:].sum()})
    data_pie = pd.concat([sumber_top, sumber_lainnya])
else:
    data_pie = df_sumber_all

# Visualisasi Pie Chart
fig6, ax6 = plt.subplots(figsize=(10, 8))

# Tema Warna Hijau Sage
ax6.set_facecolor('#88b388') 
fig6.patch.set_facecolor('#88b388')

# Membuat warna gradasi hijau untuk setiap potongan pie
colors_pie = cm.Greens(np.linspace(0.4, 0.9, len(data_pie)))

# Menggambar Pie Chart
wedges, texts, autotexts = ax6.pie(
    data_pie.values, 
    labels=data_pie.index, 
    autopct='%1.1f%%', 
    startangle=140,
    colors=colors_pie,
    textprops={'color':"white", 'weight':'bold'}, # Warna label sumber
    pctdistance=0.85, # Jarak persentase dari pusat
    explode=[0.05] * len(data_pie) # Memberi sedikit jarak antar potongan
)

# Mengatur warna persentase di dalam lingkaran agar lebih jelas
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)

# Menghilangkan bingkai default
ax6.axis('equal')  

# Judul Grafik
ax6.set_title("Sumber Berita Kriminalitas", color='white', 
              fontsize=16, fontweight='bold', pad=20)

# Menampilkan di Streamlit
st.pyplot(fig6)