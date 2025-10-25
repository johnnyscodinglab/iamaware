import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import json

st.title('▶️Summarize YouTube Video▶️')
video_id = st.text_input('YouTube Video ID:', placeholder='PDw3Uk9dN9k')

@st.cache_data(show_spinner='Fetching Video Transcript...')
def fetchYTTranscript(video_id):
    ytt_api = YouTubeTranscriptApi()
    return ytt_api.fetch(video_id)

if video_id:
    fetched_transcript = fetchYTTranscript(video_id)
    text = ' '.join([x.text for x in fetched_transcript.snippets])
    text = text.replace('\xa0', ' ')

    st.download_button(
        label="-> Download Transcript 📂 ",
        data=text,
        file_name="text.txt",
        mime="text/plain"
    )

    st.subheader(f'First 100 words of {len(text.split(' '))} words of the transcript')
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

    ### Output format guidelines
    1. Genereate the output strictly in markdown format. 
    2. Mandatorily Restrict the blog post to < 700 words
    3. Keep the bullet points concise yet informative
    4. Do not add additional information not part of the video
    5. Keep the section headings in h3, and title heading in h1
    6. The output should look like a finalized blogpost

    Here is the transcript:

    {TRANSCRIPT}
    """.format(TRANSCRIPT = text)

    client = OpenAI(api_key=st.secrets["openai_apikey"])
    @st.cache_data(show_spinner ='Converting to Blog post...')
    def getCompletion(prompt):
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt,
            max_output_tokens = 2000
        )
        return response

    response = getCompletion(BLOGPROMPT)
    # st.write(response)
    blog_post = response.output_text
    st.write(f"""
    * Input Tokens: {response.usage.input_tokens}
    * Output Tokens: {response.usage.output_tokens}
    * Total Tokens: {response.usage.total_tokens}
    * Cost of Blog Post: ${int(response.usage.total_tokens)*0.025/1000000:.4f}
    """)
    st.write(blog_post)