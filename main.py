import streamlit as st

st.set_page_config(layout='wide')
st.logo("logo.png", size='large')

# c1, c2, c3 = st.columns((3, 1, 3))
# st.sidebar.image('logo.png')

page_home = st.Page("pages/page_home.py", title="Home", icon="🏠")
page_hindu = st.Page("pages/page_hindu.py", title="Hindu Premium", icon="📰")
page_medium = st.Page("pages/page_medium.py", title="Medium", icon="⚫")
page_search = st.Page("pages/page_search.py", title="Search", icon="🔍")

pg = st.navigation([page_home, page_hindu, page_medium, page_search])
pg.run()



	
