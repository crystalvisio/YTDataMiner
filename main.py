# Import necessary libraries
import os 
import csv
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get YouTube API key from environment variables
API_KEY = os.getenv("YOUTUBE_API_KEY")
# Define YouTube API endpoint
YOUTUBE_URL_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"

# Function to get video IDs based on search query
def get_video_id(search_query, max_results):
    # Define search parameters
    params = {
        "part": "snippet",
        "q": search_query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY
    }

    # Try to send GET request to YouTube API
    try:
        response = requests.get(url = YOUTUBE_URL_ENDPOINT, params = params)
        # If the response indicates an error, raise an exception
        response.raise_for_status()
    # Catch and handle exceptions
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        return []
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return []
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return []
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return []

    # Convert the response data to JSON
    data = response.json()
    # Extract video IDs from the data
    video_ids = [item["id"]["videoId"] for item in data["items"]]

    # Get video urls
    #video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

    return video_ids

# Function to get video data based on video IDs
def get_video_data(search_query, max_results):
    # Get video IDs
    video_ids = get_video_id(search_query, max_results)
    # Define YouTube API endpoint
    url = f"https://www.googleapis.com/youtube/v3/videos"

    # Define search parameters
    params = {
        "part": "snippet,statistics",
        "id": ','.join(video_ids),
        "key": API_KEY
    }

    # Try to send GET request to YouTube API
    try:
        response = requests.get(url, params=params)
        # If the response indicates an error, raise an exception
        response.raise_for_status()
    # Catch and handle exceptions
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        return []
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return []
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return []
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return []

    # Convert the response data to JSON
    data = response.json()

    # Extract video data from the response
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

    # Return the video data as a JSON object
    return json.dumps(videos_data)

# Function to export video data to a CSV file
def export_to_csv(result):
    csv_file = "video_data.csv"
    with open(csv_file, mode="w", newline = "", encoding ="utf-8") as file:
        fieldnames = ["title", "likes", "dislikes", "views", "comments"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for video in result:
            writer.writerow(video)

    # Print a success message
    print(f"Video data exported to {csv_file}")

# Main function to run the script
def main():
    # Get video data for a specific search query
    result = json.loads(get_video_data("Database Tutorial", 1000))
    # Export the video data to a CSV file
    export_to_csv(result)

if __name__ == "__main__":
    main()
