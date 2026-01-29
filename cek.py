import pandas as pd
df = pd.read_excel("fix_data.xlsx")

# Misal kita mau tahun 2025
df_filtered = df[
    (df['jenis_kriminal'].str.contains("pencurian", case=False, na=False)) &
    (df['tahun'] == 2024)
]

# Hitung frekuensi jenis kriminal
print(df_filtered['jenis_kriminal'].value_counts())
