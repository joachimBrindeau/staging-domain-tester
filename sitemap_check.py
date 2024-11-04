import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv
import os

def get_domain(url):
    domain = urlparse(url).netloc
    return domain

def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [element.text for element in soup.findAll('loc')]
    return urls

def test_url(url, staging_domain):
    staging_url = url.replace(url.split('/')[2], staging_domain)
    response = requests.get(staging_url)
    result = (staging_url, response.status_code)
    return result

def write_results_to_csv(filename, results):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Code"])
        for result in results:
            writer.writerow(result)

# Ask for sitemap url
sitemap_url = input("Enter sitemap url: ")

# Ask for staging domain
staging_domain = input("Enter staging domain: ")

sitemap_domain = get_domain(sitemap_url)
filename = f"{sitemap_domain}.csv"

if os.path.exists(filename):
    print("A previous result file exists for this domain.")
    action = input("Enter 'ALL' to retest all pages, or enter a status code (e.g. '404') to retest pages with that status code: ")
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        old_results = list(reader)
        if action.upper() == 'ALL':
            urls = get_urls_from_sitemap(sitemap_url)
            results = [test_url(url, staging_domain) for url in urls]
        else:
            results = old_results
            code = int(action)
            for i, result in enumerate(results):
                if i == 0:
                    continue
                if int(result[1]) == code:
                    url = result[0].replace(staging_domain, get_domain(sitemap_url))
                    results[i] = test_url(url, staging_domain)
else:
    urls = get_urls_from_sitemap(sitemap_url)
    results = [test_url(url, staging_domain) for url in urls]

write_results_to_csv(filename, results)