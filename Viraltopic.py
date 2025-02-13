import streamlit as st
import requests
from datetime import datetime, timedelta

# ✅ YouTube API Key (Replace with your own API Key)
API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"

# ✅ YouTube API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# ✅ Streamlit App Title
st.title("🔥 YouTube Viral Topics Tool")

# ✅ User Input for Days
days = st.number_input("📅 Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# ✅ List of Viral Keywords
keywords = [
    "Affair Relationship Stories", "Reddit Update", "Reddit Relationship Advice", "Reddit Relationship",
    "Reddit Cheating", "AITA Update", "Open Marriage", "Open Relationship", "X BF Caught",
    "Stories Cheat", "X GF Reddit", "AskReddit Surviving Infidelity", "GurlCan Reddit",
    "Cheating Story Actually Happened", "Cheating Story Real", "True Cheating Story",
    "Reddit Cheating Story", "R/Surviving Infidelity", "Surviving Infidelity",
    "Reddit Marriage", "Wife Cheated I Can't Forgive", "Reddit AP", "Exposed Wife",
    "Cheat Exposed"
]

# ✅ Fetch Data Button
if st.button("🔍 Fetch Viral Topics"):
    try:
        # 🔹 Calculate Date Range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # 🔹 Loop Through Keywords
        for keyword in keywords:
            st.write(f"🔎 Searching for keyword: **{keyword}**...")

            # ✅ Define Search Parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # ✅ Fetch YouTube Data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # ✅ Check if Items Exist
            if "items" not in data or not data["items"]:
                st.warning(f"❌ No videos found for: **{keyword}**")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"⚠️ Skipping keyword: **{keyword}** due to missing video/channel data.")
                continue

            # ✅ Fetch Video Statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"❌ Failed to fetch video statistics for: **{keyword}**")
                continue

            # ✅ Fetch Channel Statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"❌ Failed to fetch channel statistics for: **{keyword}**")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # ✅ Collect Results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                # 🔥 Filter: Only Include Channels with Less Than 3,000 Subscribers
                if subs < 3000:
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # ✅ Display Results
        if all_results:
            st.success(f"✅ Found **{len(all_results)} trending videos!**")
            for result in all_results:
                st.markdown(
                    f"**📌 Title:** {result['Title']}  \n"
                    f"**📝 Description:** {result['Description']}  \n"
                    f"**▶️ Video URL:** [Watch Video]({result['URL']})  \n"
                    f"**👀 Views:** {result['Views']}  \n"
                    f"**📌 Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("⚠️ No results found for channels with less than **3,000 subscribers**.")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
