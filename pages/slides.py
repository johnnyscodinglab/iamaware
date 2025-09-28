import pandas as pd 
import streamlit as st
import plotly.express as px

st.title('👩🏻‍🏫Slideument')
st.subheader('Inspirations for slide layouts from big consulting firms')

df = pd.read_csv('data/slideanalysis.csv')

# OPTIONS
a1, a2, a3, a4 = st.columns(4)

a1.markdown('##### Slide Type')
slidetype = a1.selectbox('Select Type:', df.slidetype.unique(), label_visibility='collapsed')
filtered = df[(df.slidetype == slidetype)]

a2.markdown('##### Company')
companies = filtered.company.value_counts().reset_index().astype(str)
companies['count'] = ', '+companies['count']
companies = companies.sum(axis=1).tolist()
company = a2.selectbox('Select Company:',  ['Any']+companies, label_visibility='collapsed')
if company!= 'Any':
    filtered = filtered[filtered.company == company.split(',')[0]].reset_index(drop=True)


a3.markdown('##### Tags')
tags = filtered[['tags']].drop_duplicates().dropna().tags.tolist()
tags = ','.join(tags)
tags = ['Any']+list(set(tags.split(',')))
tag = a3.selectbox('Select Tag:', tags, label_visibility='collapsed')
if tag != 'Any':
    filtered = filtered[filtered.tags.str.contains(tag) ].reset_index(drop=True)

st.markdown(f'## {filtered.shape[0]} Templates found')
if filtered.shape[0] > 50:
    st.markdown(f'Showing top 50')
    filtered = filtered.sample(50).reset_index(drop=True)

# CSS styling for pill tags
pill_style = """
<style>
.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.tag-pill {
font:'Arial';
    background-color: #e0f7fa;
    color: #00796b;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
}
</style>
"""

# Build HTML with tags


cols = st.columns(2)

for i, row in filtered.iterrows():
    c = cols[i%len(cols)]
    c.image(row.logo, width=75)
    c.markdown(f'''
    #### {row.title.replace('Details','')}
    **Description**: {row.description}
    ''')
    tags_html = '<div class="tags-container">' + 'Tags:' +"".join(
        [f'<span class="tag-pill">{tag}</span>' for tag in row.tags.split(',')]
    ) + "</div><p></p>"
    

    c.markdown(f'''
        <img style="border-radius: 20px; box-shadow: 0 0px 20px rgba(0,0,0,0.2);" src="{row.img}" >
        <p></p>
    ''', unsafe_allow_html=True)
    c.markdown(pill_style + tags_html, unsafe_allow_html=True)
    c.write(f'[Source]({row.source})')
    c.divider()
