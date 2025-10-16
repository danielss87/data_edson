import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import csv

# Load environment variables from .env
load_dotenv()

# Get the API key
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Channel ID (replace if needed)
channel_id = "UCLL_e7iOupt05gXo_YbWrIg"

videos = []
next_page_token = None

# --- 1️⃣ Fetch all videos from the channel ---
while True:
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        order="date",
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            videos.append({
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "published_at": item["snippet"]["publishedAt"]  # 👈 added publish date
            })

    next_page_token = response.get("nextPageToken")
    if not next_page_token:
        break

# --- 2️⃣ Fetch detailed info (duration, views, etc.) ---
video_ids = [video["video_id"] for video in videos]
video_data = []

for i in range(0, len(video_ids), 50):
    request = youtube.videos().list(
        part="contentDetails,statistics",
        id=",".join(video_ids[i:i + 50])
    )
    response = request.execute()

    for item in response["items"]:
        video_data.append({
            "id": item["id"],
            "duration": item["contentDetails"].get("duration", "N/A"),
            "views": item["statistics"].get("viewCount", 0)
        })

# --- 3️⃣ Merge and export to CSV ---
with open("videos.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Video ID", "Duration", "Views", "Published At"])  # 👈 added column
    for video, data in zip(videos, video_data):
        writer.writerow([
            video["title"],
            video["video_id"],
            data["duration"],
            data["views"],
            video["published_at"]
        ])

print("✅ Data saved to videos.csv (now includes publish date!)")
