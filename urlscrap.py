import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

def link_checker(url):
    valid_links = []
    broken_links = []

    parse_url = urlparse(url)
    base_url = f"{parse_url.scheme}://{parse_url.netloc}"

    try:
        content = requests.get(url).content
    except requests.exceptions.RequestException:
        print(f"Failed to retrieve the content of {url}")
        return valid_links, broken_links

    parse_content = BeautifulSoup(content,'html.parser')
    links = parse_content.find_all('a')

    for link in links:
        href = link.get('href')
        if href.startswith('http'):
            href = href
        else:
            n_href = base_url + href
            href = n_href
        try:
            status = requests.head(href)
            if status.status_code == 200:
                valid_links.append(href)
            else:
                broken_links.append((url,href))

        except requests.exceptions.RequestException:
            broken_links.append((url, href))

    return valid_links, broken_links

def save_links_to_tsv(valid_links, broken_links):
    with open("links.tsv", "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["Links", "Status"])

        for link in valid_links:
            writer.writerow([link, "Valid"])

        for page_url, broken_link in broken_links:
            writer.writerow([broken_link, "broken"])



if __name__ == '__main__':
    url = 'https://github.com/Gauravraj1141/urlscrapper'
    valid_links,broken_links = link_checker(url)
    print(f"Total links checked: {len(valid_links) + len(broken_links)}")
    print(f"Valid links: {len(valid_links)}")
    print(f"Broken links: {len(broken_links)}")
    # print(valid_links,broken_links)
    save_links_to_tsv(valid_links,broken_links)


