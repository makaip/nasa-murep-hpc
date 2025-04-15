import csv
import requests
import os
import argparse

from dotenv import load_dotenv

load_dotenv()
DEFAULT_TOKEN = os.getenv("DEFAULT_TOKEN")
DEFAULT_DOWNLOAD_FOLDER = "/mnt/beegfs/groups/ouri_project/satdata/modis/"

def download_file(url, destination_folder, token):
    file_name = url.split('/')[-1]
    file_path = os.path.join(destination_folder, file_name)
    os.makedirs(destination_folder, exist_ok=True)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}. Error: {e}")

def download_files_from_csv(csv_file_path, destination_folder, token, column_name):
    with open(csv_file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Ensure proper URL concatenation
                file_path = row[column_name].lstrip('/')
                full_url = f"https://ladsweb.modaps.eosdis.nasa.gov/{file_path}"
                download_file(full_url, destination_folder, token)
            except KeyError as e:
                print(f"Missing expected column in CSV: {e}. Available columns: {reader.fieldnames}")

def parse_arguments(): 
    parser = argparse.ArgumentParser(description="Download files from URLs specified in a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file containing the file URLs.")
    parser.add_argument("--download_folder", default=DEFAULT_DOWNLOAD_FOLDER, 
                        help=f"Path to the folder where files will be downloaded. Default: {DEFAULT_DOWNLOAD_FOLDER}")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="Bearer token for authentication (optional, defaults to token in script).")
    parser.add_argument("--column_name", default="fileUrls for custom selected", 
                        help="Name of the column in the CSV file containing the file URLs. Default: 'fileUrls for custom selected'")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Files will be downloaded to: {args.download_folder}")
    download_files_from_csv(args.csv_file, args.download_folder, args.token, args.column_name)
