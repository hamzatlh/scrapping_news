from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Define your keywords
keywords = [
    "Adnane Filali", "Azure innovation", "Azure Partners", "FM6I", "FMVII",
    "fond mohamed VI", "Agritech", "E-learning", "La digitalisation", "capital", "capital amorçage", "capital risque", "capital investissement",
    "investissement", "investissement en capital", "investissement en amorçage", "investissement en risque", "investissement en capital investissement",
    "education", "formation", "enseignement", "apprentissage", "éducation", "école", "collège", "lycée", "université", "établissement scolaire",
    "Edtech", "Edutech", "Fintech", "Healthtech", "Insurtech", "Legaltech", "Regtech", "Retailtech", "Santé", "Santé numérique", "Santé connectée",
    "finance", "fintech", "banque", "assurance", "crédit", "prêt", "épargne", "investissement", "paiement", "monnaie", "cryptomonnaie", "blockchain",
    "technologie", "innovation", "numérique", "digital", "digitalisation", "transformation digitale", "technologique", "numérisation", "IA", "IA",
    "intelligence artificielle", "machine learning", "deep learning", "big data", "analyse de données", "IoT", "internet des objets", "cloud",
    "hightech", "IA", "innov invest", "game", "gaming", "jeu", "jeux", "jeux vidéo", "esport", "esports", "sport électronique", "sport électroniques",
    "KFW", "merging", "acquisition", "fusion", "acquisition", "restructuration", "restructuration", "restructuration", "restructuration",
    "mergin acquisition", "neuroéducation", "neurosciences", "neuroscience", "neuroéducation", "neuroéducation", "neuroéducation",
]

def setup_selenium():
    options = Options()
    options.headless = True  # Running headless to avoid UI load for automation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_with_selenium(url):
    driver = setup_selenium()
    driver.get(url)
    time.sleep(10)  # Allow some time for all JavaScript to load completely
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def write_to_file(url, title_text, text):
    with open("found_articles.txt", "a") as file:
        file.write(f"Website: {url}\n")
        file.write(f"Title: {title_text}\n")
        file.write(f"Content: {text[:200]}... [truncated]\n")  # Writing first 200 chars of the content
        file.write("----------------------------------------\n")

def scrape_site(url):
    soup = scrape_with_selenium(url)
    
    # Custom selectors based on the website
    custom_selectors = {
        'https://www.leconomiste.com/': [('div', {'class': 'some-article-class'})],
        'https://capitalfinance.lesechos.fr/': [('div', {'class': 'post-entry'})],
        'https://www.leparisien.fr/': [('div', {'class': 'post-entry'})],
        'https://www.lesechos.fr/': [('div', {'class': 'post-entry'})],
        'https://www.boursorama.com': [('div', {'class': 'some-article-class'})],
        'https://www.avantages.ca/': [('div', {'class': 'post-entry'})],
        'https://www.allnews.ch/': [('div', {'class': 'post-entry'})],
        'https://www.zonebourse.com/': [('div', {'class': 'post-entry'})],
        'https://www.greenunivers.com/': [('div', {'class': 'content-article'})],
        'https://www.lefigaro.fr/': [('div', {'class': 'post-entry'})],
        'https://www.usine-digitale.fr/': [('div', {'class': 'post-entry'})],
        'https://www.menara.ma/': [('div', {'class': 'post-entry'})],
        'https://www.agefi.fr/': [('div', {'class': 'post-entry'})],
        'https://www.cfnews.net/': [('div', {'class': 'post-entry'})]
    }
    
    selector = custom_selectors.get(url)
    if selector:
        articles = soup.find_all(*selector)
        print(f"Found {len(articles)} articles at {url}")
        
        for article in articles:
            title = article.find(['h1', 'h2', 'h3', 'a'])
            text = article.get_text(strip=True) if article else ""
            if title:
                title_text = title.get_text(strip=True)
                # Check for each keyword in the article title and text
                for keyword in keywords:
                    if keyword.lower() in title_text.lower() or keyword.lower() in text.lower():
                        print(f"Keyword '{keyword}' found in article: {title_text}")
                        write_to_file(url, title_text, text)
                        break
            else:
                print("No title found for an article.")
    else:
        print(f"No custom selector found for {url}")

if __name__ == "__main__":
    urls = [
        'https://www.leconomiste.com/', 
        'https://capitalfinance.lesechos.fr/',
        'https://www.leparisien.fr/',
        'https://www.lesechos.fr/',
        'https://www.boursorama.com',
        'https://www.avantages.ca/',
        'https://www.allnews.ch/',
        'https://www.zonebourse.com/',
        'https://www.greenunivers.com/',
        'https://www.lefigaro.fr/',
        'https://www.usine-digitale.fr/',
        'https://www.menara.ma/',
        'https://www.cfnews.net/',
        'https://www.agefi.fr/'
    ]
    for url in urls:
        scrape_site(url)