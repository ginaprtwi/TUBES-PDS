import requests
import os
import time

# --- Input data ---
query = input("Masukan kata kunci kriminalitas: ")
halaman_awal = int(input("Masukan halaman (page) pertama yang akan didownload: "))
halaman_akhir = int(input("Masukan halaman (page) akhir yang akan didownload: "))
nama_file_download = input("Masukan nama file hasil download (contoh: ancaman_narkoba): ")

# --- Logika Folder ---
while True:
    folder_simpan = os.path.join("scraping", "detik2.com")

    if not os.path.exists(folder_simpan):
        print(f"--- INFO: Folder '{folder_simpan}' belum ada.")
        buat_folder = input(f"Apakah ingin membuat folder '{folder_simpan}'? (y/n): ").lower()
        if buat_folder == 'y':
            os.makedirs(folder_simpan)
            print(f"Folder '{folder_simpan}' berhasil dibuat.")
        else:
            print("Silahkan masukkan lokasi lain.")
            continue
    
    konfirmasi = input(f"Apakah lokasi '{os.path.abspath(folder_simpan)}' sudah benar? (y/n): ").lower()
    if konfirmasi == 'y':
        break
    else:
        os.rmdir(folder_simpan) # Menghapus folder yang sudah dibuat
        print("Silahkan masukkan kembali lokasi yang benar.")

# --- PROSES DOWNLOAD ---
print("\n--- Memulai proses download ---\n")

for p in range(halaman_awal, halaman_akhir + 1):
    url = f"https://www.detik.com/search/searchall?query={query}&result_type=latest&page={p}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            file_path = os.path.join(folder_simpan, f"{nama_file_download}_{p}.html")

            print(f"Sedang mendownload Halaman {p}...")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"   > Tersimpan: {file_path}")
        else:
            print(f"   > Gagal di halaman {p}! Status Code: {response.status_code}")

    except Exception as e:
        print(f"   > Terjadi error pada halaman {p}: {e}")

    # Jeda agar tidak terkena blokir
    time.sleep(5) 

print("\nSemua selesai didownload!!")