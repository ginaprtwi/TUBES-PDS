from bs4 import BeautifulSoup
import pandas as pd
import os


BASE_DIR = os.path.dirname(__file__)
folder_path = os.path.join(BASE_DIR, "detik.com")

all_data = []

for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            html = file.read()
        
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")
        
        for article in articles:
            link_tag = article.find("a", href=True)
            link = link_tag["href"] if link_tag else "-"
            
            judul_tag = article.find("div", class_="media__desc")
            judul = judul_tag.text.strip() if judul_tag else "-"
            
            tanggal_tag = article.find("div", class_="media__date")
            span = tanggal_tag.find("span") if tanggal_tag else None
            tanggal = span["title"] if span and span.has_attr("title") else "-"
            
            sumber_tag = article.find("h2", class_="media__subtitle")
            sumber = sumber_tag.get_text(strip=True) if sumber_tag else "-"

            
            if judul != "-" and link != "-":
                all_data.append({
                    "judul": judul,
                    "link": link,
                    "tanggal": tanggal,
                    "sumber": sumber
                })


df = pd.DataFrame(all_data)

df.to_excel("raw_data.xlsx", index=False)



