import streamlit as st  
import requests  
import openai  
import pandas as pd  
import matplotlib.pyplot as plt  

# API Keys (Replace with your own)
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"  
OPENAI_API_KEY = "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"  

st.title("🚀 YouTube SEO & Analytics Tool (TubeBuddy Alternative)")  

# 🔹 YouTube Video Analytics
video_id = st.text_input("🎥 Enter YouTube Video ID")  

if st.button("📊 Get Video Stats"):  
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={video_id}&key={YOUTUBE_API_KEY}"  
    response = requests.get(url).json()  

    if "items" in response and len(response["items"]) > 0:  
        video = response["items"][0]  
        title = video["snippet"]["title"]  
        tags = video["snippet"].get("tags", [])  
        views = int(video["statistics"]["viewCount"])  
        likes = int(video["statistics"]["likeCount"])  
        comments = int(video["statistics"]["commentCount"])  
        monetization = "Enabled" if "monetization" in video else "Disabled"  

        st.write(f"**🎬 Title:** {title}")  
        st.write(f"**👁️ Views:** {views}")  
        st.write(f"**👍 Likes:** {likes}")  
        st.write(f"**💬 Comments:** {comments}")  
        st.write(f"💰 **Monetization:** {monetization}")  

        if tags:  
            st.write("**🏷️ Tags:**", ", ".join(tags))  
        else:  
            st.write("🚫 No Tags Found")  

        # 📊 Graph of Video Stats  
        df = pd.DataFrame({"Metrics": ["Views", "Likes", "Comments"], "Count": [views, likes, comments]})  
        st.bar_chart(df.set_index("Metrics"))  

    else:  
        st.error("Invalid Video ID or API Error!")  

# 🔹 AI-Powered Title & Description Optimizer  
title_input = st.text_input("✍ Enter Video Title")  
description_input = st.text_area("📝 Enter Video Description")  

if st.button("🤖 Optimize Title & Description"):  
    openai.api_key = OPENAI_API_KEY  
    prompt = f"Optimize this YouTube title and description for SEO & CTR:\nTitle: {title_input}\nDescription: {description_input}"  
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])  

    optimized_text = response["choices"][0]["message"]["content"]  
    st.write("✅ **Optimized Title & Description:**")  
    st.write(optimized_text)  

# 🔹 AI-Powered LSI Keywords Finder  
keyword = st.text_input("🔍 Enter Primary Keyword")  

if st.button("📈 Generate LSI Keywords"):  
    openai.api_key = OPENAI_API_KEY  
    prompt = f"Generate LSI (Latent Semantic Indexing) keywords for this topic: {keyword}"  
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])  

    lsi_keywords = response["choices"][0]["message"]["content"]  
    st.write("✅ **LSI Keywords:**")  
    st.write(lsi_keywords)  

# 🔹 AI-Based Hashtag & Tag Generator  
video_topic = st.text_input("📌 Enter Video Topic")  

if st.button("🏷️ Generate Hashtags & Tags"):  
    openai.api_key = OPENAI_API_KEY  
    prompt = f"Generate SEO-optimized YouTube tags and hashtags for this topic: {video_topic}"  
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])  

    tag_data = response["choices"][0]["message"]["content"]  
    st.write("✅ **Recommended Hashtags & Tags:**")  
    st.write(tag_data)  

# 🔹 AI-Powered Trending Topics Finder  
if st.button("🔥 Find Trending Topics"):  
    openai.api_key = OPENAI_API_KEY  
    prompt = "Generate the top 5 YouTube trending topics worldwide right now."  
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])  

    trends = response["choices"][0]["message"]["content"]  
    st.write("🔥 **Trending Topics Right Now:**")  
    st.write(trends)  

# 🔹 Competitor Analysis  
channel_id = st.text_input("🏆 Enter YouTube Channel ID")  

if st.button("📈 Get Best Videos"):  
    channel_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=5&order=viewCount&key={YOUTUBE_API_KEY}"  
    channel_response = requests.get(channel_url).json()  

    if "items" in channel_response:  
        st.write("🚀 **Top 5 Videos from this Channel:**")  
        for item in channel_response["items"]:  
            st.write(f"📌 {item['snippet']['title']}")  
    else:  
        st.error("No Data Found!")
