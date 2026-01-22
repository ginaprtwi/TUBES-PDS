import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium



st.set_page_config(layout="wide")
st.title("Peta Persebaran Pemberitaan Rawan Kriminal")

df = pd.read_excel("fix_data.xlsx")
df = pd.DataFrame(df)

# =========================
# FILTER TAHUN & PROVINSI
# =========================

df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
list_tahun = df["tahun"].dropna().astype(int).unique()
list_provinsi = df["provinsi"].dropna().astype(str).unique()


with st.container(border=True):
    col3, col4 = st.columns([2, 4])
    with col3:
        tahun_selected = st.multiselect(
            "Pilih Tahun",
            options=list_tahun,
            key="tahun_selected",
        )
        
    
    with col4:

        provinsi_selected = st.multiselect(
            "Pilih Provinsi",
            options=list_provinsi,
            key="provinsi_selected",
        )
        
    with st.container(border=False):
        col5, col6 = st.columns([2,4])
        with col5:
            st.button("Semua Tahun",on_click=lambda: st.session_state.update({"tahun_selected": list(list_tahun)}))
        with col6:
            st.button("Semua Provinsi",on_click=lambda: st.session_state.update({"provinsi_selected": list(list_provinsi)}))
        

    
    dftahun = df[
        (df["tahun"].isin(tahun_selected)) &
        (df["provinsi"].isin(provinsi_selected))
    ]

#Insightt 

total_kasus = len(dftahun)  
print("total kasus:",total_kasus)
prov_summary = (dftahun.groupby("provinsi")["judul"].count().reset_index(name="jumlah"))
print("prov_summary",prov_summary)

if len(prov_summary) > 0:   
    prov_max = prov_summary.loc[prov_summary["jumlah"].idxmax()]  
    prov_min = prov_summary.loc[prov_summary["jumlah"].idxmin()]  
    print("max",prov_max)
    print("min", prov_min)

    kriminal_dominan = dftahun["jenis_kriminal"].value_counts().idxmax()  

    with st.container(border=True):  
        if len(provinsi_selected) == 1 and len(tahun_selected) == 1:
            st.markdown(  
                f"""
                ###  Insight Provinsi {provinsi_selected[0]}
                Di provinsi **{provinsi_selected[0]}** selama periode {tahun_selected[0]}
                tercatat **{total_kasus} isu kriminalitas**.
                Jenis kriminal paling dominan adalah **{kriminal_dominan}**.
                """
            )
        
        elif len(tahun_selected) == 1:
            st.markdown(  
                f"""
                ###  Insight Tahun {tahun_selected[0]}
                Pada tahun **{tahun_selected[0]}** tercatat **{total_kasus} isu kriminalitas**.
                Provinsi paling rawan adalah **{prov_max['provinsi']} ({prov_max['jumlah']} isu)**,
                sementara **{prov_min['provinsi']}** menjadi provinsi dengan isu terendah.
                Jenis kriminal paling dominan adalah **{kriminal_dominan}**.
                """
            )
        
        else:
            st.markdown(  
                f"""
                ###  Insight Periode {min(tahun_selected)}–{max(tahun_selected)}
                Selama periode ini tercatat **{total_kasus} isu kriminalitas**.
                Wilayah paling rawan adalah **{prov_max['provinsi']}**,
                sedangkan **{prov_min['provinsi']}** relatif paling aman.
                Kriminalitas didominasi oleh **{kriminal_dominan}**.
                """
            )

# =========================
# DATA UNTUK MAP
# =========================

grouped_kota = dftahun.groupby("provinsi")["judul"].count().reset_index(name='jumlah')
df_map = pd.DataFrame(grouped_kota)   

def kategori(jumlah):
    if jumlah > 40:
        return "Sangat Rawan"
    elif jumlah > 25:
        return "Rawan"
    elif jumlah > 10:
        return "Cukup Rawan"
    else:
        return "Aman"

df_map["kategori"] = df_map["jumlah"].apply(kategori)

kategori_map = {
    "Aman": 1,
    "Cukup Rawan": 2,
    "Rawan": 3,
    "Sangat Rawan": 4
}
df_map["level"] = df_map["kategori"].map(kategori_map)

# =========================
# MAP & PANEL
# =========================

col1, col2 = st.columns([5, 2])

with col1:
    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    folium.Choropleth(
        geo_data="indonesia_prov.json",
        data=df_map,
        columns=["provinsi", "level"],
        key_on="feature.properties.NAME_1",
        fill_color="RdYlGn_r",
        threshold_scale=[1, 2, 3, 4, 5],
        fill_opacity=0.7,
        line_opacity=0.4,
        nan_fill_opacity=0.4,
    ).add_to(m)

    folium.GeoJson(
        "indonesia_prov.json",
        name="Provinsi",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME_1"],
            aliases=["Provinsi:"],
            sticky=True
        )
    ).add_to(m)

    st_folium(m, width=900, height=600)

with col2:
    with st.container(border=True):
        st.subheader("Keterangan Kategori")
        st.markdown(
            """
            - **Sangat Rawan**: > 40 kasus
            - **Rawan**: 26–40 kasus
            - **Cukup Rawan**: 11–25 kasus
            - **Aman**: ≤ 10 kasus
            """
        )
        st.divider()
        st.subheader("Data")
        st.dataframe(df_map, width="stretch") 
