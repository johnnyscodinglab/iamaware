import streamlit as st
import openai
from openai import OpenAI
import json
import pandas as pd
import plotly.express as px

st.image('images/fraudometer.png', width=300)
st.subheader('Act you are calling a bank, and... AI will rate your "Fraud"ivity')
openai.api_key = st.secrets["openai_apikey"]
client = OpenAI(api_key=st.secrets["openai_apikey"])

# Helper Functions 

def save_audio(input, path='images/recorded_audio.wav'):
    """Save audio file directly"""
    with open(path, "wb") as f:
        f.write(input.getbuffer())
    # st.success('Audio Saved')

def transcribe_audio(path='images/recorded_audio.wav'):
    """Make the transcription request from whisper"""
    audio_file = open(path, "rb")
    transcript = openai.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text" # or "json", "srt", "vtt"
    )
    return transcript


TRANSCRIPT_FEATURE_PROMPT = """
You are an expert in fraud detection using text transcripts of audio calls.  
Given a transcript, analyze it and extract fraud-relevant features across six dimensions:  
Lexical, Syntactic, Discourse, Semantic, SentimentEmotion, and Behavioral.  

## Requirements:
1. Normalize all feature values between 0.0 (low) and 1.0 (high).  
   - For counts or ratios, scale relative to typical conversation norms.  
   - For categorical/boolean presence (e.g., persuasion tactic detected), use 0 = none, 1 = strong presence.  
2. Return results strictly in JSON format.  
3. Do not include explanations or extra text — only the JSON.  

## Features to Extract

"Lexical":  
  - "SensitiveKeyword_freq" (frequency of personal/financial info requests)  
  - "LexicalDiversity" (normalized type-token ratio)  
  - "Imperative_ratio" (commands vs. total utterances)  

"Syntactic":  
  - "AvgSentenceLength" (normalized against normal conversation length)  
  - "QuestionRatio" (fraction of utterances that are questions)  
  - "Repetition_score" (repeated phrases or requests)  

"Discourse":  
  - "TopicDrift" (sudden changes without smooth transitions)  
  - "Urgency_score" (presence of urgent/pressure language)  
  - "Politeness_level" (use of polite vs. forceful forms)  

"Semantic":  
  - "EntityMentions" (mentions of names, DOB, account details, etc.)  
  - "ScriptSimilarity" (similarity to known scam scripts)  
  - "LM_Perplexity" (linguistic anomaly level)  

"SentimentEmotion":  
  - "NegativeSentiment_ratio"  
  - "EmotionalVolatility" (frequency of sentiment/emotion shifts)  
  - "ConfidenceMarkers" (certainty/assurance words)  

"Behavioral":  
  - "InfoSeeking_ratio" (proportion of utterances asking for sensitive info)  
  - "Scriptedness_score" (repetitiveness vs. natural flow)  
  - "Persuasion_tactics" (presence of authority, fear, scarcity appeals)  

## Example Output JSON
{
  "Lexical": {
    "SensitiveKeyword_freq": 0.80,
    "LexicalDiversity": 0.35,
    "Imperative_ratio": 0.60
  },
  "Syntactic": {
    "AvgSentenceLength": 0.40,
    "QuestionRatio": 0.85,
    "Repetition_score": 0.70
  },
  "Discourse": {
    "TopicDrift": 0.55,
    "Urgency_score": 0.90,
    "Politeness_level": 0.20
  },
  "Semantic": {
    "EntityMentions": 0.75,
    "ScriptSimilarity": 0.88,
    "LM_Perplexity": 0.42
  },
  "SentimentEmotion": {
    "NegativeSentiment_ratio": 0.65,
    "EmotionalVolatility": 0.55,
    "ConfidenceMarkers": 0.80
  },
  "Behavioral": {
    "InfoSeeking_ratio": 0.95,
    "Scriptedness_score": 0.82,
    "Persuasion_tactics": 0.70
  }
"""

# Feature descriptions dictionary
feature_descriptions = {
    # Lexical
    "SensitiveKeyword_freq": "Frequency of sensitive info requests (e.g., password, OTP, account).",
    "LexicalDiversity": "Diversity of vocabulary used; low values may indicate scripted speech.",
    "Imperative_ratio": "Proportion of commands vs. total utterances.",
    # Syntactic
    "AvgSentenceLength": "Normalized sentence length; short sentences may indicate scripts.",
    "QuestionRatio": "Fraction of utterances that are questions.",
    "Repetition_score": "Degree of repeated phrases or requests.",
    # Discourse
    "TopicDrift": "Frequency of abrupt topic changes without transitions.",
    "Urgency_score": "Presence of urgent or pressuring language.",
    "Politeness_level": "Level of politeness vs. forcefulness in language.",
    # Semantic
    "EntityMentions": "Mentions of names, DOB, account numbers, or other identifiers.",
    "ScriptSimilarity": "Semantic similarity to known fraud scripts.",
    "LM_Perplexity": "How unusual the language is compared to normal conversations.",
    # Sentiment & Emotion
    "NegativeSentiment_ratio": "Proportion of negative sentiment in the transcript.",
    "EmotionalVolatility": "Frequency of rapid sentiment/emotion shifts.",
    "ConfidenceMarkers": "Use of strong certainty words like 'guaranteed' or 'definitely'.",
    # Behavioral
    "InfoSeeking_ratio": "Ratio of info-seeking utterances (asking for sensitive details).",
    "Scriptedness_score": "Degree of scripted vs. natural conversation flow.",
    "Persuasion_tactics": "Use of authority, fear, or scarcity tactics."
}

@st.cache_data()
def analyze_transcript(transcript: str):
    """
    Send transcript text to OpenAI for fraud-feature extraction.
    """
    response = client.chat.completions.create(
        model="gpt-5",  # or "gpt-4.1" depending on your plan
        messages=[
            {"role": "system", "content": TRANSCRIPT_FEATURE_PROMPT},
            {"role": "user", "content": transcript}
        ],
        temperature=1
    )
    # Parse JSON output
    raw_output = response.choices[0].message.content
    return json.loads(raw_output)

# Get audio from user
audio_input = st.audio_input('Speak you Fraudster')

if audio_input:
    
    save_audio(audio_input)

    transcribed = transcribe_audio()
    st.subheader("Transcription")
    st.write(transcribed)

    features = analyze_transcript(transcribed)
    # Get Fraud features and display

    # Flatten JSON into list of rows
    rows = []
    for category, feats in features.items():
        for feat, value in feats.items():
            description = feature_descriptions.get(feat, "No description available.")
            rows.append({
                "Category": category,
                "Feature": feat,
                "Value": value,
                "Description": description
            })

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    st.subheader('Fraud Score')
    positive_features = df[df.Feature.isin([
        'Urgency_score',
        'ScriptSimilarity',
        'LM_Perplexity',
        'InfoSeeking_ratio',
        'Scriptedness_score'
    ])]
    final_score = int(round(positive_features.Value.mean() * 100,2))
    st.title(f'{final_score}/100')

    fig = px.bar(df[df.Value > 0].sort_values('Value', ascending=False), 
        x='Feature', y='Value', 
        # text='Description', 
        barmode='group', color = 'Category')
    st.subheader('Features')
    st.plotly_chart(fig)