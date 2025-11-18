import pandas as pd
import matplotlib.pyplot as plt
import squarify
import matplotlib.colors as mcolors

# Load the data (assuming Visuals.csv contains player names and win shares)
data = pd.read_csv('Visuals.csv')

# Sort data by Win Shares in descending order
data = data.sort_values(by='WS', ascending=False)

# Round win shares to 1 decimal place
data['WS'] = data['WS'].round(1)

# Create labels with player names and their win shares
labels = [f'{name}\n{ws} WS' for name, ws in zip(data['Name'], data['WS'])]

# Define sizes for the squares in the treemap (based on win shares)
sizes = data['WS']

# Scale the sizes to adjust the visual decrease
scaling_factor = 2  # Adjust this value to control the scaling effect
scaled_sizes = sizes ** scaling_factor  # Applying scaling to sizes

# Normalize the scaled sizes for color mapping
norm = plt.Normalize(min(scaled_sizes), max(scaled_sizes))
cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", ["#aabe2a", "#570000"])  # Dark red to light yellow
colors = [cmap(norm(value)) for value in scaled_sizes]

# Plot the treemap with adjusted sizes
plt.figure(figsize=(30, 15))  # Adjust figure size for 25 players
squarify.plot(sizes=scaled_sizes, label=labels, color=colors, alpha=0.9, pad=True,
              text_kwargs={'fontsize': 12, 'fontname': 'Georgia', 'color': 'white', 'weight': 'bold'})

# Ensure the layout starts from top left to bottom right with squares proportional to WS
plt.gca().invert_yaxis()  # To start from top-left as the highest

# Title and display settings
plt.title('Top 25 Players by Win Shares', fontsize=18, fontname='Georgia', color='white', weight='bold')
plt.axis('off')

# Save and show the plot
plt.savefig('Win_Shares_25.png', dpi=500, bbox_inches='tight')
plt.show()
