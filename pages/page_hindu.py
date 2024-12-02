import streamlit as st
import requests
from bs4 import BeautifulSoup


st.subheader('Only Premium articles from')
st.image('https://www.thehindu.com/theme/images/th-online/thehindu-logo.svg')

@st.cache_data
def scrapePages():
	links = []
	for page in [1,2]:
	    r =  requests.get(f'https://www.thehindu.com/premium/?page={page}')
	    soup = BeautifulSoup(r.content,  "html.parser")
	    result = soup.find_all('div', class_='result')[0]
	    divs = result.find_all('div', class_='element row-element')
	    maindiv = soup.find_all('div', class_='element main-row-element')[0]
	    equalrow = soup.find_all('div', class_='row equal-height')[0].find_all('div', class_='element')

	    for div in [maindiv] + equalrow + divs:
	        try:
	            img = div.find('div', class_='picture').find('img')['data-src-template']
	        except:
	            img = None
	        temp_dict = {
	            'title': div.find('h3').find('a').text.strip(),
	            'href': div.find('h3').find('a')['href'],
	            'img': img
	        }

	        if not temp_dict['title'] in [x['title'] for x in links]:
	        	links.append(temp_dict)
	return links

links = scrapePages()

@st.dialog('💎', width='large')
def loadPremiumArticle(i):
	a = requests.get(i['href'])
	soup = BeautifulSoup(a.content, 'html.parser')
	try:
		caption = soup.find('img', class_='lead-img')['title']
		leadimg = soup.find('picture').find('source')['srcset']
		subtitle =soup.find('h2', class_='sub-title').text
		authors = soup.find('div', class_='author-name').text.strip()
	except:
		caption = ''
		leadimg = ''
		subtitle = ''
		authors = ''
	
	body = soup.find('div',class_='articlebodycontent')
	
	children = []
	for child in body.findChildren(recursive=False):
	    el = child.find('div')
	    if not el:
	        children.append(str(child))
	
	st.title(i['title'])
	st.subheader(subtitle)
	st.write(authors)
	try:
		st.image(leadimg, caption=caption, use_container_width=True)
	except:
		pass

	st.write('\n'.join(children), unsafe_allow_html=True)

cols = st.columns(7, gap='small')
for i, item in enumerate(links):
	c = cols[i%len(cols)]
	try:
		img = c.image(item['img'].replace('SQUARE_80','SQUARE_140'), use_container_width=True)
	except:
		img = c.image('https://www.thehindu.com/theme/images/th-online/thumbnail-rectangle.svg', use_container_width=True)
	if c.button(f"{item['title']}", use_container_width=True):
		loadPremiumArticle(item)

