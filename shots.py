import os
import requests
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime

# Function to fetch and parse sitemap
def fetch_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()
    return ET.fromstring(response.content)

# Function to extract URLs from sitemap XML
def extract_urls(sitemap_xml):
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [url.text for url in sitemap_xml.findall('.//ns:url/ns:loc', namespace)]

# Create a folder with the current date
date_str = datetime.now().strftime('%Y-%m-%d')
folder_name = f'screenshots_{date_str}'
os.makedirs(folder_name, exist_ok=True)

# Fetch and parse the sitemap
sitemap_url = 'https://docs.runpod.io/sitemap.xml'
sitemap_xml = fetch_sitemap(sitemap_url)

# Extract URLs
urls = extract_urls(sitemap_xml)

# Loop through each URL and take a screenshot
for url in urls:
    file_name = url.replace('https://', '').replace('/', '_') + '.png'
    file_path = os.path.join(folder_name, file_name)
    subprocess.run(['shot-scraper', url, '-o', file_path])

print("Screenshots taken and saved in the folder:", folder_name)
