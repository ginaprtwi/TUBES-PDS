import streamlit as st

dashboard_page = st.Page(
    "dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)

data_berita_page = st.Page(
    "data_berita.py",
    title="Data Berita",
    icon=":material/article:"
)

visualisasi_page = st.Page(
    "visualisasi.py",
    title="Visualisasi",
    icon=":material/analytics:"
)

gis_map_page = st.Page(
    "gis_map.py",
    title="GIS Map",
    icon=":material/map:"
)

pg = st.navigation(
    {
        "Ringkasan": [dashboard_page],
        "Analisis": [data_berita_page, visualisasi_page],
        "Pemetaan": [gis_map_page]
    }
)

pg.run()

