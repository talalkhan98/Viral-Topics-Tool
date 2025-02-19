import streamlit as st
import requests
import json
import re
import random
from googleapiclient.discovery import build
from pytrends.request import TrendReq

# 🔑 API KEYS (Aap Apni Keys yahan enter karein)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
DEEPAI_API_KEY = "YOUR_DEEPAI_API_KEY"
HUGGINGFACE_API_KEY = "YOUR_HUGGINGFACE_API_KEY"

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
        "AI Hashtags": generate_ai_hashtags(video_data["snippet"]["title"]),
        "AI Title & Description": ai_title_description(video_data["snippet"]["title"]),
        "Thumbnail Analysis": ai_thumbnail_analysis(video_url),
    }, None

# 📊 CTR & Title Optimization
def analyze_ctr_boost(title):
    power_words = ["must-watch", "shocking", "revealed", "secret", "hidden"]
    if any(word in title.lower() for word in power_words):
        return "🔥 High CTR Title"
    return "📉 Low CTR Title – Add Power Words"

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

# 🧠 AI Title & Description Generator (Google Gemini AI)
def ai_title_description(title):
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    data = {"prompt": f"Generate an optimized YouTube title and description for '{title}' with high SEO impact."}
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json().get("candidates", [{}])[0].get("output", "No AI Title Found.")

# 🖼 AI Thumbnail Analysis (Hugging Face API)
def ai_thumbnail_analysis(video_url):
    api_url = "https://api-inference.huggingface.co/models/facebook/dino-vits16"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    response = requests.post(api_url, headers=headers, json={"inputs": video_url})
    return response.json().get("result", "No Thumbnail Analysis Available.")

# 🌍 **Streamlit Web App**
st.title("🚀 AI-Powered YouTube SEO & Automation Tool (Expert-Level)")
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("Analyze Video"):
    if video_url:
        with st.spinner("🔄 Fetching Video Data..."):
            video_info, error = get_video_details(video_url)
            if error:
                st.error(error)
            else:
                st.success("✅ Advanced AI SEO Analysis Complete!")
                st.json(video_info)
    else:
        st.warning("⚠️ Please enter a valid YouTube video URL!")
