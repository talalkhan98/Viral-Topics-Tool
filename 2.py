import os
import requests
import streamlit as st
from datetime import datetime, timedelta

# ✅ API Keys Setup (Replace with actual keys)
YOUTUBE_API_KEY = os.getenv("AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc")  
OPENAI_API_KEY = os.getenv("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")

# ✅ YouTube API URL
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# ✅ Ensure OpenAI module is installed
try:
    import openai
    openai.api_key = OPENAI_API_KEY
except ImportError:
    st.error("❌ OpenAI module not found! Install using `pip install openai`")

# ✅ Streamlit UI
st.title("🚀 Mastery Expert-Level YouTube Research Tool")

# ✅ User Input Section
search_query = st.text_input("🔍 Enter Topic:")
region_code = st.selectbox("🌍 Select Country:", ["US", "IN", "UK", "CA", "AU"])
days = st.number_input("📅 Days for Trending Data:", min_value=1, max_value=30, value=7)

# ✅ Fetch YouTube Trending Data
def fetch_youtube_trending():
    params = {
        "part": "snippet",
        "q": search_query,
        "maxResults": 15,
        "regionCode": region_code,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z",
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    return response.json()

if st.button("🚀 Find Best Topics"):
    try:
        data = fetch_youtube_trending()
        if "items" not in data or not data["items"]:
            st.warning("❌ No results found.")
        else:
            for video in data["items"]:
                title = video["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                st.markdown(f"🎬 **{title}**  \n🔗 [Watch Here]({video_url})")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ✅ AI Title Generator
st.header("🤖 AI-Powered Title Generator")
title_input = st.text_input("✍️ Enter Video Title:")
if st.button("🚀 Generate AI Title"):
    try:
        if title_input:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Generate an engaging YouTube title: {title_input}"}]
            )
            st.success("✅ AI Title Generated:")
            st.write(response["choices"][0]["message"]["content"])
        else:
            st.warning("⚠️ Enter a title first!")
    except Exception as e:
        st.error(f"❌ OpenAI API Error: {e}")
