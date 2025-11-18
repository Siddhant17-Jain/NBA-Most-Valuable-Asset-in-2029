import pandas as pd
import os

# Folder where CSV files are stored
folder_path = ".."


# Function to process each CSV file
def process_csv_file(file_path):
    # Read the CSV file, skipping the first row
    df = pd.read_csv(file_path)

    # Convert the 'Pk' column to numeric, forcing errors to NaN
    df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')

    # Filter rows where Pk <= 60 and drop rows where Pk is NaN
    df_filtered = df[df['Pk'] <= 30].dropna(subset=['Pk'])

    # Select only the columns 'Pk', 'Yrs', and 'WS'
    df_filtered = df_filtered[['Pk', 'Yrs', 'WS']]

    # Save the modified DataFrame back to the CSV file
    df_filtered.to_csv(file_path, index=False)
    print(f"Processed and saved: {file_path}")


# Loop through each CSV file from 1979 to 2023
for year in range(1979, 2024):
    file_name = f"{year}.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        process_csv_file(file_path)
    else:
        print(f"File not found: {file_path}")

print("All files have been processed.")
