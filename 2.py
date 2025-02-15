import os
import subprocess
import streamlit as st
import requests
from datetime import datetime, timedelta

# ✅ Ensure OpenAI & Required Modules are Installed
try:
    import openai
except ModuleNotFoundError:
    subprocess.check_call(["pip", "install", "openai"])
    import openai

# 🔑 API Keys (Replace with real keys)
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"  
OPENAI_API_KEY = "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"

# ✅ Validate API Keys
if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
    st.error("❌ Please provide a valid **YouTube API Key**!")
if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    st.warning("⚠️ OpenAI API Key is missing! AI-powered features may not work.")

# 🎯 YouTube API Endpoints
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# 🎬 **Streamlit App UI**
st.title("🚀 Expert-Level AI YouTube Research Tool")

# 🌍 **User Inputs**
search_query = st.text_input("🔍 Enter Topic or Keyword:")
region_code = st.selectbox("🌍 Select Country for Research:", ["US", "IN", "UK", "CA", "AU"])
days = st.number_input("📅 Fetch Data from Last (1-30 Days):", min_value=1, max_value=30, value=7)

# 🔥 **Fetch Trending Video Data**
if st.button("🚀 Find Best Topics"):
    try:
        search_params = {
            "part": "snippet",
            "q": search_query,
            "maxResults": 15,
            "regionCode": region_code,
            "type": "video",
            "order": "viewCount",
            "publishedAfter": (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z",
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
        data = response.json()

        # ✅ Handle API Errors
        if response.status_code != 200:
            error_message = data.get('error', {}).get('message', 'Unknown error')
            st.error(f"❌ YouTube API Error: {error_message}")
        elif "items" not in data or not data["items"]:
            st.warning("❌ No results found.")
        else:
            trending_results = []
            for video in data["items"]:
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:150]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                
                trending_results.append({
                    "Title": title,
                    "Description": description,
                    "URL": video_url
                })

            # 🎯 **Display Results**
            st.success(f"🎯 Found {len(trending_results)} high-potential topics!")
            for result in trending_results:
                st.markdown(
                    f"**🎬 {result['Title']}**  \n"
                    f"🔗 [Watch Video]({result['URL']})"
                )
                st.write("---")

    except Exception as e:
        st.error(f"❌ Error fetching videos: {e}")

# 🤖 **AI Optimization Section**
st.header("🤖 AI-Powered Video Title & SEO Optimization")

title_input = st.text_input("✍️ Enter Video Title:")
if st.button("🚀 Generate AI-Optimized Title & Hashtags"):
    if title_input:
        if openai:
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
            st.warning("⚠️ OpenAI module is not installed properly. Try restarting.")
    else:
        st.warning("⚠️ Please enter a video title first!")
