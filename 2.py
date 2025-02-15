import os
import subprocess

try:
    import openai
except ModuleNotFoundError:
    subprocess.check_call(["pip", "install", "openai"])
    import openai

import streamlit as st
import requests
import openai
from datetime import datetime, timedelta

# 🔑 API Keys
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"  # Replace with your API Key
OPENAI_API_KEY = "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"    # Replace with your API Key

# URLs
YOUTUBE_TRENDING_URL = "https://www.googleapis.com/youtube/v3/videos"

# Streamlit App Title
st.title("🚀 Auto-Generated Trending Faceless Topics Finder")

# Input Fields
region_code = st.selectbox("🌍 Select Country for Trending Videos:", ["US", "IN", "UK", "CA", "AU"])
days = st.number_input("🔍 Fetch Trending Videos from the Last (1-30 Days):", min_value=1, max_value=30, value=7)

# Fetch Data Button
if st.button("🔥 Find Trending Faceless Topics"):
    try:
        # YouTube API Trending Search
        search_params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": 10,
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(YOUTUBE_TRENDING_URL, params=search_params)
        data = response.json()

        if "items" not in data:
            st.warning("❌ No trending videos found.")
        else:
            trending_results = []
            for video in data["items"]:
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:150]
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                views = int(video["statistics"].get("viewCount", 0))

                # Store Results
                trending_results.append({
                    "Title": title,
                    "Description": description,
                    "URL": video_url,
                    "Views": views
                })

            # Display Results
            if trending_results:
                st.success(f"🎯 Found {len(trending_results)} trending faceless video topics!")
                for result in trending_results:
                    st.markdown(
                        f"**🎬 {result['Title']}**  \n"
                        f"🔗 [Watch Video]({result['URL']})  \n"
                        f"👀 Views: {result['Views']}"
                    )
                    st.write("---")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# AI Optimization Section
st.header("🤖 AI-Powered Title & Hashtag Generator")

title_input = st.text_input("✍️ Enter Video Title:")
if st.button("🚀 Generate AI-Optimized Title & Hashtags"):
    if title_input:
        try:
            openai.api_key = OPENAI_API_KEY
            prompt = f"Generate an engaging YouTube title and hashtags for: {title_input}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response["choices"][0]["message"]["content"]
            st.success("✅ AI-Generated Title & Hashtags:")
            st.write(result)
        except Exception as e:
            st.error(f"❌ OpenAI API Error: {e}")
    else:
        st.warning("⚠️ Please enter a video title first!")
