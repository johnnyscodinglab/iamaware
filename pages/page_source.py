import streamlit as st
import requests
import json
from datetime import datetime

@st.cache_data
def getSources(api):
	r = requests.get(f'https://newsapi.org/v2/top-headlines/sources?apiKey={api}&language=en')
	return json.loads(r.text)['sources']

@st.cache_data
def getTechNews(api, d):
	url = f'https://newsapi.org/v2/everything?domains={d}&apiKey={api}&sortBy=publishedAt&language=en'
	# st.write(url)
	r = requests.get(url)
	return json.loads(r.text)

apiKey = st.secrets["newsapikey"]
defaultimg = 'https://images.unsplash.com/photo-1495020689067-958852a7765e?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

sources = getSources(apiKey)
# st.write(sources)
# st.subheader('Choose your Source')
# restrict to .com domains
sources = [x for x in sources if '.com' in x['url']]
for x in sources:
	x['domain'] = x['url'].replace('https:','').replace('http:','').replace('/','').replace('www.','')
sources = [x for x in sources if len(x['domain'].split('.')) == 2]
sources = [x for x in sources if x['country'] in ['us','in']]
source_name = st.selectbox('Select Source : ', [x['name'] for x in sources], 5)
# st.write(sources)
domain = [x['domain'] for x in sources if x['name'] == source_name][0]
# st.write(source_name, domain)

news = getTechNews(apiKey, domain)['articles']
# st.write(news)


st.title(source_name)
columns = st.columns(4, gap='large')

for i, item in enumerate(news[:49]):

	c = columns[i%len(columns)]
	date = datetime.strptime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %b %Y')

	c.markdown(f'''
		
	    <a href="{item['url']}" style="text-decoration:none;color:inherit;background-image:url({item['urlToImage'] if item['urlToImage'] else defaultimg}); background-position:center top; background-size:cover;display:block; height:400px">
			<h5 style="bottom:0;margin:5pt 0;padding:20px;color:white;background:rgba(0,0,0,1);"> {item['title'].split(' - ')[0]} </h5>
	    </a>
	    <p></p>
	    ''',
	    unsafe_allow_html=True
	)
