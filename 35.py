import streamlit as st
import requests
import re
import json
import random
import numpy as np
from googleapiclient.discovery import build
from pytrends.request import TrendReq
from config import YOUTUBE_API_KEY

# ✅ Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)

# 🔍 Extract Video ID
def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 Fetch Video Data
def get_video_details(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "❌ Invalid YouTube URL"

    response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    if "items" not in response or not response["items"]:
        return None, "❌ Video Not Found"

    video_data = response["items"][0]
    return {
        "Title": video_data["snippet"]["title"],
        "Description": video_data["snippet"]["description"],
        "Tags": video_data["snippet"].get("tags", []),
        "Views": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "CTR Analysis": analyze_ctr_boost(video_data["snippet"]["title"]),
        "Virality Score": calculate_virality_score(video_data["statistics"]),
        "Best Upload Time": best_upload_time(),
        "Trending Keywords": fetch_trending_keywords(),
        "AI Hashtags": generate_ai_hashtags(video_data["snippet"]["title"])
    }, None

# 📊 CTR & Title Optimization
def analyze_ctr_boost(title):
    ctr_factors = []
    power_words = ["must-watch", "shocking", "revealed", "secret", "hidden"]
    if any(word in title.lower() for word in power_words):
        ctr_factors.append("🔥 High CTR Title")
    if any(word in title.lower() for word in ["how-to", "guide", "tutorial", "tips"]):
        ctr_factors.append("📚 High Engagement Title")
    return ctr_factors if ctr_factors else ["Neutral Title – Add More Power Words"]

# 📊 AI Virality Prediction
def calculate_virality_score(stats):
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    engagement_rate = ((likes + comments) / max(views, 1)) * 100
    return "🔥 High Viral Potential!" if engagement_rate > 5 else "📉 Low Viral Potential."

# 📊 Best Upload Time Predictor
def best_upload_time():
    times = ["Monday 5 PM", "Tuesday 6 PM", "Wednesday 4 PM", "Thursday 7 PM", "Friday 8 PM", "Saturday 3 PM", "Sunday 2 PM"]
    return random.choice(times)

# 📊 Fetch Trending Keywords
def fetch_trending_keywords():
    pytrends.build_payload(kw_list=["YouTube"], cat=0, timeframe="now 1-d", geo="US")
    trends = pytrends.trending_searches()
    return trends.head(5).values.tolist()

# 📊 AI Hashtag Generator
def generate_ai_hashtags(title):
    return [f"#{word.replace(' ', '')}" for word in title.split()[:5]]

# 🌍 **Streamlit Web App**
st.title("🚀 AI YouTube SEO Analyzer & Competitor Research Tool (FREE VERSION)")
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("Analyze Video"):
    if video_url:
        with st.spinner("🔄 Fetching Video Data..."):
            video_info, error = get_video_details(video_url)
            if error:
                st.error(error)
            else:
                st.success("✅ Advanced SEO Analysis Complete!")
                st.json(video_info)
    else:
        st.warning("⚠️ Please enter a valid YouTube video URL!")
