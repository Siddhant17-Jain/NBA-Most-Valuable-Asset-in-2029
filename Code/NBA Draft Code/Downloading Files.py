import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create a directory to save the files
output_folder = "Drafts"
os.makedirs(output_folder, exist_ok=True)

# Loop through each year from 1979 to 2023
for year in range(2024):
    url = f"https://www.basketball-reference.com/draft/NBA_2023.html"
    print(f"Processing {url}")

    # Send an HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    # Find the table in the HTML
    table = soup.find('table')

    if table:
        # Read the HTML table into a DataFrame
        df = pd.read_html(str(table))[0]

        # Save the DataFrame to a CSV file
        file_path = os.path.join(output_folder, f"{year}.csv")
        df.to_csv(file_path, index=False)
        print(f"Saved data for {year} to {file_path}")
    else:
        print(f"No table found for {year}")

print("All drafts have been processed.")
