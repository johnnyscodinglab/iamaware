import streamlit as st

st.set_page_config(layout='wide')
st.logo("logo.png", size='large')


with open('style.css') as f:
	st.markdown(f"<style> {f.read()} </style>",unsafe_allow_html=True)


# c1, c2, c3 = st.columns((3, 1, 3))
# st.sidebar.image('logo.png')

page_home = st.Page("pages/page_home.py", title="Home", icon="🏠")
page_hindu = st.Page("pages/page_hindu.py", title="Hindu Premium", icon="📰")
# page_medium = st.Page("pages/page_medium.py", title="Medium", icon="⚫")
page_search = st.Page("pages/page_search.py", title="Search", icon="🔍")
page_source = st.Page("pages/page_source.py", title="Favorite Source", icon="ℹ️")
ft = st.Page("pages/financialtimes.py", title="Financial Times")
mint = st.Page("pages/mint.py", title="Mint Premium", icon="🍃")	
atlantic = st.Page("pages/theatlantic.py", title="The Atlantic", icon="🅰️")
wired = st.Page("pages/wired.py", title="Wired", icon="🔌")
free = st.Page("pages/free_resources.py", title="Free Resources", icon="🆓")
fraudometer = st.Page("pages/fraudometer.py", title="Fraud-o-Meter", icon="🕵️")
gnews = st.Page("pages/googlenews.py", title="Google News", icon="🗺️")
newsletter = st.Page("pages/newsletter.py", title="Daily Newsletter", icon="🗺️")
slides = st.Page("pages/slides.py", title="Slideument", icon="👩‍🏫")
genai = st.Page("pages/genai.py", title="AI News", icon="🤖")
# hbr = st.Page('pages/hbr.py', title="HBR")

pg = st.navigation([page_home, page_hindu, mint, atlantic, wired, page_search, 
	page_source, free, fraudometer, gnews, newsletter, slides, genai])
pg.run()


	
