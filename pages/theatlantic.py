import json
import requests
import streamlit as st 
from bs4 import BeautifulSoup
from datetime import datetime

with open('style.css') as f:
	st.markdown(f"<style> {f.read()} </style>",unsafe_allow_html=True)

c1,c2 = st.columns([2,10])
c1.image("https://logovectordl.com/wp-content/uploads/2021/01/the-atlantic-logo-vector.png")



@st.cache_data
def getSections():
	r = requests.get('https://www.theatlantic.com/world/')
	soup = BeautifulSoup(r.content, 'html.parser')
	sections = soup.find_all('div', attrs={'data-event-element':'sections'})[0].find_all('ul')[0].find_all('a')
	items = {}
	for x in sections:
		items[x.text] = 'https://www.theatlantic.com'+x['href'] if 'https://www.theatlantic.com' not in x['href'] else x['href']
	return items


sections = getSections()
sections['Books'] = sections['Books'] + '/all'
# st.write(sections)
keys_display = [x for x in sections.keys() if x not in ['Newsletters','Fiction','Photo','Culture','Planet','Audio','Features','Events','Washington Week','Progress']]
section_selected = st.radio('Section', keys_display, horizontal=True)

@st.cache_data
def getStories(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	articles = soup.find('div', attrs={'data-event-module': "collection"}).find_all('article')
	items = []
	for article in articles:
		try:
			author = article.find('div').find(attrs={'data-event-element':'author'}).text
		except:
			author = ''

		try:
			t = article.find('div').find('time').text if article.find('div').find('time') else ""
		except:
			t = ''

		try:
			img = article.find('img')['srcset'].split(',')[-1].strip().split(' ')[0]
		except:
			img = 'https://variety.com/wp-content/uploads/2020/05/the-atlantic.png'

		try:
			p = article.find('p').text
		except:
			p = ''

		items.append({
			'url': article.find('a')['href'],
			'title': article.find('h3').text.strip(),
			'subtitle': p,
			'time': t,
			'author': author,
			'img': img
			})

	return items


@st.dialog('💎', width='large')
def loadPremiumArticle(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	h1 = soup.find('h1').text
	subheader = soup.find('p', attrs={'class':"ArticleDek_root__P3leE"}).text
	author = soup.find('address').text
	imgsrc = soup.find('figure', class_='ArticleLeadFigure_root__Bj81R').find('img')['src']
	caption = soup.find('figure', class_='ArticleLeadFigure_root__Bj81R').find('figcaption').text
	body = soup.find('section', attrs={'data-event-module':"article body"})
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

storyriver = getStories(sections[section_selected])
# st.write(storyriver)

st.divider()
cols = st.columns(4)
for i, item in enumerate(storyriver):
	c = cols[i%len(cols)]
	c.image(item['img'], use_container_width=True)
	if c.button(item['title']):
		loadPremiumArticle(item['url'])
	if item['author'] or item['time']:
		c.markdown(f'''
			<style>  </style>
			<p> {item['subtitle']} </p>
			<small> {item['author']} {item['time']} </small>
			<hr>
		''',
		unsafe_allow_html=True)
	else:
		c.markdown(f'''
			<style>  </style>
			<p> {item['subtitle']} </p>
			<hr>
		''',
		unsafe_allow_html=True)
