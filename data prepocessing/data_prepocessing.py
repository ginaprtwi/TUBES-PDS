import pandas as pd
import re #buat baca pola 20xx krn klo langsung ubah ke date time ga kebaca semua data nya

df = pd.read_excel("raw_data.xlsx")

#cek duplikat
df = df.drop_duplicates(subset=["judul", "link"])

#biar sama format judulnya
df["judul"] = df["judul"].str.lower()

#hapus hari dan jam, sisain tgl
def get_tanggal_tahun(x):
    # Step 1: kalau sudah datetime, langsung ambil
    if isinstance(x, pd.Timestamp):
        return x, x.year
    try:
        # bersihkan string
        s = str(x).replace("\xa0"," ").replace("WIB","").strip()
        dt = pd.to_datetime(s, dayfirst=True, errors="coerce")
        if pd.notna(dt):
            return dt, dt.year
        else:
            # backup: ambil 4 digit 20xx dari string asli, kalau tahun ga kebaca
            match = re.search(r"20\d{2}", s)
            if match:
                year = int(match.group())
                dt_backup = pd.Timestamp(f"{year}-01-01")
                return dt_backup, year
            else:
                return pd.NaT, 0 #pd.Nat buat nandain tgl yg ga valid biar ga error
    except:
        return pd.NaT, 0 #klo ga ketemu 0

# masukin fungsi ke data frame
df[["tanggal_parsed","tahun"]] = df["tanggal"].apply(get_tanggal_tahun).apply(pd.Series)

# buat kolom tanggal string
df["tanggal"] = df["tanggal_parsed"].dt.strftime("%Y-%m-%d")

# hapus kolom sementara
df = df.drop(columns=["tanggal_parsed"])

# kata kunci kriminal
kata_kunci = {
    "pembunuhan": [
        "bunuh","dibunuh","pembunuhan",
        "tewas","mayat","meninggal",
        "habisi","menghabisi","tragis","tewas mengenaskan"
    ],

    "penculikan": [
        "culik", "penculikan", "diculik", "penyekapan", "disekap"
    ],

    "judi online": [
        "judi", "judol", "perjudian"
    ],

    "kekerasan": [
        "aniaya","dianiaya","penganiayaan",
        "keroyok","pengeroyokan","dikeroyok",
        "pukul","pemukulan",
        "bacok","pembacokan",
        "tusuk","penusukan",
        "tembak","penembakan",
        "kdrt","aniaya istri","aniaya suami","aniaya anak", "kekerasan","pengancaman","ancam",
        "intimidasi","brutal"
    ],

    "pencurian": [
        "curi","pencurian","maling",
        "jambret","rampok","perampokan",
        "begal","bajing loncat", "dirampas","merampas","scam","penipuan","phising", "pinjol", "tppu", "bandit", "data fiktif", "menipu", "tertipu","curanmor", "raib", "copet", "perampas", "pembobolan"
    ],

    "narkoba": [
        "narkoba","sabu","ganja","ekstasi",
        "pil koplo","obat terlarang","tembakau"
    ],

    "pemerkosaan": [
        "perkosa","pemerkosaan",
        "cabul","pencabulan",
        "asusila","pelecehan", "memerkosa"
    ]
}

#kata kunci yg nanti nya bakal di drop
kata_drop = [
    "razia","operasi","sidak","imbauan","himbauan",
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
    "jakarta": "Jakarta Raya", "jakpus": "Jakarta Raya", "jaksel": "Jakarta Raya",
    "jakbar": "Jakarta Raya", "jaktim": "Jakarta Raya", "jakut": "Jakarta Raya",
    "kepulauan seribu": "DJakarta Raya",
    
    # Jawa Barat
    "bandung": "Jawa Barat", "bekasi": "Jawa Barat", "bogor": "Jawa Barat",
    "depok": "Jawa Barat", "cimahi": "Jawa Barat", "garut": "Jawa Barat",
    "subang": "Jawa Barat", "purwakarta": "Jawa Barat", "karawang": "Jawa Barat",
    "tasikmalaya": "Jawa Barat", "cirebon": "Jawa Barat", "sumedang": "Jawa Barat",
    "sukabumi": "Jawa Barat", "ciamis": "Jawa Barat", "majalah": "Jawa Barat",
    
    # Banten
    "tangerang": "Banten", "tangsel": "Banten", "tangerang selatan": "Banten",
    "serang": "Banten", "cilegon": "Banten", "pandeglang": "Banten", "lebak": "Banten",
    
    # Jawa Tengah
    "semarang": "Jawa Tengah", "solo": "Jawa Tengah", "surakarta": "Jawa Tengah",
    "purwokerto": "Jawa Tengah", "pekalongan": "Jawa Tengah", "magelang": "Jawa Tengah",
    "tegal": "Jawa Tengah", "salatiga": "Jawa Tengah", "cilacap": "Jawa Tengah",
    "kudus": "Jawa Tengah", "jepara": "Jawa Tengah", "karanganyar": "Jawa Tengah",
    "boyolali": "Jawa Tengah", "wonogiri": "Jawa Tengah", "karanganyar": "Jawa Tengah",
    
    # DI Yogyakarta
    "yogyakarta": "DI Yogyakarta", "jogja": "DI Yogyakarta", "sleman": "DI Yogyakarta",
    "bantul": "DI Yogyakarta", "kulon progo": "DI Yogyakarta", "gunungkidul": "DI Yogyakarta",
    
    # Jawa Timur
    "surabaya": "Jawa Timur", "malang": "Jawa Timur", "sidoarjo": "Jawa Timur",
    "kediri": "Jawa Timur", "blitar": "Jawa Timur", "mojokerto": "Jawa Timur",
    "pasuruan": "Jawa Timur", "probolinggo": "Jawa Timur", "jember": "Jawa Timur",
    "banyuwangi": "Jawa Timur", "madiun": "Jawa Timur", "ponorogo": "Jawa Timur",
    
    # Sumatera Utara
    "medan": "Sumatera Utara", "binjai": "Sumatera Utara", "pematangsiantar": "Sumatera Utara",
    "tanjungbalai": "Sumatera Utara", "sibolga": "Sumatera Utara", "langkat": "Sumatera Utara",
    
    # Sumatera Selatan
    "palembang": "Sumatera Selatan", "lubuklinggau": "Sumatera Selatan", "prabumulih": "Sumatera Selatan",
    
    # Riau
    "pekanbaru": "Riau", "dumai": "Riau", "selatpanjang": "Riau",
    
    # Sumatera Barat
    "padang": "Sumatera Barat", "solok": "Sumatera Barat", "bukittinggi": "Sumatera Barat",
    "payakumbuh": "Sumatera Barat", "pariaman": "Sumatera Barat",
    
    # Kepulauan Riau
    "batam": "Kepulauan Riau", "tanjungpinang": "Kepulauan Riau", "bintan": "Kepulauan Riau",
    
    # Sulawesi Selatan
    "makassar": "Sulawesi Selatan", "parepare": "Sulawesi Selatan", "bulukumba": "Sulawesi Selatan",
    "gowa": "Sulawesi Selatan", "bantaeng": "Sulawesi Selatan", "pinrang":"Sulawesi Selatan",
    
    # Bali
    "denpasar": "Bali", "bali": "Bali", "tabanan": "Bali", "karangasem": "Bali",
    "klungkung": "Bali", "bangli": "Bali", "gianyar": "Bali", "jembrana": "Bali",
    
    # Kalimantan Timur
    "balikpapan": "Kalimantan Timur", "samarinda": "Kalimantan Timur", "bontang": "Kalimantan Timur",
    "kutai": "Kalimantan Timur", "berau": "Kalimantan Timur",
    
    # Kalimantan Selatan
    "banjarmasin": "Kalimantan Selatan", "martapura": "Kalimantan Selatan", "tanah laut": "Kalimantan Selatan",
    
    # Kalimantan Barat
    "pontianak": "Kalimantan Barat", "singkawang": "Kalimantan Barat", "sanggau": "Kalimantan Barat",
    
    # Sulawesi Utara
    "manado": "Sulawesi Utara", "bitung": "Sulawesi Utara", "tomohon": "Sulawesi Utara",
    
    # Papua
    "jayapura": "Papua", "merauke": "Papua", "biak": "Papua", "nabire": "Papua",
    
    # Provinsi tambahan kota besar
    "bengkulu": "Bengkulu", "lhokseumawe": "Aceh", "meulaboh": "Aceh", "aceh besar": "Aceh",
    "palangkaraya": "Kalimantan Tengah", "sampit": "Kalimantan Tengah", "tarakan": "Kalimantan Utara",
    "toli-toli": "Sulawesi Tengah", "palu": "Sulawesi Tengah", "kendari": "Sulawesi Tenggara",
}

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

#drop judul bukan kriminal
df = df[df["judul"].apply(lambda x: not any(k in str(x) for k in kata_drop))]
df = df[df["sumber"].apply(lambda x: not any(s in str(x) for s in sumber_drop))]


# drop judul tanpa kota
df = df[(df["kota"] != "lainnya")].reset_index(drop=True)


df = df[df["tahun"] != 2026].reset_index(drop=True)

df.to_excel("fix_data.xlsx", index=False)