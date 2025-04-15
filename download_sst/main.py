import os
import requests
from datetime import datetime, timedelta

# Create a directory to save the downloaded files
output_dir = "/mnt/beegfs/groups/ouri_project/satdata/sst/"
os.makedirs(output_dir, exist_ok=True)

# Define the specific time periods for June 2024 with their corresponding identifiers
june_periods = [
    {"start": "2024-06-01", "end": "2024-06-09", "si": "1955852"},
    {"start": "2024-06-09", "end": "2024-06-17", "si": "1955844"},
    {"start": "2024-06-17", "end": "2024-06-25", "si": "1955846"},  # Updated with correct si value
    {"start": "2024-06-25", "end": "2024-07-03", "si": "1955854"}   # Updated with correct si value
]

# Base URL format for the data
base_url = "https://neo.gsfc.nasa.gov/servlet/RenderData"
params = {
    "cs": "gs",
    "format": "TIFF",
    "width": "3600",
    "height": "1800"
}

# Loop through each time period and download the data
for period in june_periods:
    # Update the si parameter for this period
    params["si"] = period["si"]
    
    # Create filename based on date range
    start_date = period["start"]
    end_date = period["end"]
    filename = f"SST_{start_date}_to_{end_date}.tif"
    output_path = os.path.join(output_dir, filename)
    
    # Download the file
    print(f"Downloading data for {start_date} to {end_date}...")
    print(f"URL parameters: {params}")
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved to {output_path}")
    else:
        print(f"Failed to download: HTTP {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # Print partial response for debugging
