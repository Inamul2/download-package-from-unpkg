import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os


def download_file(path, name, url):
    file_path = path.split(name)[1]
    pat = file_path.rsplit('/', 1)
    if len(pat) > 1 and not os.path.isdir(pat[0]):
        os.makedirs(pat[0])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(requests.get(path).text)

def get_all_links_inside_folder(folder_link):
    req = Request(folder_link)
    try:
        html_page = urlopen(req)
    except:
        return ['']

    soup = BeautifulSoup(html_page, "html.parser")

    links = []
    for link in soup.find_all("a", class_="css-xt128v"):
        if link.get('title') not in ["Parent directory"]:
            if "/" not in link.get('href'):
                links.append(folder_link + link.get('href'))
            else:
                links = links + get_all_links_inside_folder(folder_link = folder_link+link.get('href'))
    
    return links    


#url = "https://unpkg.com/browse/react@18.2.0/"

url = input("Enter the url : ")
name = url.split("browse/")[-1]

k = get_all_links_inside_folder(url)

for l in k:
    if l:
        download_file(l.replace("browse/",""), name, url)

