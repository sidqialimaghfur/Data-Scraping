from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

def scrape_liputan6_news():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.liputan6.com/'
        }
        
        url = "https://www.liputan6.com/"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(soup.prettify())
        
        articles = []
        
        main_articles = (
            soup.find_all('article', class_=re.compile(r'articles--list')) or
            soup.find_all('div', class_=re.compile(r'article-list')) or
            soup.find_all('article')
        )
        
        print(f"Jumlah artikel yang ditemukan: {len(main_articles)}")
        
        for article in main_articles[:10]:
            print("Artikel:", article)
            
            title_elem = (
                article.find('h3', class_=re.compile(r'articles--list__title')) or
                article.find('h2', class_=re.compile(r'title')) or
                article.find('a', class_=re.compile(r'title'))
            )
            title = title_elem.text.strip() if title_elem else "Judul Tidak Tersedia"
            
            link_elem = (
                article.find('a', class_=re.compile(r'articles--list__title-link')) or
                article.find('a', href=True)
            )
            link = link_elem['href'] if link_elem else "#"
            
            img_elem = (
                article.find('img', class_=re.compile(r'articles--list__img')) or
                article.find('img', src=True)
            )
            img_url = img_elem['src'] if img_elem else "https://via.placeholder.com/300x200"
            
            desc_elem = (
                article.find('div', class_=re.compile(r'articles--list__excerpt')) or
                article.find('p', class_=re.compile(r'excerpt'))
            )
            description = desc_elem.text.strip() if desc_elem else "Deskripsi tidak tersedia"
            
            articles.append({
                'title': title,
                'link': link,
                'image': img_url,
                'description': description
            })
        
        return articles
    except Exception as e:
        print(f"Error scraping Liputan6: {e}")
        import traceback
        traceback.print_exc()
        return []

def scrape_kategori_berita():
    """Mengambil daftar kategori berita dari Liputan6.com"""
    try:
        url = "https://www.liputan6.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        kategori = []
        nav_menu = soup.find('nav', class_=re.compile(r'navbar__category'))
        
        if nav_menu:
            menu_items = nav_menu.find_all('a', class_=re.compile(r'navbar__category-list-link'))
            for item in menu_items[:10]:
                kategori.append({
                    'nama': item.text.strip(),
                    'link': item.get('href', '#')
                })
        
        return kategori
    except Exception as e:
        print(f"Error scraping kategori: {e}")
        return []

@app.route('/')
def index():
    berita = scrape_liputan6_news()
    kategori = scrape_kategori_berita()
    return render_template('index.html', berita=berita, kategori=kategori)

@app.route('/berita')
def daftar_berita():
    berita = scrape_liputan6_news()
    return render_template('berita.html', berita=berita)

@app.route('/kategori')
def daftar_kategori():
    kategori = scrape_kategori_berita()
    return render_template('kategori.html', kategori=kategori)

if __name__ == '__main__':
    app.run(debug=True)