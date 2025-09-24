import streamlit as st 
from templates.template01 import *
from openai import OpenAI
from pygooglenews import GoogleNews
from googlenewsdecoder import gnewsdecoder
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from datetime import date
from fpdf import FPDF


st.title('Newsletter')
client = OpenAI(api_key=st.secrets["openai_apikey"])
gn = GoogleNews(lang = 'en', country = 'IN')


# st.html(f"{HTMLPROMPT}".format(CSS=CSS, ISSUE='01', DATE='March 30, 2026'))


@st.cache_data(show_spinner='Fetching GenAI News...')
def getNews(topic):
    search = gn.search(topic, when='24h')
    return search['entries']

genainews = getNews('Generative AI')
llmnews = getNews('LargeLanguageModels')
titles = [x['title'] for x in genainews] + [x['title'] for x in llmnews]
titles = ';'.join(x for x in titles)

PROMPT = f"""
Act as an expert tech journalist and rank the following titles of news articles 
in the order of popularity and how important the news is about Generative AI. 
Return the output as list of titles without changing the format. 
Filter top 10 articles

List of titles in as Python list : {titles}
### Output format
STRICTLY RETURN Python List of input titles
"""

SUMMARYPROMPT = """
Generate a 100 word consice yet informative summary covering key points of the article.
Output format should be just JSON output in plain text summary of article. Don't write any leading statements.
Here is the article to summarize.
Article: {}
"""

@st.cache_data(show_spinner ='Getting Top Articles...')
def getCompletion(prompt):

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    return json.loads(response.output_text)

out = getCompletion(PROMPT)
# st.write(out)

news = genainews + llmnews
news = [x for x in news if x['title'] in out]


def clean_article_html(html_content):
    """
    Cleans raw HTML content and extracts readable text.
    Removes scripts, styles, ads, and unnecessary tags.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # remove unwanted tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "form", "iframe", "svg", "button", "nav", "aside"]):
        tag.decompose()

    # get text
    text = soup.get_text(separator=" ", strip=True)

    # collapse multiple spaces/newlines
    text = " ".join(text.split())

    return text

def getArticleData(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    print(f'Getting article for link: {link}')
    try:
        decoded_url = gnewsdecoder(link)['decoded_url']
        r = requests.get(decoded_url, headers=headers, timeout=10)
        print(r.status_code)
        if r.status_code != 200:
            return {"link": decoded_url, "image": None, "body": None}
        
        soup = BeautifulSoup(r.content, "html.parser")

        # --- extract image ---
        image_url = None
        meta = soup.find("meta", attrs={"property": "og:image"})
        if meta and "content" in meta.attrs:
            image_url = meta["content"]
        else:
            print('Image URL not found')

        # --- extract main body ---
        # Heuristic: most articles are inside <article>, or <div> with "content" in class/id
        article_tag = soup.find("article")
        if not article_tag:
            article_tag = soup.find("div", attrs={"class": lambda x: x and "content" in x.lower()}) \
                        or soup.find("div", attrs={"id": lambda x: x and "content" in x.lower()})

        article_body = article_tag.get_text(" ", strip=True) if article_tag else soup.get_text(" ", strip=True)

        # --- clean text ---
        clean_text = clean_article_html(article_body)

        return {"link": decoded_url, "image": image_url, "body": clean_text}

    except Exception as e:
        print(f"Error with {link}: {e}")
        return {"link": decoded_url, "image": None, "body": None}


@st.cache_data(show_spinner='Getting Articles...')
def get_articles_parallel(links, max_workers=10):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_link = {executor.submit(getArticleData, link): link for link in links}
        for future in as_completed(future_to_link):
            link = future_to_link[future]
            try:
                article_data = future.result()  # returns dict: {link, image, body}
                results[link] = article_data
            except Exception as e:
                print(f"Error with {link}: {e}")
                results[link] = {"link": link, "image": None, "body": None}
    return results                                                                                                         


content = get_articles_parallel([x['link'] for x in news])
# st.subheader('Content')

# Filter articles with both content > 100 words and having an image
content = {k:v for k,v in content.items() if v['body'] and v['image']}
content = {k:v for k,v in content.items() if len(v['body'].split(' ')) > 100}

news = [x for x in news if x['link'] in content.keys()]
for item in news:
    body = [v['body'] for k,v in content.items() if k==item['link']][0]
    item['body'] = body
    item['image'] = [v['image'].split('?')[0] for k,v in content.items() if k==item['link']][0]
    summary = getCompletion(SUMMARYPROMPT.format(body))
    item['summary'] = summary['summary']



LISTOFTITLES = '\n'.join([f"<li>{x['title'].split('-')[0]}</li>" for x in news])
T1, S1, I1 = news[0]['title'], news[0]['summary'], news[0]['image']
T2, S2, I2 = news[1]['title'], news[1]['summary'], news[1]['image']
T3, S3, I3 = news[2]['title'], news[2]['summary'], news[2]['image']
T4, S4, I4 = news[3]['title'], news[3]['summary'], news[3]['image']
T5, S5, I5 = news[4]['title'], news[4]['summary'], news[4]['image']
DATE = date.today().strftime("%d %B %Y")
html_formatted = HTMLPROMPT.format(
    CSS=CSS, 
    ISSUE='01', 
    DATE= DATE, 
    LISTOFTITLES=LISTOFTITLES, 
    T1=T1, S1=S1, I1=I1,
    T2=T2, S2=S2, I2=I2,
    T3=T3, S3=S3, I3=I3,
    T4=T4, S4=S4, I4=I4,
    T5=T5, S5=S5, I5=I5,
    )
st.html(html_formatted)

# def html_to_pdf(html_content, filename="output.pdf"):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
    
#     # Convert HTML to plain text (basic handling, no styling)
#     # For advanced HTML → PDF, you’d use `pdfkit` or `weasyprint`
#     import re
#     text = re.sub("<[^<]+?>", "", html_content)  # strip HTML tags
    
#     pdf.multi_cell(0, 10, text)
#     pdf.output(filename)
#     return filename

# # Convert and make downloadable
# pdf_file = html_to_pdf(html_formatted, f"newsletter_{DATE}.pdf")

# with open(pdf_file, "rb") as f:
#     st.download_button(
#         label="📥 Download PDF",
#         data=f,
#         file_name=f"newsletter_{DATE}.pdf",
#         mime="application/pdf"
#     )