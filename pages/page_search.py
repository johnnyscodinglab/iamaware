import streamlit as st
import requests
import json
from datetime import datetime, timedelta


st.title('🔍Search by Topic')
apiKey = st.secrets["newsapikey"]

@st.cache_data
def getSources(api):
	r = requests.get(f'https://newsapi.org/v2/top-headlines/sources?apiKey={api}&language=en')
	return json.loads(r.text)['sources']

sources = getSources(apiKey)
defaultimg = 'https://images.unsplash.com/photo-1495020689067-958852a7765e?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'


# c1,c2,c3,c4 = st.columns(4)
c1,c2,c3 = st.columns(3)

query = c1.text_input('Topic :', placeholder='Bitcoin')
sortBy = c2.selectbox('Sort By :', ['relevancy','popularity','publishedAt'], 1)
yesterday = datetime.now() - timedelta(1)
fromdate = c3.date_input('FROM :', yesterday)
# sources = getSources(apiKey)
# sources = [x for x in sources if x['country'] in ('us','in')]
# sources = [x for x in sources if x['category'] in ('science','technology','business','general','health')]
# source_names = [x['name'] for x in sources]
# source = c4.selectbox('SOURCE :',source_names)

cols = st.columns(10)


if query:

	@st.cache_data
	def getQueryArticles(query, sortBy, fromdate, api):
		u = f"""https://newsapi.org/v2/everything?q="{query.lower().replace(' ','%20')}"&sortBy={sortBy}&from={fromdate}&language=en&apiKey={api}""".replace(' ','%20')
		r = requests.get(u)
		return json.loads(r.text)['articles']

	articles = getQueryArticles(query, sortBy, fromdate, apiKey)
	articles = [x for x in articles if x['title'] != "[Removed]"]

	st.title(query.title())

	columns = st.columns(4)
	for i, item in enumerate(articles[:49]):

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