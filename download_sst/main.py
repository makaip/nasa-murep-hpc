import os
import requests
from datetime import datetime, timedelta

# Define the base URL and dataset ID
base_url = "https://neo.gsfc.nasa.gov/archive/geotiff.float"
dataset_id = "MYD28M"

# Define the start and end dates for June 2024
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 6, 30)

# Create a directory to save the downloaded files
output_dir = "/mnt/beegfs/groups/ouri_project/satdata/sst/"
os.makedirs(output_dir, exist_ok=True)

# Loop through the dates in 8-day intervals
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    filename = f"{dataset_id}_{date_str}_float.tif"
    url = f"{base_url}/{dataset_id}/{filename}"
    output_path = os.path.join(output_dir, filename)

    # Download the file
    print(f"Downloading {filename}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved to {output_path}")
    else:
        print(f"Failed to download {filename}: HTTP {response.status_code}")

    # Increment the date by 8 days
    current_date += timedelta(days=8)
