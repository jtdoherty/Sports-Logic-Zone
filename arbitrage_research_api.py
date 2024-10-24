import requests
import json
import os
import sys
from datetime import datetime

def fetch_arbitrage_data():
    """
    Fetches arbitrage data from the RapidAPI endpoint and returns filtered data
    """
    # Get API key from environment variable
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        raise ValueError("RAPIDAPI_KEY environment variable not found")

    # API configuration
    url = "https://sportsbook-api2.p.rapidapi.com/v0/advantages/"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sportsbook-api2.p.rapidapi.com"
    }
    params = {"type": "ARBITRAGE"}

    # Make API request
    print(f"Making API request at {datetime.now().isoformat()}")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    advantages = data.get('advantages', [])
    print(f"Received {len(advantages)} advantages from API")
    
    return advantages

def process_advantages(advantages):
    """
    Processes the advantages data and returns filtered information
    """
    filtered_data = []
    
    for advantage in advantages:
        event = advantage.get('market', {}).get('event', {})
        competition_instance = event.get('competitionInstance', {})
        participants = event.get('participants', [])
        outcomes = advantage.get('outcomes', [])
        
        event_info = {
            "event_name": event.get('name'),
            "competition_name": competition_instance.get('name'),
            "start_time": event.get('startTime'),
            "sport": participants[0].get('sport') if participants else "N/A",
            "last_found_at": advantage.get('lastFoundAt'),
            "profit_percentage": advantage.get('profitPercentage'),
            "participants": [participant.get('name') for participant in participants],
            "outcomes": [
                {
                    "type": outcome.get('type'),
                    "source": outcome.get('source', {}).get('name'),
                    "payout": outcome.get('payout'),
                    "odds": outcome.get('odds')
                } for outcome in outcomes
            ]
        }
        filtered_data.append(event_info)
    
    return filtered_data

def save_data(data, filename):
    """
    Saves the data to a JSON file and verifies the save
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
    
    # Verify file was created and has content
    file_size = os.path.getsize(filename)
    print(f"Data saved to '{filename}' (Size: {file_size} bytes)")
    
    if file_size == 0:
        raise ValueError(f"Error: {filename} is empty after saving")

def main():
    try:
        # Fetch data from API
        advantages = fetch_arbitrage_data()
        
        # Process the data
        filtered_data = process_advantages(advantages)
        
        if not filtered_data:
            print("Warning: No data to save")
            return
        
        # Save the processed data
        save_data(filtered_data, 'filtered_data.json')
        
        print("Data processing completed successfully")
        
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
