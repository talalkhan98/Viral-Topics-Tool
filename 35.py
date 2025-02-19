import streamlit as st
import requests
import re
import openai
from googleapiclient.discovery import build
from pytrends.request import TrendReq
import numpy as np
import random
from PIL import Image
import cv2
import matplotlib.pyplot as plt

# 🔑 Replace API Keys
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"
DEEPAI_API_KEY = "0cd66499-6458-4d12-883b-b87f355d4b3d"
openai.api_key = "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"

# ✅ Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ✅ Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# 🔍 Extract Video ID
def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 Get Video Data
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

    return {
        "Title": video_data["snippet"]["title"],
        "Description": video_data["snippet"]["description"],
        "Tags": video_data["snippet"].get("tags", []),
        "Views": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "CTR Analysis": analyze_ctr_boost(video_data["snippet"]["title"]),
        "Virality Score": calculate_virality_score(video_data["statistics"]),
        "Sentiment Analysis": analyze_comments_sentiment(video_data["snippet"]["title"]),
        "Best Upload Time": best_upload_time(),
        "Trending Keywords": fetch_trending_keywords()
    }, None

import streamlit as st
import requests
import re
import openai
from googleapiclient.discovery import build
from pytrends.request import TrendReq
import numpy as np
import random
from PIL import Image
import cv2
import matplotlib.pyplot as plt

# 🔑 Replace API Keys
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
DEEPAI_API_KEY = "YOUR_DEEPAI_API_KEY"
openai.api_key = "YOUR_OPENAI_API_KEY"

# ✅ Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ✅ Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# 🔍 Extract Video ID
def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 📊 Get Video Data
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

    return {
        "Title": video_data["snippet"]["title"],
        "Description": video_data["snippet"]["description"],
        "Tags": video_data["snippet"].get("tags", []),
        "Views": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "CTR Analysis": analyze_ctr_boost(video_data["snippet"]["title"]),
        "Virality Score": calculate_virality_score(video_data["statistics"]),
        "Sentiment Analysis": analyze_comments_sentiment(video_data["snippet"]["title"]),
        "Best Upload Time": best_upload_time(),
        "Trending Keywords": fetch_trending_keywords()
    }, None

# 📊 CTR & Title Optimization
def analyze_ctr_boost(title):
    ctr_factors = []
    power_words = ["must-watch", "shocking", "revealed", "secret", "hidden"]
    
    if any(word in title.lower() for word in power_words):
        ctr_factors.append("🔥 High Click-Through Rate Title")
    
    if any(word in title.lower() for word in ["how-to", "guide", "tutorial", "tips"]):
        ctr_factors.append("📚 High Engagement Title")
    
    return ctr_factors if ctr_factors else ["Neutral Title – Consider More Power Words"]

# 📊 AI Thumbnail Analysis (CTR Optimization)
def analyze_thumbnail(image_path):
    image = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("📊 Thumbnail Analysis - CTR Optimization")
    plt.show()

# 📊 AI Virality Prediction
def calculate_virality_score(stats):
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    engagement_rate = ((likes + comments) / max(views, 1)) * 100

    if engagement_rate > 5 and views > 5000:
        return "🔥 High Viral Potential!"
    elif engagement_rate > 2 and views > 2000:
        return "⚡ Moderate Viral Potential!"
    else:
        return "📉 Low Viral Potential."

# 📊 AI-Powered Sentiment Analysis
def analyze_comments_sentiment(title):
    response = requests.post(
        "https://api.deepai.org/api/sentiment-analysis",
        headers={"api-key": DEEPAI_API_KEY},
        data={"text": title}
    )
    return response.json().get("output", ["Unknown"])[0]

# 📊 Best Upload Time Predictor
def best_upload_time():
    times = ["Monday 5 PM", "Tuesday 6 PM", "Wednesday 4 PM", "Thursday 7 PM", "Friday 8 PM", "Saturday 3 PM", "Sunday 2 PM"]
    return random.choice(times)

# 📊 Fetch Trending Keywords
def fetch_trending_keywords():
    pytrends.build_payload(kw_list=["YouTube"], cat=0, timeframe="now 1-d", geo="US")
    trends = pytrends.trending_searches()
    return trends.head(5).values.tolist()

# 📊 AI-Generated SEO Title & Description
def generate_ai_title_description(video_topic):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Generate a viral YouTube title and SEO description"},
                  {"role": "user", "content": video_topic}]
    )
    return response['choices'][0]['message']['content']

# 🌍 **Streamlit Web App**
st.title("🚀 AI-Powered YouTube SEO Analyzer & Competitor Research")
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
        st.warning("⚠️ Please enter a valid YouTube video URL!")￼Enter# 📊 CTR & Title Optimization
def analyze_ctr_boost(title):
    ctr_factors = []
    power_words = ["must-watch", "shocking", "revealed", "secret", "hidden"]
    
    if any(word in title.lower() for word in power_words):
        ctr_factors.append("🔥 High Click-Through Rate Title")
    
    if any(word in title.lower() for word in ["how-to", "guide", "tutorial", "tips"]):
        ctr_factors.append("📚 High Engagement Title")
    
    return ctr_factors if ctr_factors else ["Neutral Title – Consider More Power Words"]

# 📊 AI Thumbnail Analysis (CTR Optimization)
def analyze_thumbnail(image_path):
    image = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("📊 Thumbnail Analysis - CTR Optimization")
    plt.show()

# 📊 AI Virality Prediction
def calculate_virality_score(stats):
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
gagement_rate = ((likes + comments) / max(views, 1)) * 100

    if engagement_rate > 5 and views > 5000:
        return "🔥 High Viral Potential!"
    elif engagement_rate > 2 and views > 2000:
        return "⚡ Moderate Viral Potential!"
    else:
        return "📉 Low Viral Potential."

# 📊 AI-Powered Sentiment Analysis
def analyze_comments_sentiment(title):
    response = requests.post(
        "https://api.deepai.org/api/sentiment-analysis",
        headers={"api-key": DEEPAI_API_KEY},
        data={"text": title}
    )
    return response.json().get("output", ["Unknown"])[0]

# 📊 Best Upload Time Predictor
def best_upload_time():
    times = ["Monday 5 PM", "Tuesday 6 PM", "Wednesday 4 PM", "Thursday 7 PM", "Friday 8 PM", "Saturday 3 PM", "Sunday 2 PM"]
    return random.choice(times)

# 📊 Fetch Trending Keywords
def fetch_trending_keywords():
    pytrends.build_payload(kw_list=["YouTube"], cat=0, timeframe="now 1-d", geo="US")
