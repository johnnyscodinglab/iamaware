import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


st.set_page_config(layout="wide")

apiKey = st.secrets["newsapikey"]

# st.markdown("<img src='logo.png'>")
st.image('logo.png', width=200)
# st.title(':bullettrain_front: THE JOHNNY\'S EXPRESS ')


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

menu  = st.selectbox('Select:', ['HOME','SEARCH','HINDU PREMIUM'], 0)

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
	
	query = c1.text_input('Topic :', placeholder='Bitcoin')
	sortBy = c2.selectbox('Sort By :', ['relevancy','popularity','publishedAt'], 1)
	yesterday = datetime.now() - timedelta(1)
	fromdate = c3.date_input('FROM :', yesterday)

	cols = st.columns(10)
	sources = [x for x in sources if x['country'] in ('us','in')]
	sources = [x for x in sources if x['category'] in ('science','technology','business','general','health')]

	if query:
		@st.cache_data
		def getQueryArticles(query, sortBy, fromdate, api):
			u = f"""https://newsapi.org/v2/everything?q="{query.lower().replace(' ','%20')}"&sortBy={sortBy}&from={fromdate}&language=en&apiKey={api}""".replace(' ','%20')
			r = requests.get(u)
			return json.loads(r.text)['articles']
		articles = getQueryArticles(query, sortBy, fromdate, apiKey)
		articles = [x for x in articles if x['title'] != "[Removed]"]

		st.title(query.upper())

		columns = st.columns(5, gap='small')
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

elif menu == 'HINDU PREMIUM':
	
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
		caption = soup.find('img', class_='lead-img')['title']
		leadimg = soup.find('picture').find('source')['srcset']
		body = soup.find('div',class_='articlebodycontent')
		
		children = []
		for child in body.findChildren(recursive=False):
		    el = child.find('div')
		    if not el:
		        children.append(str(child))
		
		st.title(i['title'])
		st.image(leadimg, caption=caption, use_container_width=True)
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
