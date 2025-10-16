from dotenv import load_dotenv
import os
import pandas as pd
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# Access your API key
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found! Make sure it is set in .env")

# Set up YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to fetch videos from a channel
def fetch_videos(channel_id, max_results=50):
    """
    Fetch videos from a given YouTube channel.
    Returns a list of video details.
    """
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=max_results,
        order='date'
    )
    response = request.execute()
    
    videos = []
    for item in response.get('items', []):
        video_data = {
            'video_id': item['id'].get('videoId'),
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'description': item['snippet']['description']
        }
        videos.append(video_data)
    
    return videos

# Example usage
if __name__ == "__main__":
    CHANNEL_ID = "UCLL_e7iOupt05gXo_YbWrIg"
    videos = fetch_videos(CHANNEL_ID)
    
    # Convert to DataFrame
    df = pd.DataFrame(videos)
    print(df.head())
    
    # Save to CSV
    df.to_csv('videos.csv', index=False)
    print("Saved videos to videos.csv")
