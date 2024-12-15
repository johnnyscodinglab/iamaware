import json
import requests
import streamlit as st 
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

c1,c2 = st.columns([2,10])
c1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/2560px-Wired_logo.svg.png")
st.divider()

@st.cache_data
def getStories():
	items = []
	for page in range(1,3):
		r = requests.get(f'https://www.wired.com/search/?q=&page={page}&sort=publishdate%20desc&format=json')
		items+=json.loads(r.content)['search']['items']
	return items


@st.dialog('💎', width='large')
def loadPremiumArticle(s):

	url = 'https://www.wired.com'+s['url']
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	h1 = s['source']['hed']
	subheader = s['source']['dek']
	try:
		author = ', '.join([x['name'] for x in s['contributors']['author']['items']])
	except:
		author = ''
	imgsrc = s['image']['sources']['xxl']['url']
	caption = s['image']['altText']
	body = soup.find('div', attrs={'class':"body__inner-container"})
	if not body:
		body = soup.find('div',attrs={'data-attribute-verso-pattern' : "gallery-body"})
	st.markdown(f"""
		<h1>{h1} </h1>
		<h3> {subheader} </h3>
		<small> {author} </small>
		<img src="{imgsrc}">
		<small style='color:gray;font-style: italic'> {caption} </small>
		<p></p>
		{body}
		<hr>
		""", unsafe_allow_html=True)

stories = getStories()

# st.write(stories)


cols = st.columns(4)

for i, story in enumerate(stories):
	c = cols[i%len(cols)]
	c.markdown(f'''
		<img src="{story['image']['sources']['lg']['url']}">
		<p></p>
	''', unsafe_allow_html=True)
	# c.image(story['image']['sources']['lg']['url'])
	if c.button(story['source']['hed']):
		loadPremiumArticle(story)
	c.markdown(f'''
		<p>{story['source']['dek']}</p>
		<small>{parse(story['pubDate'],'').strftime('%d %b %Y')} </small>
		<hr>
	''', unsafe_allow_html=True)
	# st.write(stories)