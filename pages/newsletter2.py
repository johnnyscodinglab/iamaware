import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
from pygooglenews import GoogleNews
from googlenewsdecoder import gnewsdecoder
import json
import pandas as pd

### FUNCTIONS ------------------------------------------------
@st.cache_data(show_spinner='Getting Images...')
def getImage(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        decoded_url = gnewsdecoder(link)['decoded_url']
        r = requests.get(decoded_url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.content, 'html.parser')
        meta = soup.find('meta', attrs={'property': 'og:image'})
        if meta and 'content' in meta.attrs:
            return meta['content']
    except Exception as e:
        print(f"Error with {link}: {e}")
    return None

# multiprocessing wrapper

def get_images_parallel(links, max_workers=15):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_link = {executor.submit(getImage, link): link for link in links}
        for future in as_completed(future_to_link):
            link = future_to_link[future]
            try:
                image_url = future.result()
                results[link] = image_url
            except Exception as e:
                print(f"Error with {link}: {e}")
                results[link] = None
    return results


@st.cache_data(show_spinner='Fetching News...')
def getNews(topic, from_dt, to_dt):
    search = gn.search(topic, from_=from_dt, to_=to_dt)
    return search['entries']

@st.cache_data(show_spinner ='Ranking Articles...')
def getCompletion(prompt):
    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    return json.loads(response.output_text)

### PAGE ------------------------------------------------
st.title('Newsletter 2.0')

client = OpenAI(api_key=st.secrets["openai_apikey"])
gn = GoogleNews(lang = 'en', country = 'IN')

timeformat = '%Y-%m-%d'
to_dt = datetime.now().strftime(timeformat)
from_dt = (datetime.today() - timedelta(days=6)).strftime(timeformat)

genainews = getNews('Generative AI', from_dt, to_dt)
llmnews = getNews('LargeLanguageModels', from_dt, to_dt)
titles = [x['title'].split('-')[0] for x in genainews] + [x['title'].split('-')[0] for x in llmnews]
titles = list(set(titles))
# st.write(titles)    
titles = ';'.join(x for x in titles)

# st.write(genainews[0])

RANKING_PROMPT = """
Act as an expert tech journalist and answer the following questions about the titles of the news articles presented to you.
Do not assume any other information if not present in the title
1. Is this news an academic paper - 0 (No), 1 for Yes
2. Is this a new product or a model or a partnership launch - (0/1)
3. Does this contain negative news (0-doest not contain /1 -contains)
4. Does this involve big Tech and AI companies like Google, microsoft, Alibaba, Amazon, Nvidia etc (0-No, 1-Yes)
5. Is this a major news outlet similar to NYT, WSJ, Guardian, Techcrunch etc (0 - No, 1-Yes)

### Output format
For each title in the input, 
STRICTLY return a LIST of JSON objects with each JSON object refers to
{'title':'Launch of new Model', 'academic':1, 'product_model_partnership':1, 'negative_news':0,'bigtech':0, 'major_publisher':0}

### INPUT: 
List of titles (separated by ;):
"""

# st.write(RANKING_PROMPT+titles)

out = getCompletion(RANKING_PROMPT+titles)
df = pd.DataFrame(out)
filtered = df[(df.major_publisher==1)& (df.academic==0)& (df.product_model_partnership == 1) & (df.negative_news==0)]
st.header(len(filtered))
st.write(filtered)