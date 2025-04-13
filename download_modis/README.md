# Downloading MODIS Data Using the Script

Follow these steps to download data using the provided script:

## 1. Generate a Token
1. Go to [LAADS DAAC](https://ladsweb.modaps.eosdis.nasa.gov/).
2. Log in to your account.
3. Navigate to **Login > Generate Token** and generate an API token.
4. Save the token in the `.env` file in this directory.

## 2. Search for Data
1. Visit the [Search Page](https://ladsweb.modaps.eosdis.nasa.gov/search/).
2. Under **Products**, select **MODIS Terra, Aqua** and click on **MOD021KM**.
3. Under **Time**, select the desired time range.
4. Under **Location**, click **Enter Coordinates** and input the following coordinates:
   ```
   -94, 27.5, -88, 30.5
   ```
   Then, click the **+** button to add the location.

## 3. Download Query Results
1. Go to the **Files** section.
2. Select **Download query results as JSON or CSV** and click **CSV**.
3. Save the downloaded CSV file.
4. Copy the contents of the CSV file into `downloads.csv` in this directory.

## 4. Run the Download Script
Run the script using the following command:
```bash
sbatch download_job.sh <csv_file_path>
```
Replace `<csv_file_path>` with the path to `downloads.csv` (e.g., `downloads.csv`).


