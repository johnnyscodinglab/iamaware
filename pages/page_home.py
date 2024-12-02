import streamlit as st
import requests
import json
from datetime import datetime, timedelta

c,c1 = st.columns([1,7])
c.image("logo.png")

apiKey = st.secrets["newsapikey"]

@st.cache_data
def getSources(api):
	r = requests.get(f'https://newsapi.org/v2/top-headlines/sources?apiKey={api}&language=en')
	return json.loads(r.text)['sources']

@st.cache_data
def getTopHeadlines(api):
	r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api}')
	return json.loads(r.text)['articles']

@st.cache_data
def getTechNews(api):
	r = requests.get(f'https://newsapi.org/v2/everything?domains=techcrunch.com&apiKey={api}')
	return json.loads(r.text)['articles']

@st.cache_data
def getGenAI(api):
	r = requests.get(f'https://newsapi.org/v2/everything?q="LLM"&sortBy=popularity&excludeDomains=pypi.org&language=en&apiKey={api}')
	return json.loads(r.text)['articles']


sources = getSources(apiKey)
defaultimg = 'https://images.unsplash.com/photo-1495020689067-958852a7765e?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'



topHeadlines = getTopHeadlines(apiKey)
topHeadlines = [x for x in topHeadlines if x['title'] != "[Removed]"]
master_col = st.columns(2, gap='large')
master_col[0].title('Top News')
columns = master_col[0].columns(2, gap='small')

for i, item in enumerate(topHeadlines[:5]):

	c = columns[i%len(columns)]
	date = datetime.strptime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %b %Y')

	c.markdown(f'''
		
	    <a href="{item['url']}" style="text-decoration:none;color:inherit;">
	        <img src="{item['urlToImage'] if item['urlToImage'] else defaultimg}" />
	        <small style="font-weight:bold"> {item['source']['name'].upper()} </small>
			<br>
			<small style="margin:5pt 0;padding:0; color:gray"> {date} </small>
			<h3 style="margin:5pt 0;padding:0"> {item['title'].split(' - ')[0]} </h3>
	    </a>
        <p> {item['description'] if item['description'] else '' } </p>
        <hr>
	    ''',
	    unsafe_allow_html=True
	)
	# c.divider()

# master_col[1].header('Category wise')

technews = getTechNews(apiKey)
technews = [x for x in technews if x['title'] != "[Removed]"]

a,t = master_col[1].columns([1,9])
a.image('https://yt3.googleusercontent.com/ytc/AIdro_kCWnlG0S5KmFxBckuWUwXOaIsmZL7hBkuXa4CFY27vtk_y=s900-c-k-c0x00ffffff-no-rj')
t.subheader(f'TechCrunch ({len(technews)}+)')


for i, item in enumerate(technews[:3]):
	master_col[1].markdown(f'''
			<a href="{item['url']}" style="text-decoration:none;color:inherit;">
			<h5 style="margin:2pt 0;padding:0"> {item['title'].split(' - ')[0]} </h5>
			<p> {item['description'] if item['description'] else '' } </p>
			</a>''',
		    unsafe_allow_html=True
			)

	# c1,c2 = master_col[1].columns([2,8])
	# # c1.write(date)
	# c1.image(item['urlToImage'] if item['urlToImage'] else defaultimg)
	# c2.markdown(f'''
	#     <a href="{item['url']}" style="text-decoration:none;color:inherit;">
	# 		<h5 style="margin:2pt 0;padding:0"> {item['title'].split(' - ')[0]} </h5>
	# 		<p> {item['description'] if item['description'] else '' } </p>
	#     </a>''',
	#     unsafe_allow_html=True
	# )

master_col[1].divider()
# GET https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=d97a5473c5a6484fb5b7995b231e7df0
technews = getTechNews(apiKey)
genAInews = getGenAI(apiKey)
genAInews = [x for x in genAInews if x['title'] != "[Removed]"]

master_col[1].subheader(f'Generative AI ({len(genAInews)}+)')
cols = master_col[1].columns(2)
for i, item in enumerate(genAInews[:5]):
	c = cols[i%len(cols)]
	# c.write(date)


	# c1,c2 = master_col[1].columns([2,8])
	# # c1.write(date)
	# c1.image(item['urlToImage'] if item['urlToImage'] else defaultimg)
	c.markdown(f'''
		<img src="{item['urlToImage'] if item['urlToImage'] else defaultimg}" >
	    <a href="{item['url']}" style="text-decoration:none;color:inherit;">
			<small style="margin:0;padding:0;font-weight:bold"> {item['source']['name'].upper()} </small>
			<br>
			<small style="margin:5pt 0;padding:0; color:gray"> {date} </small>
			<h5 style="margin:2pt 0;padding:0"> {item['title'].split(' - ')[0]} </h5>
			<hr>
	    </a>''',
	    unsafe_allow_html=True
	)
	# <p> {item['description'] if item['description'] else '' } </p>

master_col[1].divider()