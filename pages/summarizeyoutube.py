import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import json

st.title('▶️Summarize YouTube Video▶️')
video_id = st.text_input('YouTube Video ID:', 'PDw3Uk9dN9k')

@st.cache_data(show_spinner='Fetching Video Transcript...')
def fetchYTTranscript(video_id):
    ytt_api = YouTubeTranscriptApi()
    return ytt_api.fetch(video_id)

fetched_transcript = fetchYTTranscript(video_id)
text = ' '.join([x.text for x in fetched_transcript.snippets])
text = text.replace('\xa0', ' ')

st.subheader(f'First 100 words of {len(text.split(' '))} words')
first100 = ' '.join(text.split(' ')[:100]) + '...'
st.write(first100)

BLOGPROMPT = """
You are an expert content writer. Your task is to convert the following YouTube video transcript into a professional, readable, and engaging blog post. Follow these instructions carefully:

1. **Title**: Create a catchy and SEO-friendly title based on the video content.
2. **Introduction**: Write a compelling introduction summarizing the main theme of the video.
3. **Sections**: Divide the blog post into logical sections with clear subheadings. Use the transcript to identify key points or topics.
4. **Content under Sections**:
   - Summarize key points from the transcript.
   - Make the content engaging, easy to read, and in paragraph form.
   - Use bullet points or numbered lists where it makes sense.
5. **Conclusion**: End with a summary or actionable insights, encouraging readers to take action or reflect.
6. **Tone & Style**: Friendly, informative, and professional. Suitable for a blog audience.

Genereate the output in a markdown format

Here is the transcript:

{TRANSCRIPT}
""".format(TRANSCRIPT = text)

client = OpenAI(api_key=st.secrets["openai_apikey"])
@st.cache_data(show_spinner ='Converting to Blog post...')
def getCompletion(prompt):
    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    return response.output_text

blog_post = getCompletion(BLOGPROMPT)
st.write(blog_post)