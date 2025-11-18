import pandas as pd
import os

# Folder where CSV files are stored
folder_path = ".."

# Initialize an empty DataFrame to store aggregated results
aggregated_df = pd.DataFrame(columns=['Pk', 'Yrs', 'WS'])

# Loop through each CSV file from 1979 to 2023
for year in range(1979, 2024):
    file_name = f"{year}.csv"
    file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Convert the 'Pk' column to numeric, forcing errors to NaN
        df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')

        # Drop rows where 'Pk' is NaN
        df = df.dropna(subset=['Pk'])

        # Group by 'Pk' and sum the 'Yrs' and 'WS' columns
        df_grouped = df.groupby('Pk', as_index=False)[['Yrs', 'WS']].sum()

        # Append the grouped data to the aggregated DataFrame
        aggregated_df = pd.concat([aggregated_df, df_grouped], ignore_index=True)
    else:
        print(f"File not found: {file_path}")

# After processing all files, group the aggregated DataFrame by 'Pk' and sum 'Yrs' and 'WS' across all files
final_df = aggregated_df.groupby('Pk', as_index=False)[['Yrs', 'WS']].sum()

# Save the final aggregated DataFrame to a new CSV file
final_df.to_csv("Totals.csv", index=False)
print("Aggregated results have been saved to 'Totals.csv'.")
