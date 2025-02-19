import streamlit as st
import requests
import json
import re
import random
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from pytrends.request import TrendReq
from transformers import pipeline

# 🔑 API KEYS
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"
GEMINI_API_KEY = "AIzaSyCKCLZsmO80dVDSqEY0KZwzNbaMmn3gJ5s"
DEEPAI_API_KEY = "0cd66499-6458-4d12-883b-b87f355d4b3d"
HUGGINGFACE_API_KEY = "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"

# ✅ Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)
sentiment_analysis = pipeline("sentiment-analysis")

# 📊 **Extract Video ID**
def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 **Fetch Video Data**
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
        "AI Hashtags": generate_ai_hashtags(video_data["snippet"]["title"]),
        "AI Title & Description": ai_title_description(video_data["snippet"]["title"]),
        "Thumbnail Analysis": ai_thumbnail_analysis(video_url),
        "Monetization Potential": check_monetization_potential(video_data["statistics"]),
        "Sentiment Analysis": analyze_video_comments(video_id),
    }, None

# 📊 **CTR & Title Optimization**
def analyze_ctr_boost(title):
    power_words = ["must-watch", "shocking", "revealed", "secret", "hidden"]
    return "🔥 High CTR Title" if any(word in title.lower() for word in power_words) else "📉 Low CTR Title"

# 📊 **AI Virality Prediction**
def calculate_virality_score(stats):
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    engagement_rate = ((likes + comments) / max(views, 1)) * 100
    return "🔥 High Viral Potential!" if engagement_rate > 5 else "📉 Low Viral Potential."

# 📊 **Best Upload Time Predictor**
def best_upload_time():
    times = ["Monday 5 PM", "Tuesday 6 PM", "Wednesday 4 PM", "Thursday 7 PM", "Friday 8 PM", "Saturday 3 PM", "Sunday 2 PM"]
    return random.choice(times)

# 📊 **Fetch Trending Keywords**
def fetch_trending_keywords():
    pytrends.build_payload(kw_list=["YouTube"], cat=0, timeframe="now 1-d", geo="US")
    trends = pytrends.trending_searches()
    return trends.head(5).values.tolist()

# 📊 **AI Hashtag Generator**
def generate_ai_hashtags(title):
    return [f"#{word.replace(' ', '')}" for word in title.split()[:5]]

# 🧠 **AI Title & Description Generator**
def ai_title_description(title):
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    data = {"prompt": f"Generate an optimized YouTube title and description for '{title}' with high SEO impact."}
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json().get("candidates", [{}])[0].get("output", "No AI Title Found.")

# 🖼 **AI Thumbnail Analysis**
def ai_thumbnail_analysis(video_url):
    api_url = "https://api-inference.huggingface.co/models/facebook/dino-vits16"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    response = requests.post(api_url, headers=headers, json={"inputs": video_url})
    return response.json().get("result", "No Thumbnail Analysis Available.")

# 💰 **Monetization Potential Checker**
def check_monetization_potential(stats):
    views = int(stats.get("viewCount", 0))
    if views > 100000:
        return "💰 High Monetization Potential!"
    elif views > 10000:
        return "🟡 Medium Monetization Potential"
    else:
        return "🔴 Low Monetization Potential"

# 🧠 **AI-Powered Comment Sentiment Analysis**
def analyze_video_comments(video_id):
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=10)
    response = request.execute()
    
    comments = [item["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for item in response.get("items", [])]
    sentiments = sentiment_analysis(comments) if comments else []
    
    positive = sum(1 for s in sentiments if s["label"] == "POSITIVE")
    negative = sum(1 for s in sentiments if s["label"] == "NEGATIVE")
    return f"👍 Positive Comments: {positive}, 👎 Negative Comments: {negative}"

# 🌍 **Streamlit Web App**
st.title("🚀 AI-Powered YouTube SEO & Automation Tool")
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("Analyze Video"):
    if video_url:
        with st.spinner("🔄 Fetching Video Data..."):
            video_info, error = get_video_details(video_url)
            if error:
                st.error(error)
            else:
                st.success("✅ AI SEO Analysis Complete!")
                st.json(video_info)
    else:
        st.warning("⚠️ Please enter a valid YouTube video URL!")
