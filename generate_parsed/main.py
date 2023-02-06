import requests
from bs4 import BeautifulSoup

with open("links.txt", "r") as links_file:
    with open("parsed.txt", "w") as parsed_file:
        for page in links_file:
            page = page.strip()
            res = requests.get(page)
            soup = BeautifulSoup(res.content, "html.parser")
            for p in soup.find_all("p")[6:-1]:
                text = p.text
                text = text.replace('\n', ' ')
                if text.endswith("¶"):
                    text = text[:-1]
                parsed_file.write(text + " ")
            parsed_file.write('\n')

with open("parsed.txt", "r") as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        print(line)