import requests
import json

# API details
url = "https://sportsbook-api2.p.rapidapi.com/v0/advantages/"
querystring = {"type": "ARBITRAGE"}
headers = {
    "x-rapidapi-key": "ef3058b4a2mshe108ada4b6202dep181435jsnc8563910c50c",
    "x-rapidapi-host": "sportsbook-api2.p.rapidapi.com"
}

# Get the response from the API
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# List to hold the filtered data
filtered_data = []

# Loop through advantages and collect the filtered data
for advantage in data.get('advantages', []):
    event = advantage.get('market', {}).get('event', {})
    competition_instance = event.get('competitionInstance', {})
    participants = event.get('participants', [])
    outcomes = advantage.get('outcomes', [])
    last_found_at = advantage.get('lastFoundAt')

    # Create a dictionary for the event
    event_info = {
        "event_name": event.get('name'),
        "competition_name": competition_instance.get('name'),
        "start_time": event.get('startTime'),
        "sport": participants[0].get('sport') if participants else "N/A",
        "last_found_at": last_found_at,
        "participants": [participant.get('name') for participant in participants],
        "outcomes": [
            {
                "type": outcome.get('type'),
                "source": outcome.get('source'),
                "payout": outcome.get('payout')
            } for outcome in outcomes
        ]
    }

    # Add the event info to the list
    filtered_data.append(event_info)

# Save the filtered data to a JSON file
with open('filtered_data.json', 'w') as json_file:
    json.dump(filtered_data, json_file, indent=4)

print("Data has been saved to 'filtered_data.json'")
