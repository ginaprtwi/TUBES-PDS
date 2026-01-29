import pandas as pd
import re 
from datetime import datetime

df = pd.read_excel("o.xlsx")

#biar sama format judulnya
df["judul"] = df["judul"].str.lower()

#buat kata kunci 
# kata kunci kriminal
kata_kunci = {
    "pencurian": [
        "curi","pencurian","maling", "jambret","rampok","perampokan", "begal","bajing loncat", 
        "dirampas", "merampas","scam","penipuan","phising", "pinjol", "tppu", "bandit", "data fiktif", 
        "menipu", "tertipu","curanmor", "raib", "copet", "perampas", "pembobolan", "gasak", "digasak"
    ],

    "kekerasan": [
        "aniaya","dianiaya","penganiayaan", "keroyok","pengeroyokan","dikeroyok",
        "pukul","pemukulan","bacok","pembacokan", "tusuk","penusukan","tembak","penembakan",
        "kdrt","aniaya istri","aniaya suami", "aniaya anak", "kekerasan","pengancaman","ancam",
        "intimidasi","brutal","kekerasan", "miras", "tawuran", "mabuk"
    ],
    
    "pemerkosaan": [
        "perkosa","pemerkosaan", "cabul", "pencabulan","asusila","pelecehan","memerkosa",
        "pelecehan seksual","pelecehan anak","PE","perkosaan massal", "pemaksaan seksual"
    ],

    "narkoba": [
        "narkoba","sabu","ganja","ekstasi", "pil koplo","obat terlarang","tembakau",
        "ganja kering", "miras oplosan", "cocaine", "meth", "happy five", "shabu-shabu",
        "pil koplo", "psikotropika", "tembakau sintetis", "heroin"
    ],

    "pembunuhan": [
        "bunuh","dibunuh","pembunuhan", "tewas","mayat","meninggal", "habisi",
        "menghabisi","tragis","tewas mengenaskan"
    ],

    "penculikan": [
        "culik", "penculikan", "diculik", "penyekapan", "disekap", "penculik", 
        "disandera", "sandera", "diambil paksa", "ditawan", "pemerasan"
    ]
}

#kata kunci framing media
kata_sentimen = {
    "positif": [
        # keberhasilan penegakan hukum / polisi / pengadilan
        "berhasil ditangkap", "ditangkap", "tersangka diamankan", "tertangkap",
        "pengungkapan kasus", "pelaku diproses", "penegakan hukum", "tersangka ditahan",
        "korban mendapatkan keadilan", "penyelidikan berhasil", "polisi selidiki",
        "polisi tangkap", "pelaku diringkus", "tersangka dijebloskan penjara", "kasus tuntas",
        "tersangka dibekuk", "tersangka menyerahkan diri", "tersangka kooperatif", "pelaku diadili",
        "penjahat ditangkap", "keadilan ditegakkan", "diringkus"
    ],

    "negatif": [
        # kejahatan & kriminalitas
        "kabur", "tidak tertangkap", "menghilang", "merajalela", "menyerang", "korupsi",
        "kriminal", "razia", "pembunuhan", "penganiayaan", "perampokan", "perdagangan narkoba",
        "penipuan", "kekerasan", "pelecehan", "perkelahian", "kejahatan", "pembobolan", "curanmor",
        "jambret", "begal", "maling", "aniaya", "pemukulan", "penculikan", "perkosa", "pemerkosaan",
        "sabu", "ganja", "narkoba", "tembak", "penembakan", "tusuk", "penusukan", "ancam", "intimidasi",
        "brutal", "dirampas", "dikeroyok", "dibegal", "dibobol", "diperkosa", "ditipu", "menipu", "tertipu",
        "diculik", "dianiaya", "merampok", "terbakar", "kebakaran", "bencana", "perusakan", "vandal", "teror",
        "bom", "ledakan", "pembajakan", "penyekapan", "tawuran"
    ]
}

#kata kunci yg nanti nya bakal di drop
kata_drop = [
    "sosialisasi","edukasi","kampanye",
    "kunjungan","peresmian","rapat","apel",
    "pengamanan","siaga","lalu lintas","kecelakaan",
    "banjir","longsor", "tiket konser", "lowongan kerja", "internasional"
]

sumber_drop = [
    "detikfood", "detikHot", "detikFinance", "detikInet"
]

#kata kunci kota
kotaxprov = {
    # DKI Jakarta
    "jakarta": "Jakarta Raya", "dki": "Jakarta Raya", "jakpus": "Jakarta Raya", "jaksel": "Jakarta Raya",
    "jakbar": "Jakarta Raya", "jaktim": "Jakarta Raya", "jakut": "Jakarta Raya", "kep seribu": "Jakarta Raya",
    "kepulauan seribu": "Jakarta Raya",

    # Jawa Barat
    "jabar": "Jawa Barat", "bandung": "Jawa Barat", "kab bandung": "Jawa Barat", "bandung barat": "Jawa Barat",
    "bekasi": "Jawa Barat", "kab bekasi": "Jawa Barat", "bogor": "Jawa Barat", "kab bogor": "Jawa Barat",
    "depok": "Jawa Barat", "cimahi": "Jawa Barat", "garut": "Jawa Barat", "tasik": "Jawa Barat", "tasikmalaya": "Jawa Barat",
    "cirebon": "Jawa Barat", "kab cirebon": "Jawa Barat", "sukabumi": "Jawa Barat", "sumedang": "Jawa Barat", "subang": "Jawa Barat",
    "karawang": "Jawa Barat", "purwakarta": "Jawa Barat", "indramayu": "Jawa Barat", "majalengka": "Jawa Barat",
    "ciamis": "Jawa Barat",

    # Banten
    "banten": "Banten", "tangerang": "Banten",
    "kab tangerang": "Banten", "tangsel": "Banten",
    "tangerang selatan": "Banten", "serang": "Banten",
    "cilegon": "Banten", "lebak": "Banten",
    "pandeglang": "Banten",

    # Jawa Tengah
    "jateng": "Jawa Tengah", "semarang": "Jawa Tengah", "solo": "Jawa Tengah", 
    "surakarta": "Jawa Tengah", "purwokerto": "Jawa Tengah", "cilacap": "Jawa Tengah",
    "pekalongan": "Jawa Tengah", "tegal": "Jawa Tengah", "magelang": "Jawa Tengah",
    "salatiga": "Jawa Tengah", "kudus": "Jawa Tengah", "jepara": "Jawa Tengah",
    "pati": "Jawa Tengah", "demak": "Jawa Tengah", "klaten": "Jawa Tengah",
    "boyolali": "Jawa Tengah", "wonogiri": "Jawa Tengah",

    # DI Yogyakarta
    "diy": "Yogyakarta", "jogja": "Yogyakarta", "yogyakarta": "Yogyakarta",
    "sleman": "Yogyakarta", "bantul": "Yogyakarta", "kulon progo": "Yogyakarta",
    "gunungkidul": "Yogyakarta",

    # Jawa Timur
    "jatim": "Jawa Timur", "surabaya": "Jawa Timur", "sby": "Jawa Timur",
    "malang": "Jawa Timur", "kab malang": "Jawa Timur", "sidoarjo": "Jawa Timur",
    "gresik": "Jawa Timur", "mojokerto": "Jawa Timur", "kediri": "Jawa Timur",
    "blitar": "Jawa Timur", "pasuruan": "Jawa Timur", "probolinggo": "Jawa Timur",
    "jember": "Jawa Timur", "banyuwangi": "Jawa Timur", "madiun": "Jawa Timur",
    "ponorogo": "Jawa Timur", "tuban": "Jawa Timur", "lamongan": "Jawa Timur",

    # Sumatera (umum media)
    "sumut": "Sumatera Utara", "medan": "Sumatera Utara", "binjai": "Sumatera Utara",
    "siantar": "Sumatera Utara", "sumsel": "Sumatera Selatan", "palembang": "Sumatera Selatan",
    "sumbar": "Sumatera Barat", "padang": "Sumatera Barat", "bukittinggi": "Sumatera Barat",

    #riau
    "riau": "Riau","pekanbaru": "Riau","dumai": "Riau", "kepri": "Riau", "batam": "Riau", 
    "tanjungpinang": "Riau",

    #aceh
    "aceh": "Aceh", "banda aceh": "Aceh", "lhokseumawe": "Aceh",

    # Bengkulu
    "bengkulu": "Bengkulu", "lebong": "Bengkulu", "rejang lebong": "Bengkulu", "curup": "Bengkulu",
    
    #lampung
    "lampung": "Lampung", "bandar lampung": "Lampung",

    # Kalimantan
    "kaltim": "Kalimantan Timur", "balikpapan": "Kalimantan Timur", "samarinda": "Kalimantan Timur",
    "kalsel": "Kalimantan Selatan", "banjarmasin": "Kalimantan Selatan",
    "kalbar": "Kalimantan Barat", "pontianak": "Kalimantan Barat",
    "kalteng": "Kalimantan Tengah", "palangkaraya": "Kalimantan Tengah",
    "kalut": "Kalimantan Utara", "tarakan": "Kalimantan Utara",

    # Sulawesi
    "sulsel": "Sulawesi Selatan", "makassar": "Sulawesi Selatan", "gowa": "Sulawesi Selatan",
    "sulteng": "Sulawesi Tengah", "palu": "Sulawesi Tengah", "sulut": "Sulawesi Utara",
    "manado": "Sulawesi Utara", "sultra": "Sulawesi Tenggara", "kendari": "Sulawesi Tenggara", 
    "sulbar": "Sulawesi Barat", "majene": "Sulawesi Barat", "polewali mandar": "Sulawesi Barat",

    # Bali & Nusa Tenggara
    "bali": "Bali", "denpasar": "Bali",
    "badung": "Bali", "ntb": "Nusa Tenggara Barat", "mataram": "Nusa Tenggara Barat", 
    "ntt": "Nusa Tenggara Timur", "kupang": "Nusa Tenggara Timur",

    # Maluku
    "maluku": "Maluku", "ambon": "Maluku", "tual": "Maluku", "namlea": "Maluku",

    # Papua
    "papua": "Papua", "jayapura": "Papua", "merauke": "Papua",

    # Jambi
    "jambi": "Jambi", "muaro jambi": "Jambi", "muara jambi": "Jambi", "batanghari": "Jambi",
    "tebo": "Jambi", "bungo": "Jambi", "tanjab barat": "Jambi", "tanjab timur": "Jambi",
    "tanjung jabung barat": "Jambi", "tanjung jabung timur": "Jambi", "sarolangun": "Jambi",
    "merangin": "Jambi", "kerinci": "Jambi", "sungai penuh": "Jambi",

    # Maluku Utara
    "malut": "Maluku Utara", "tidore": "Maluku Utara", "ternate": "Maluku Utara",
    
    # Papua Barat
    "papua barat": "Papua Barat", "manokwari": "Papua Barat", "sorong": "Papua Barat",
    
    # Kalimantan Barat tambahan
    "singkawang": "Kalimantan Barat", "ketapang": "Kalimantan Barat",
    
    # Kalimantan Tengah tambahan
    "kapuas": "Kalimantan Tengah", "kotawaringin": "Kalimantan Tengah",
    
    # Kalimantan Timur tambahan
    "kutai": "Kalimantan Timur", "sangatta": "Kalimantan Timur",
    
    # Kalimantan Selatan tambahan
    "tanah laut": "Kalimantan Selatan", "baru": "Kalimantan Selatan",
    
    # Sulawesi Tenggara tambahan
    "konawe": "Sulawesi Tenggara", "baubau": "Sulawesi Tenggara",
    
    # Sulawesi Tengah tambahan
    "donggala": "Sulawesi Tengah", "banggai": "Sulawesi Tengah",
    
    # Sulawesi Selatan tambahan
    "parepare": "Sulawesi Selatan", "bone": "Sulawesi Selatan", "enrekang": "Sulawesi Selatan",
    
    # Sumatera Utara tambahan
    "tobasa": "Sumatera Utara", "tapanuli": "Sumatera Utara",
    
    # Sumatera Barat tambahan
    "solok": "Sumatera Barat", "payakumbuh": "Sumatera Barat",
    
    # Sumatera Selatan tambahan
    "lubuklinggau": "Sumatera Selatan", "karanganyar": "Sumatera Selatan",
    
    # Lampung tambahan
    "metro": "Lampung", "pringsewu": "Lampung",
    
    # Aceh tambahan
    "langsa": "Aceh", "aceh timur": "Aceh",

}


df["tanggal"] = df["tanggal"].astype(str)
df["tanggal"] = df["tanggal"].str.replace(r"^[A-Za-z]+,\s*", "", regex=True)
df["tanggal"] = df["tanggal"].str.replace(r"\s+\d{1,2}:\d{2}.*$", "", regex=True)

# Ganti bulan Indonesia ke English
bulan = {
    "Januari":"January", "Februari":"February", "Maret":"March", "April":"April",
    "Mei":"May", "Juni":"June", "Juli":"July", "Agustus":"August",
    "September":"September", "Oktober":"October", "November":"November", "Desember":"December"
}
for indo, eng in bulan.items():
    df["tanggal"] = df["tanggal"].str.replace(indo, eng, regex=True)

# Parse tanggal
df["tanggal"] = pd.to_datetime(df["tanggal"], dayfirst=True, errors="coerce", infer_datetime_format=True)

# Ambil tahun
df["tahun"] = df["tanggal"].dt.year

# Overwrite format
df["tanggal"] = df["tanggal"].dt.strftime("%d-%m-%Y")



#buat kolom baru 
df["kota"] = df["judul"].apply(
    lambda x: next((k for k in kotaxprov.keys() if k in x), "lainnya")
)

df["provinsi"] = df["judul"].apply(
    lambda x: next((v for k, v in kotaxprov.items() if k in x), "Lainnya")
)

df["jenis_kriminal"] = df["judul"].apply(
    lambda x: next((key for key, kws in kata_kunci.items() if any(kw in x for kw in kws)), "lainnya")
)

df["sentimen"] = df["judul"].apply(
    lambda x: "Positif" if any(k in str(x).lower() for k in kata_sentimen["positif"])
    else "Negatif" if any(k in str(x).lower() for k in kata_sentimen["negatif"])
    else "Netral"
)

#drop judul bukan kriminal
df = df[df["judul"].apply(lambda x: not any(k in str(x) for k in kata_drop))]
df = df[df["sumber"].apply(lambda x: not any(s in str(x) for s in sumber_drop))]

#cek duplikat
df = df.drop_duplicates(subset=["judul", "link"])

# drop judul tanpa kota
df = df[(df["kota"] != "lainnya")].reset_index(drop=True)

# drop thn selain 24 atau 25
df = df[df["tahun"].isin([2024, 2025])].reset_index(drop=True)

df.to_excel("xxx.xlsx", index=False)