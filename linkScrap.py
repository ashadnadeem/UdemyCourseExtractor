__author__ = "Ashad Nadeem Mahmudi"
__date__ = "8/21/2020"

import requests
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

def is_valid(url):
    """Checks whether `url` is a valid URL."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """Returns all URLs that is found on `url` in which it belongs to the same website"""

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path +"?"+ parsed_href.query

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print("[!] External link: " + href)
                external_urls.add(href)
            continue
        print("[*] Internal link: " + href)
        internal_urls.add(href)
    return internal_urls, external_urls

def write_urls_to_file(filename, list):
    with open(filename,'w') as file:
        for link in list:
            file.write(link + "\n")
    print("Write Complete")

if __name__ == "__main__":
    _,eUrls = get_all_website_links("https://yofreesamples.com/courses/free-discounted-udemy-courses-list/")
    links = list()
    for extUrl in eUrls:
        if re.match(r"^https://www.udemy.com/course/", extUrl):
            links.append(extUrl)
    print(links)

    write_urls_to_file("UdemyLinks.txt", links)

    print("Total Udemy Links: ", (len(links)))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total:", len(external_urls) + len(internal_urls))
