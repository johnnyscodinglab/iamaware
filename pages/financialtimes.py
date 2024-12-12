import json
import requests
import streamlit as st 
from bs4 import BeautifulSoup

c1,c2 = st.columns([1,10])
c1.image("https://upload.wikimedia.org/wikipedia/commons/0/0a/Financial_Times_corporate_logo_%28no_background%29.svg")


url = st.text_input('Enter FT URL :')
if url:
	url = f"https://removepaywalls.com/2/{url}"
	r = requests.get(url, timeout=20000)
	soup = BeautifulSoup(r.content, 'html.parser')
	# .find('article', id_ = 'article-body')
	st.write(soup)
	c1,c2,c3 = st.columns([1,3,1])
	# c2.markdown(f"""
	# 	{soup}
	# 	""", unsafe_allow_html=True)
