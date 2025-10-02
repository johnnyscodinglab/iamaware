import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
from pygooglenews import GoogleNews
from googlenewsdecoder import gnewsdecoder
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta


st.title('🤖AI News🤖')

topics = {
	'🧠Machine Learning': 'CAAqJggKIiBDQkFTRWdvSkwyMHZNREZvZVdoZkVnVmxiaTFIUWlnQVAB',
	'🤖 Artificial intelligence': 'CAAqJAgKIh5DQkFTRUFvSEwyMHZNRzFyZWhJRlpXNHRSMElvQUFQAQ',
	'⚛ Deep Learning': 'CAAqKAgKIiJDQkFTRXdvS0wyMHZNR2d4Wm00NGFCSUZaVzR0UjBJb0FBUAE',
	'📊Data and information visualization':'CAAqKAgKIiJDQkFTRXdvS0wyMHZNRFJtZW5JMVpCSUZaVzR0UjBJb0FBUAE',
	'🖼️Infographic': 'CAAqJggKIiBDQkFTRWdvSkwyMHZNRE40WTE5cUVnVmxiaTFIUWlnQVAB',
	'🐍Python': 'CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFY2TVY4U0JXVnVMVWRDS0FBUAE'
}

# your existing function
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


@st.cache_data(show_spinner='Getting News...')
def get_news(topics, end_date):
    gn = GoogleNews(lang = 'en', country = 'IN')
    news = {}
    for topic in topics:
        news[topic] = gn.topic_headlines(topics[topic])['entries']
    return news

today = datetime.today().strftime('%m/%d/%Y')
all_news = get_news(topics, today)

def display_news(section, topic, num_col=5, num_rows=1):
    news = all_news[topic][:num_col*num_rows]
    images = get_images_parallel([x['link'] for x in news])
    cols = section.columns(num_col, gap='medium')
    for i, n in enumerate(news):
        c = cols[i%len(cols)]
        img = images[n['link']] if images[n['link']] else 'https://static.vecteezy.com/system/resources/previews/001/257/159/non_2x/reading-hot-news-flat-design-concept-vector.jpg'
        c.html(f"""
        <a href="{n['link']}">
            <img src='{img}' width=100% height=140 
            style="border-radius: 10px; box-shadow: 0 0px 10px rgba(0,0,0,0.15); object-fit: cover">
        </a>
        <p></p>
        <strong style="color:#16a085">{n['source']['title']}</strong>
        <h6> {n['title'].split(' - ')[0]} </h6>
        """)

tabs = st.tabs(topics.keys())
for topic, tab in zip(topics.keys(), tabs):
    display_news(tab, topic, 5 , 3)
