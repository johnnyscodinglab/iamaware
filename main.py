import streamlit as st
import requests
import json
from datetime import datetime


st.set_page_config(layout="wide")

apiKey = st.secrets["newsapikey"]

st.title(':bullettrain_front: THE JOHNNY\'S EXPRESS ')


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
	r = requests.get(f'https://newsapi.org/v2/everything?domains=thenextweb.com&sortBy=popularity&apiKey={api}')
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

menu  = st.selectbox('Select:', ['HOME','SEARCH'], 0)

if menu == 'HOME':
	topHeadlines = getTopHeadlines(apiKey)
	topHeadlines = [x for x in topHeadlines if x['title'] != "[Removed]"]
	# st.write(sources)


	# st.write(topHeadlines[1])

	

	master_col = st.columns(2, gap='large')
	master_col[0].header('Top Headlines')
	columns = master_col[0].columns(3, gap='small')
	for i, item in enumerate(topHeadlines[:15]):

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
		    ''',
		    unsafe_allow_html=True
		)
		c.divider()

	master_col[1].header('Category wise')


	technews = getTechNews(apiKey)
	technews = [x for x in technews if x['title'] != "[Removed]"]
	master_col[1].subheader(f'TECHCRUNCH ({len(technews)}+)')

	for i, item in enumerate(technews[:3]):
		c1,c2 = master_col[1].columns([2,8])
		# c1.write(date)
		c1.image(item['urlToImage'] if item['urlToImage'] else defaultimg)
		c2.markdown(f'''
		    <a href="{item['url']}" style="text-decoration:none;color:inherit;">
				<h5 style="margin:2pt 0;padding:0"> {item['title'].split(' - ')[0]} </h5>
				<p> {item['description'] if item['description'] else '' } </p>
		    </a>''',
		    unsafe_allow_html=True
		)

	master_col[1].divider()
	# GET https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=d97a5473c5a6484fb5b7995b231e7df0
	technews = getTechNews(apiKey)
	genAInews = getGenAI(apiKey)
	genAInews = [x for x in genAInews if x['title'] != "[Removed]"]

	master_col[1].subheader(f'Generative AI ({len(genAInews)}+)')
	for i, item in enumerate(genAInews[:5]):
		c1,c2 = master_col[1].columns([2,8])
		# c1.write(date)
		c1.image(item['urlToImage'] if item['urlToImage'] else defaultimg)
		c2.markdown(f'''
		    <a href="{item['url']}" style="text-decoration:none;color:inherit;">
				<small style="margin:0;padding:0"> {item['source']['name'].upper()} </small>
				<h5 style="margin:2pt 0;padding:0"> {item['title'].split(' - ')[0]} </h5>
				<p> {item['description'] if item['description'] else '' } </p>
		    </a>''',
		    unsafe_allow_html=True
		)

	master_col[1].divider()

elif menu == 'SEARCH':
	
	c1,c2,c3 = st.columns(3)
	
	query = c1.text_input('Search Query :')
	sortBy = c2.selectbox('Sort By :', ['relevancy','popularity','publishedAt'])
	fromdate = c3.date_input('FROM :')

	cols = st.columns(10)
	sources = [x for x in sources if x['country'] in ('us','in')]
	sources = [x for x in sources if x['category'] in ('science','technology','business','general','health')]
	# st.write(set([x['category'] for x in sources]))
	# for i, source in enumerate(sources):
	# 	cols[i%len(cols)].checkbox(source['name'], value=source['id'])

	if query:
		@st.cache_data
		def getQueryArticles(query, sortBy, fromdate, api):
			u = f"""https://newsapi.org/v2/everything?q="{query}"&sortBy={sortBy}&from={fromdate}&language=en&apiKey={api}""".replace(' ','%20')
			# st.write(u)
			r = requests.get(u)
			return json.loads(r.text)['articles']
		articles = getQueryArticles(query, sortBy, fromdate, apiKey)
		articles = [x for x in articles if x['title'] != "[Removed]"]
		# st.write(articles)	

		st.title(query.upper())

		columns = st.columns(5, gap='small')
		for i, item in enumerate(articles):

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
			    ''',
			    unsafe_allow_html=True
			)
			c.divider()
