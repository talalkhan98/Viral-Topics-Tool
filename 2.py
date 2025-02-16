pip install streamlit
pip install requests
pip install openai
import os
import requests
import streamlit as st
import openai
from datetime import datetime, timedelta

# ✅ API Keys Setup (Replace with actual keys)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# ✅ YouTube API URL
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# ✅ Ensure OpenAI module is installed
openai.api_key = OPENAI_API_KEY

# ✅ Streamlit UI
st.title("🚀 Mastery Expert-Level YouTube Research Tool (AI-Powered)")

# ✅ Fetch AI-Generated Viral Topics
def generate_viral_topics():
    prompt = """
    Find 5 trending and viral YouTube video topics based on real-time trends, search volume, and competition. 
    Focus on high-engagement and high-watch-time topics that are suitable for faceless YouTube automation. 
    Provide results in a structured format.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# ✅ Fetch YouTube Trending Data
def fetch_youtube_trending(topic):
    params = {
        "part": "snippet",
        "q": topic,
        "maxResults": 10,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z",
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    return response.json()

# ✅ Generate AI-Based Viral Topics
if st.button("🚀 Find Trending Topics"):
    try:
        viral_topics = generate_viral_topics()
        st.subheader("🔥 AI-Generated Trending Topics:")
        st.write(viral_topics)

        # Fetch YouTube trending videos for each topic
        for topic in viral_topics.split("\n"):
            st.subheader(f"📌 YouTube Trends for: {topic}")
            data = fetch_youtube_trending(topic)
            if "items" in data:
                for video in data["items"]:
                    title = video["snippet"]["title"]
                    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                    st.markdown(f"🎬 **{title}**  \n🔗 [Watch Here]({video_url})")
            else:
                st.warning("❌ No results found for this topic.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ✅ AI Title & Description Generator
st.header("🤖 AI-Powered Video Title & Description Generator")
if st.button("🚀 Generate AI Titles & Descriptions"):
    try:
        title_prompt = "Generate a high-engagement YouTube title based on one of the trending topics."
        description_prompt = "Generate a high-SEO video description for YouTube."

        title_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": title_prompt}]
        )
        description_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": description_prompt}]
        )

        st.subheader("🎯 AI-Generated Video Title:")
        st.write(title_response["choices"][0]["message"]["content"])

        st.subheader("📄 AI-Generated Video Description:")
        st.write(description_response["choices"][0]["message"]["content"])

    except Exception as e:
        st.error(f"❌ OpenAI API Error: {e}")

# ✅ Tool Features Rec ommendations
st.header("🛠️ Tool Features Recommendations")
st.write("""
- **Real-time Trend Analysis**: Continuously monitor trending topics and adjust content strategies accordingly.
- **SEO Optimization**: Integrate SEO tools to analyze keywords and improve video discoverability.
- **Engagement Metrics**: Track viewer engagement metrics to refine content strategies.
- **Automated Posting**: Schedule video uploads and social media posts to maximize reach.
- **Collaboration Tools**: Facilitate collaboration with other creators for cross-promotion.
""")

# ✅ User Feedback Section
st.header("💬 User Feedback")
user_feedback = st.text_area("Share your thoughts or suggestions for improving this tool:")
if st.button("Submit Feedback"):
    if user_feedback:
        st.success("Thank you for your feedback! We appreciate your input.")
    else:
        st.warning("Please enter your feedback before submitting.")

# ✅ Conclusion
st.header("🔚 Conclusion")
st.write("""
This AI-powered YouTube research tool is designed to help you discover trending topics, generate engaging titles and descriptions, and optimize your content strategy. By leveraging the power of OpenAI and the YouTube Data API, you can stay ahead in the competitive landscape of YouTube content creation.
""")
