import streamlit as st
from pygooglenews import GoogleNews
from bs4 import BeautifulSoup
import requests
from googlenewsdecoder import gnewsdecoder
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed

# your existing function
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
        r = requests.get(decoded_url, headers=headers, timeout=10)
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
@st.cache_data(show_spinner='Getting Articles...')
def get_images_parallel(links, max_workers=10):
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

@st.cache_data()
def getNews(topic):
    search = gn.search(topic, when='24h')
    return search['entries']


# MAIN SCRIPT
gn = GoogleNews(lang = 'en', country = 'IN')
st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Google_News_icon.svg/1200px-Google_News_icon.svg.png', width=100)
st.title('Google News')
topic = st.text_input('Enter Topic :')

if topic:
    news = getNews(topic)

    images = get_images_parallel([x['link'] for x in news])

    cols = st.columns(4)
    for i, entry in enumerate(news):
        c = cols[i%len(cols)]
        c.markdown(f"#### {entry['title']}")
        img = images[entry['link']] if images[entry['link']] else 'https://www.stockvault.net/data/2019/01/28/259696/preview16.jpg'
        try:
            c.image(img)
        except:
            pass
        c.page_link(entry['link'], label="Read More...", icon='👉')
        c.divider()
else:
    st.write('Enter a topic to get news')

