# YTDataMiner

## Description
**YTDataMiner**: This repository contains a Python script that uses the YouTube API to fetch data related to specific search queries. For instance, if you search for 'Database Tutorial', it retrieves all the videos related to this topic, extracts their data, and neatly organizes it into a CSV file. This tool is perfect for those who need to analyze YouTube video data in a structured and easily accessible format.

## Features
- Fetches data from YouTube based on user-defined search queries.
- Extracts comprehensive data for each video result.
- Organizes and stores data in a structured CSV file for easy analysis.
- Handles potential errors during the execution.

## Usage
1. Clone the repository to your local machine.
2. Install the required Python packages with `pip install -r requirements.txt`.
3. Run the script with your desired search query as an argument.
4. The script will create a CSV file in the same directory with the extracted data.

## Requirements
- Python 3.6 or higher
- YouTube Data API v3
- Python packages: os, json, csv, requests, python-dotenv

Please note that you will need to obtain your own API key from the Google Cloud Console and enable the YouTube Data API v3 for your project.

## Contributing
Contributions are welcome!
