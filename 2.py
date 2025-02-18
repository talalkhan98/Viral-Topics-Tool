import streamlit as st
import re
from googleapiclient.discovery import build
import requests

# 🔑 Replace with your YouTube API Key
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# 🎯 Initialize YouTube API Client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# 🔍 Extract Video ID from YouTube URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 Fetch Video SEO Data + Hidden Tags
def get_video_details(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "❌ Invalid YouTube URL"

    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if "items" not in response or not response["items"]:
        return None, "❌ Video Not Found"

    video_data = response["items"][0]
    
    # 🔍 Extract LSI Keywords from Description
    description = video_data["snippet"]["description"]
    lsi_keywords = extract_lsi_keywords(description)
    
    return {
        "Title": video_data["snippet"]["title"],
        "Description": description,
        "Tags": video_data["snippet"].get("tags", []),
        "LSI Keywords": lsi_keywords,
        "Views": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "Psychological Triggers": analyze_psychological_triggers(description),
    }, None

# 🔥 Extract LSI Keywords (Using OpenAI API)
def extract_lsi_keywords(text):
    # Dummy function (Replace with NLP API if needed)
    keywords = ["SEO tips", "YouTube growth", "video ranking", "metadata strategies"]
    return keywords

# 🧠 Psychological Triggers Analysis
def analyze_psychological_triggers(description):
    triggers = []
    if any(word in description.lower() for word in ["shocking", "secrets", "hidden", "must-watch"]):
        triggers.append("Curiosity Gap 🔥")
    if any(word in description.lower() for word in ["exclusive", "limited-time", "rare"]):
        triggers.append("Scarcity Effect ⏳")
    if any(word in description.lower() for word in ["how-to", "tutorial", "step-by-step"]):
        triggers.append("Instructional Hook 📚")
    return triggers if triggers else ["No strong psychological triggers found"]

# 🌍 Streamlit Web App
st.title("📈 YouTube Video SEO Analyzer + LSI + Psychological Triggers")
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("Analyze Video"):
    if video_url:
        with st.spinner("🔄 Fetching Video Data..."):
            video_info, error = get_video_details(video_url)
            if error:
                st.error(error)
            else:
                st.success("✅ SEO Analysis Complete!")
                st.json(video_info)
    else:
        st.warning("⚠️ Please enter a valid YouTube video URL!")
