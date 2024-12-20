import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def download_urls(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def scrape_page(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service('/usr/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    screenshot_path = f"reports/{url.replace('https://', '').replace('/', '_')}.png"
    driver.save_screenshot(screenshot_path)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.title.string if soup.title else 'Sin título'
    body_attributes = soup.body.attrs if soup.body else {}

    driver.quit()

    return {
        'url': url,
        'title': title,
        'body_attributes': body_attributes,
        'screenshot': screenshot_path
    }

def generate_report(data):
    os.makedirs('reports', exist_ok=True)
    report_path = 'reports/report.html'
    with open(report_path, 'w') as f:
        f.write('<html><body>')
        f.write('<h1>Reporte de Scraping</h1>')
        for entry in data:
            f.write(f"<h2>{entry['title']}</h2>")
            f.write(f"<p>URL: {entry['url']}</p>")
            f.write(f"<p>Body Attributes: {entry['body_attributes']}</p>")
            f.write(f"<img src='{entry['screenshot']}' alt='Screenshot' style='max-width:500px;'>")
        f.write('</body></html>')
    return report_path

if __name__ == '__main__':
    url_file = "https://example.com/urls.txt"
    urls = download_urls(url_file)
    data = [scrape_page(url) for url in urls]
    report = generate_report(data)
    print(f"Reporte generado: {report}")