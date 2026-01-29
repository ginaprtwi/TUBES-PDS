import streamlit as st

dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)

isu_kota_page = st.Page(
    "pages/analisis_dominan.py",
    title="Isu & Wilayah Dominan",
    icon=":material/stacks:"
)

sumber_page = st.Page(
    "pages/analisis_sumber.py",
    title="Sumber Pemberitaan",
    icon=":material/monitoring:"
)

sentimen_page = st.Page(
    "pages/analisis_sentimen.py",
    title="Sentimen Pemberitaan",
    icon=":material/psychology:"
)

gis_map_page = st.Page(
    "pages/gis_map.py",
    title="Peta GIS",
    icon=":material/map:"
)

data_mentah_page = st.Page(
    "pages/data_berita.py",
    title="Data Berita",
    icon=":material/article:"
)

pg = st.navigation(
    {
        "Ringkasan": [dashboard_page],
        "Visualisasi": [isu_kota_page, sumber_page, sentimen_page],
        "Pemetaan": [gis_map_page],
        "Data": [data_mentah_page]
    }
)

pg.run()
