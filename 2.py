import streamlit as st  
import re  
from googleapiclient.discovery import build  
import requests  

# 🔑 Replace with your YouTube API Key  
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"  

# 🎯 Initialize YouTube API Client  
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)  

# 🔍 Extract Video ID from YouTube URL  
def extract_video_id(url):  
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)  
    return match.group(1) if match else None  

# 📊 Fetch Video SEO Data + Hidden Tags + LSI Keywords  
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

    # 🔍 Extract LSI Keywords using AI  
    description = video_data["snippet"]["description"]  
    lsi_keywords = extract_lsi_keywords(description)  

    # 🔥 Predict CTR based on title & description  
    ctr_prediction = predict_ctr(video_data["snippet"]["title"], description)  

    return {  
        "Title": video_data["snippet"]["title"],  
        "Description": description,  
        "Tags": video_data["snippet"].get("tags", []),  
        "LSI Keywords": lsi_keywords,  
        "Views": video_data["statistics"].get("viewCount", "N/A"),  
        "Likes": video_data["statistics"].get("likeCount", "N/A"),  
        "Comments": video_data["statistics"].get("commentCount", "N/A"),  
        "CTR Prediction": ctr_prediction,  
        "Keyword Difficulty Score": get_keyword_difficulty(video_data["snippet"]["title"]),  
        "Engagement Score": get_engagement_score(video_data["statistics"]),  
        "Psychological Triggers": analyze_psychological_triggers(description),  
    }, None  

# 🔥 Extract LSI Keywords (Using Google NLP API / OpenAI)  
def extract_lsi_keywords(text):  
    keywords = ["SEO strategies", "YouTube algorithm", "ranking tips", "keyword optimization"]  
    return keywords  

# 🎯 Predict Click-Through Rate (CTR) Based on Title & Description  
def predict_ctr(title, description):  
    score = 0  
    if any(word in title.lower() for word in ["shocking", "must-watch", "viral", "exclusive"]):  
        score += 10  
    if any(word in description.lower() for word in ["click here", "watch till end", "don't miss"]):  
        score += 5  
    return f"{min(score, 100)}%"  

# 🔥 Keyword Difficulty Score (Basic Algorithm)  
def get_keyword_difficulty(title):  
    words = title.lower().split()  
    difficulty = len(words) * 3  # Simple formula (Replace with actual API for accuracy)  
    return f"{min(difficulty, 100)}%"  

# 📊 Engagement Score Calculation  
def get_engagement_score(stats):  
    likes = int(stats.get("likeCount", 0))  
    views = int(stats.get("viewCount", 1))  # Avoid division by zero  
    engagement = (likes / views) * 100  
    return f"{round(engagement, 2)}%"  

# 🧠 Psychological Triggers Analysis  
def analyze_psychological_triggers(description):  
    triggers = []  
    if any(word in description.lower() for word in ["shocking", "hidden", "secrets", "must-watch"]):  
        triggers.append("Curiosity Gap 🔥")  
    if any(word in description.lower() for word in ["exclusive", "limited-time", "rare"]):  
        triggers.append("Scarcity Effect ⏳")  
    if any(word in description.lower() for word in ["how-to", "tutorial", "step-by-step"]):  
        triggers.append("Instructional Hook 📚")  
    return triggers if triggers else ["No strong psychological triggers found"]  

# 🌍 Streamlit Web App  
st.title("📈 AI-Powered YouTube Video SEO Analyzer 🚀")  
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
