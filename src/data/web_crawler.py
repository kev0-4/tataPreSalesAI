from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

def extract_links(base_url, start_page=1, end_page=2):
    href_links = []

    for page_number in range(start_page, end_page + 1):
        page_url = base_url.rstrip('/') + f"/page/{page_number}/"
        
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        
        # Find all 'a' tags within div with class 'o-brXWGL'
        links_div = page_soup.findAll("div", class_="o-brXWGL")

        for div in links_div:
            a_tags = div.findAll("a", href=True)
            for a in a_tags:
                href = a['href']
                full_link = "https://www.carwale.com" + href
                if full_link.startswith("https://www.carwale.com/tata-cars"):
                    href_links.append(full_link)
        print(len(href_links))
        print(len(set(href_links)))
    
    return href_links

# Example usage
# base_url = 'https://www.carwale.com/tata-cars/expert-reviews'
# all_links = extract_links(base_url)
# print(all_links)
# print(len(all_links))
