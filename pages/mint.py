import json
import requests
import streamlit as st 
from bs4 import BeautifulSoup
from datetime import datetime


# st.subheader('Only Premium Articles from ')
c1,c2 = st.columns([2,10])
# c1.subheader('Only Premium Articles from ')
c1.image("https://logowik.com/content/uploads/images/mint-magazine8794.jpg")

def cleanhtml(htmlsoup):
	for element in htmlsoup.find_all(True):  # True gets all tags
		if element.string:  # Check if the element contains a string
			element.string = element.string.strip()
	return htmlsoup

@st.dialog('💎', width='large')
def loadPremiumArticle(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	h1 = soup.find('h1').string.strip()
	mainarea = soup.find('div', class_='mainArea')

	for element in mainarea.find_all(True):

		if element.string:
			element.string = element.string.strip()

		if element.string == 'View Full Image':
			element.string = ''

		if element.name == 'img':
			try:
				src = element.attrs['src']
			except:
				src = element.attrs['data-src']
				newframe = soup.new_tag("img", src=src, width="100%")
				element.replace_with(newframe)

		if element.name == 'figcaption':
			element['style'] = "color: gray; font-style: italic;font-size:0.9em;"

	fig = soup.find('picture').find('img')

	st.markdown(' '.join([x.strip() for x in f"""<div>
				<h1>{h1}</h1>
				{fig}
				<p></p>
				{mainarea}""".split()]), unsafe_allow_html=True)


links = []
for page in range(1,5):

	r = requests.get(f'https://www.livemint.com/premium/page-{page}')
	soup = BeautifulSoup(r.content, 'html.parser')
	tiles = soup.find_all('div', class_='listingNew')

	for div in tiles:
		temp_dict = {
		'title': div.find('h2').text.strip(),
		'href': 'https://www.livemint.com'+div.find('h2').find('a')['href'],
		'img': div.find('a').find('img')['src']
		}
		links.append(temp_dict)

cols = st.columns(6)
for i, link in enumerate(links):
	c = cols[i%len(cols)]
	try:
		img = c.image(link['img'], use_container_width=True)
	except:
		img = c.image('https://media.licdn.com/dms/image/v2/D5612AQGG_UNzA25jdA/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1727849138194?e=2147483647&v=beta&t=9LqRlgCQVZcO2z1SiKP8SyrVRn941ouVtK9T3FoLWiA', use_container_width=True)
	if c.button(link['title'], use_container_width=True):
		loadPremiumArticle(link['href'])