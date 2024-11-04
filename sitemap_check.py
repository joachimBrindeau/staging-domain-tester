import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv
import os
from tqdm import tqdm

def get_domain(url):
    return urlparse(url).netloc

def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    return [element.text for element in soup.findAll('loc')]

def test_url(url, staging_domain):
    staging_url = url.replace(urlparse(url).netloc, staging_domain)
    try:
        response = requests.get(staging_url, timeout=10)
        return (staging_url, response.status_code)
    except requests.RequestException:
        return (staging_url, "Error")

def write_results_to_csv(filename, results):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Code"])
        writer.writerows(results)

def process_urls(urls, staging_domain, existing_results=None):
    results = []
    not_found_count = 0
    error_count = 0

    for i, url in enumerate(urls, 1):
        if existing_results:
            existing_result = next((r for r in existing_results if r[0] == url), None)
            if existing_result and existing_result[1] != '404':
                results.append(existing_result)
                continue

        result = test_url(url, staging_domain)
        results.append(result)

        if result[1] == 404:
            not_found_count += 1
        elif result[1] == "Error":
            error_count += 1

        status = f"{'🔴' if result[1] == 404 else '🟢' if result[1] == 200 else '🟡'}"
        
        # Extract the path from the URL
        path = urlparse(result[0]).path
        
        print(f"{i}/{len(urls)} {status} {result[0]} | Code: {result[1]} | 404: {not_found_count}, Errors: {error_count}")

    return results, not_found_count, error_count

def main():
    sitemap_url = input("Enter sitemap URL: ")
    staging_domain = input("Enter staging domain: ")

    sitemap_domain = get_domain(sitemap_url)
    filename = f"{sitemap_domain}.csv"

    if os.path.exists(filename):
        print("A previous result file exists for this domain.")
        action = input("Enter 'ALL' to retest all pages, or enter a status code (e.g. '404') to retest pages with that status code: ")
        
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            old_results = list(reader)[1:]  # Skip header
        
        if action.upper() == 'ALL':
            urls = get_urls_from_sitemap(sitemap_url)
            results, not_found_count, error_count = process_urls(urls, staging_domain)
        else:
            code = action
            urls_to_retest = [r[0].replace(staging_domain, get_domain(sitemap_url)) for r in old_results if r[1] == code]
            results, not_found_count, error_count = process_urls(urls_to_retest, staging_domain, old_results)
    else:
        urls = get_urls_from_sitemap(sitemap_url)
        results, not_found_count, error_count = process_urls(urls, staging_domain)

    write_results_to_csv(filename, results)
    print(f"\nResults have been written to {filename}")
    print(f"Total 404 errors: {not_found_count}")
    print(f"Total request errors: {error_count}")

if __name__ == "__main__":
    main()
