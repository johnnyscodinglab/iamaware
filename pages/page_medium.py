import streamlit as st
from bs4 import BeautifulSoup
import requests


st.title('FREEDIUM')
st.markdown('**Read member only medium articles for free**')
input_url = st.text_input('Enter medium URL :')
if input_url:
	input_url = f"https://freedium.cfd/{input_url}"
	r = requests.get(input_url)
	soup = BeautifulSoup(r.content, 'html.parser')
	banner = soup.find('img')['src']		
	h1 = soup.find('h1')
	h3 = soup.find('h2').text
	maincontent = soup.find('div', class_='main-content')
	for element in maincontent.find_all(True):
		if 'class' in element.attrs:
			del element.attrs['class']
		if element.name == 'iframe':
			try:
				src = element.attrs['src']
				print(src)
				newframe = soup.new_tag("iframe", src=src, width="100%")
				element.replace_with(newframe)
			except:
				pass
				
		if element.name == 'img':
			# element.attrs['width'] = '100%'
			try:
				element.attrs['src'] = element.attrs['data-src']
			except:
				pass
		if element.name in ['p','li']:
			element.attrs['style'] = 'font-size:1.1em'
		if element.name == 'figcaption':
			element.attrs['style'] = 'font-size:0.9em; color:gray'
	c1,c2,c3 = st.columns([1,3,1])
	c2.markdown(f"""
		<div>
		<img src="{banner}" width="100%">
		<h1>{h1}</h1>
		<h3 style='color:gray'>{h3}</h3>
		{maincontent}
		</div>
		""", unsafe_allow_html=True)

