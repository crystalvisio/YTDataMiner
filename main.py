import os 
import json
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_URL_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"

def get_video_id(search_query, max_results):

    # Defining search params
    params = {
        "part": "snippet",
        "q": search_query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY
    }

    # Send GET request
    response = requests.get(url = YOUTUBE_URL_ENDPOINT, params = params)

    # convert data to json
    data = response.json()

    # Extract the video IDs from the response
    video_ids = [item["id"]["videoId"] for item in data["items"]]

    # Get video urls
    #video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

    return video_ids

# Search keyword 
def get_video_data():
    video_ids = get_video_id("Database Tutorial", 1000)
    # Define the endpoint URL
    url = f"https://www.googleapis.com/youtube/v3/videos"

    # Define the parameters for the request
    params = {
        "part": "snippet,statistics",
        "id": ','.join(video_ids),
        "key": API_KEY
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Convert the response to JSON
    data = response.json()

    # Extract the video statistics and details from the response
    videos_data = []
    for item in data["items"]:
        video_data = item["snippet"]
        video_statistics = item["statistics"]
        videos_data.append({
            "title": video_data["title"],
            "likes": video_statistics.get("likeCount", "N/A"),
            "dislikes": video_statistics.get("dislikeCount", "N/A"),
            "views": video_statistics.get("viewCount", "N/A"),
            "comments": video_statistics.get("commentCount", "N/A")
        })

    # Return the data as a JSON object
    return json.dumps(videos_data)

result = json.loads(get_video_data())

# Export to a CSV file
csv_file = "video_data.csv"
with open(csv_file, mode="w", newline = "", encoding ="utf-8") as file:
    fieldnames = ["title", "likes", "dislikes", "views", "comments"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for video in result:
        writer.writerow(video)

print(f"Video data exported to {csv_file}")