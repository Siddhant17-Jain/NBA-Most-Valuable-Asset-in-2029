import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


# Function to scrape the list of top 78 NBA players from HoopsHype
def get_top_78_players():
    url = "https://hoopshype.com/lists/78-greatest-nba-players-ever-hoopshype-list/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements that contain player names under the class "listicle-header-text"
    player_elements = soup.find_all('span', class_='listicle-header-text')

    # Extract player names
    players = [player.get_text(strip=True) for player in player_elements]

    return players


# Function to convert player name to Basketball Reference URL format
def get_basketball_reference_url(player_name):
    name_parts = player_name.lower().split()
    last_name = name_parts[-1]
    first_name = name_parts[0]
    # Build the URL based on the Basketball Reference player page format
    player_url = f"https://www.basketball-reference.com/players/{last_name[0]}/{last_name[:5]}{first_name[:2]}01.html"
    print(f"Generated URL for {player_name}: {player_url}")  # Debug print
    return player_url


# Function to scrape the "Advanced" stats table for a player
def scrape_advanced_stats(player_name):
    try:
        url = get_basketball_reference_url(player_name)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the "Advanced" stats table by its ID
        table = soup.find('table', {'id': 'advanced'})
        if table is None:
            print(f"Advanced stats table not found for {player_name}")
            return None

        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]
        return df
    except Exception as e:
        print(f"Error scraping {player_name}: {e}")
        return None


# Function to save the DataFrame to a CSV file in the format "firstname_lastname.csv"
def save_player_stats_to_csv(df, player_name):
    # Convert player name to the format "firstname_lastname"
    name_parts = player_name.split()
    filename = f"{name_parts[0].lower()}_{name_parts[-1].lower()}.csv"

    # Create the directory if it doesn't exist
    folder = "NBA Top 75"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the DataFrame to the CSV file
    file_path = os.path.join(folder, filename)
    df.to_csv(file_path, index=False)
    print(f"Saved stats for {player_name} to {file_path}")


# Main function to download stats for all players
def download_advanced_stats_for_top_78():
    players = get_top_78_players()
    print(f"Found {len(players)} players")  # Debug print

    for player in players:
        print(f"Scraping advanced stats for {player}...")
        stats_df = scrape_advanced_stats(player)

        if stats_df is not None:
            save_player_stats_to_csv(stats_df, player)

        # Sleep for a short time to avoid overwhelming the server
        time.sleep(2)


# Run the script
download_advanced_stats_for_top_78()


# Function to get the list of players from HoopsHype
def get_top_78_players():
    url = "https://hoopshype.com/lists/78-greatest-nba-players-ever-hoopshype-list/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements that contain player names under the class "listicle-header-text"
    player_elements = soup.find_all('span', class_='listicle-header-text')

    # Extract player names
    players = [player.get_text(strip=True) for player in player_elements]

    return players


# Function to convert player name to the corresponding CSV filename
def player_name_to_filename(player_name):
    name_parts = player_name.split()
    filename = f"{name_parts[0].lower()}_{name_parts[-1].lower()}.csv"
    return filename


# Function to find players whose advanced stats were not downloaded
def find_missing_players():
    players = get_top_78_players()

    # Get list of all files in the "NBA Top 75" directory
    downloaded_files = set(os.listdir(''))

    # Find players whose files are missing
    missing_players = []
    for player in players:
        filename = player_name_to_filename(player)
        if filename not in downloaded_files:
            missing_players.append(player)

    return missing_players


# Get the list of players whose stats are missing
missing_players = find_missing_players()

# Print the missing players
print("Players whose advanced stats were not downloaded:")
for player in missing_players:
    print(player)
