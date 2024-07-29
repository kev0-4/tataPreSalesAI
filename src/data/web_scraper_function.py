from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import google.generativeai as genai
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_data(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    
    # Find the h1 element with class name "o-cscLpt o-fzoTnS" and store it in a title variable
    title_tag = page_soup.find("h1", class_="o-cscLpt o-fzoTnS")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"
    
    data = []
    
    # Find all parent divs with class name "o-fzptYr o-fznVmz"
    parent_divs = page_soup.findAll("div", class_="o-fzptYr o-fznVmz")
    
    for parent_div in parent_divs:
        # Find the heading class name "o-Hyyko o-bPYcRG"
        heading_tag = parent_div.find("h2", class_="o-Hyyko o-bPYcRG")
        heading = heading_tag.get_text(strip=True) if heading_tag else None
        
        # Handle the special cases
        if heading in ["Why would I buy it?", "Why would I avoid it?"]:
            # Extract all span elements with class "o-fzptZU o-jjpuv" for special cases
            span_elements = parent_div.findAll("span", class_="o-fzptZU o-jjpuv")
            paragraph_content = '. '.join(span.get_text(strip=True) for span in span_elements)
            if not paragraph_content.endswith('.'):
                paragraph_content += '.'
        else:
            # Find the paragraph content in the div with class name "udlDPq articleContent"
            paragraph_div = parent_div.find("div", class_="udlDPq articleContent")
            paragraph_content = paragraph_div.get_text(strip=True) if paragraph_div else None
        
        if heading and paragraph_content:
            data.append({heading: paragraph_content})
    
    response = model.generate_content(f"Find and return only the car name from this, dont write anything else except the name. {title}")
    title_cleaned = response.text.strip() if response.text else title
    return {title_cleaned: data}

