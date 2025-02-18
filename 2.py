import streamlit as st
import requests
import re
import json
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# YouTube API Key (Replace with your key)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Function to extract video details
def get_video_details(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Invalid YouTube URL"

    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if "items" not in response or not response["items"]:
        return None, "Video not found"

    video_data = response["items"][0]
    title = video_data["snippet"]["title"]
    description = video_data["snippet"]["description"]
    tags = video_data["snippet"].get("tags", [])
    views = video_data["statistics"].get("viewCount", "N/A")
    likes = video_data["statistics"].get("likeCount", "N/A")
    comments = video_data["statistics"].get("commentCount", "N/A")

    return {
        "Title": title,
        "Description": description,
        "Tags": tags,
        "Views": views,
        "Likes": likes,
        "Comments": comments
    }, None

# Extract Video ID from URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Streamlit UI
st.title("🎯 YouTube Video SEO Analyzer")
video_url = st.text_input("Enter YouTube Video URL")

if st.button("Analyze"):
    if video_url:
        with st.spinner("Fetching video details..."):
            video_info, error = get_video_details(video_url)

            if error:
                st.error(error)
            else:
                st.success("✅ Analysis Complete!")
                st.write("### 📌 Video Details:")
                st.json(video_info)

                # Show Tags
                st.write("### 🏷️ Extracted Tags:")
                if video_info["Tags"]:
                    st.write(", ".join(video_info["Tags"]))
                else:
                    st.warning("No tags found!")

                # Engagement Metrics
                st.write("### 🔥 Engagement Stats:")
                st.write(f"👁️ **Views:** {video_info['Views']}")
                st.write(f"👍 **Likes:** {video_info['Likes']}")
                st.write(f"💬 **Comments:** {video_info['Comments']}")

    else:
        st.warning("⚠️ Please enter a valid YouTube video URL!")
