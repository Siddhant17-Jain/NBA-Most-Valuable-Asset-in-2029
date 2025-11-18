import pandas as pd
import os
import matplotlib.pyplot as plt

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

# Calculate the Win Shares per Year (WS/Yrs), handling cases where Yrs is zero
final_df['WS/Yrs'] = final_df['WS'] / final_df['Yrs'].replace(0, pd.NA)

# Save the final DataFrame with totals and WS/Yrs to a new CSV file
final_df.to_csv("Totals.csv", index=False)
print("Aggregated results with WS/Yrs have been saved to 'Totals.csv'.")

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(final_df['Pk'], final_df['WS/Yrs'], color='skyblue')
plt.xlabel('Pick (Pk)')
plt.ylabel('Win Shares per Year (WS/Yrs)')
plt.title('Win Shares per Year by Pick')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Save the bar graph as an image file
plt.savefig("WS_Yrs_vs_Pk.png")

# Show the plot (optional, can be removed if running in a script)
plt.show()

print("Bar graph has been saved as 'WS_Yrs_vs_Pk.png'.")
