import streamlit as st
import re
from googleapiclient.discovery import build
import datetime

# 🔑 Replace with your YouTube API Key
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"

# 🎯 Initialize YouTube API Client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# 🔍 Extract Video ID from YouTube URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 Fetch Video SEO Data with Competitor Analysis
def get_video_details(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "❌ Invalid YouTube URL"

    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    if "items" not in response or not response["items"]:
        return None, "❌ Video Not Found"

    video_data = response["items"][0]

    # 🔥 Extract AI-Powered LSI Keywords
    lsi_keywords = extract_lsi_keywords(video_data["snippet"]["title"], video_data["snippet"]["description"])

    # 🔥 CTR Boost Factors Analysis
    ctr_boost_factors = analyze_ctr_boost(video_data["snippet"]["title"])

    # 🔥 Engagement Score & Watch Time
    engagement_score = get_engagement_score(video_data["statistics"])

    # 🔥 Best Upload Time Analysis
    best_upload_time = get_best_upload_time(video_data["snippet"]["publishedAt"])

    return {
        "Title": video_data["snippet"]["title"],
        "Description": video_data["snippet"]["description"],
        "Tags": video_data["snippet"].get("tags", []),
        "LSI Keywords": lsi_keywords,
        "Views": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "CTR Boost Factors": ctr_boost_factors,
        "Engagement Score": engagement_score,
        "Watch Time Analysis": analyze_watch_time(video_data["contentDetails"]),
        "Trending Score": get_trending_score(video_data["snippet"]["title"]),
        "Best Upload Time": best_upload_time
    }, None

# 🔥 AI-Powered LSI Keywords Extraction (Without NLP APIs)
def extract_lsi_keywords(title, description):
    keywords = set()
    title_words = title.lower().split()
    desc_words = description.lower().split()

    for word in title_words + desc_words:
        if len(word) > 3 and word not in ["the", "and", "with", "from"]:
            keywords.add(word)

    return list(keywords)[:10]  # Top 10 Related Keywords

# 🎯 CTR Boost Factors Analysis
def analyze_ctr_boost(title):
    ctr_factors = []
    if any(word in title.lower() for word in ["must-watch", "shocking", "revealed", "secret", "hidden"]):
        ctr_factors.append("High Curiosity Factor 🔥")
    if any(word in title.lower() for word in ["how-to", "guide", "tutorial", "tips"]):
        ctr_factors.append("Instructional Appeal 📚")
    return ctr_factors if ctr_factors else ["Neutral Title (Consider adding more power words)"]

# 🔥 Engagement Score Calculation
def get_engagement_score(stats):
    likes = int(stats.get("likeCount", 0))
    views = int(stats.get("viewCount", 1))
    engagement = (likes / views) * 100
    return f"{round(engagement, 2)}%"

# 🔍 Watch Time & Video Length Analysis
def analyze_watch_time(content_details):
    duration = content_details["duration"]
    return f"Video Duration: {duration}"

# 📊 Trending Score Analysis
def get_trending_score(title):
    trending_keywords = ["viral", "trending", "new", "latest", "breaking"]
    score = sum(1 for word in trending_keywords if word in title.lower()) * 20
    return f"{min(score, 100)}%"

# 🔥 Best Upload Time Analysis (Based on Video Publish Time)
def get_best_upload_time(published_at):
    publish_time = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    peak_hours = ["12 PM - 3 PM", "6 PM - 9 PM"]
    hour = publish_time.hour

    if 12 <= hour < 15:
        return f"Published at {publish_time.strftime('%I:%M %p')} (Optimal Upload Time ✅)"
    elif 18 <= hour < 21:
        return f"Published at {publish_time.strftime('%I:%M %p')} (High Engagement Time ✅)"
    else:
        return f"Published at {publish_time.strftime('%I:%M %p')} (Consider Adjusting for Better Reach) ❌"

# 🌍 Streamlit Web App
st.title("🚀 Advanced YouTube SEO Analyzer + Competitor Insights")
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
