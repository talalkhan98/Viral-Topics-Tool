import streamlit as st
import requests
import openai
from googleapiclient.discovery import build
from transformers import pipeline
from pytube import YouTube
from pytrends.request import TrendReq
import pandas as pd

# ✅ Streamlit App Title
st.title("🚀 AI-Powered YouTube SEO & Automation Tool")

# ✅ YouTube API Key Setup
API_KEY = "YOUR_YOUTUBE_API_KEY"
youtube = build("youtube", "v3", developerKey=API_KEY)

# ✅ AI-Powered Title & Description Generator
def generate_ai_title_description(video_topic):
    prompt = f"Generate a highly engaging YouTube title and description for {video_topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert YouTube SEO optimizer."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# ✅ AI Competitor Analysis
def competitor_analysis(video_title):
    trends = TrendReq(hl='en-US', tz=360)
    trends.build_payload([video_title], cat=0, timeframe='now 7-d', geo='US', gprop='youtube')
    df = trends.interest_over_time()
    return df

# ✅ Get Video Details from YouTube
def get_video_details(video_url):
    yt = YouTube(video_url)
    video_id = yt.video_id
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()
    return response

# ✅ Input YouTube URL
video_url = st.text_input("🔗 Enter YouTube Video URL")

if video_url:
    video_info = get_video_details(video_url)
    video_title = video_info["items"][0]["snippet"]["title"]
    
    # ✅ AI Title & Description Generation
    st.subheader("🎯 AI-Generated Title & Description")
    ai_content = generate_ai_title_description(video_title)
    st.write(ai_content)

    # ✅ Competitor Research
    st.subheader("📊 Competitor Trends Analysis")
    trend_data = competitor_analysis(video_title)
    st.line_chart(trend_data)
