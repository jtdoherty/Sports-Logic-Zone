import requests
import pandas as pd
import json
import os
from github import Github

# Define the API URL and parameters for PLUS_EV_AVERAGE
url = "https://sportsbook-api2.p.rapidapi.com/v0/advantages/"
querystring = {"type": "PLUS_EV_AVERAGE"}

# Define the headers for the request
headers = {
    "x-rapidapi-key": os.environ['RAPIDAPI_KEY'],
    "x-rapidapi-host": "sportsbook-api2.p.rapidapi.com"
}

# Make the API request
response = requests.get(url, headers=headers, params=querystring)

# Parse the JSON response
data = response.json()

# Initialize a list to store filtered data
filtered_data_list = []

# Check if there are advantages available
if 'advantages' in data and data['advantages']:
    # Loop through the advantages and filter the data
    for advantage in data['advantages']:
        # Define the keys you want to keep
        outcomes = advantage.get('outcomes', [])
        participant = outcomes[0]['participant'] if outcomes else None
        
        # Extract values needed for calculations
        implied_probability = advantage['marketStatistics'][0]['value'] if advantage['marketStatistics'] else None
        outcome_payout = outcomes[0]['payout'] if outcomes else None

        # Calculate profit potential and EV if values are available
        if implied_probability is not None and outcome_payout is not None:
            profit_potential = (outcome_payout - 1) * 100
            implied_probability_decimal = implied_probability / 100
            EV = (implied_probability_decimal * profit_potential) - ((1 - implied_probability_decimal) * 100)
        else:
            profit_potential = None
            EV = None

        # Extract additional information
        event_start_time = advantage['market']['event']['startTime'] if 'startTime' in advantage['market']['event'] else None
        competition_instance_name = advantage['market']['event']['competitionInstance']['name'] if 'competitionInstance' in advantage['market']['event'] else None

        filtered_data = {
            'key': advantage['key'],
            'edge': advantage['type'],
            'lastFoundAt': advantage['lastFoundAt'],
            'type': advantage['market']['type'],
            'market_name': advantage['market']['event']['name'],
            'participants': [p['name'] for p in advantage['market']['event']['participants']],
            'outcome_payout': outcome_payout,
            'source': outcomes[0]['source'] if outcomes else None,
            'participant': participant['name'] if participant else None,
            'sport': participant['sport'] if participant else None,
            'implied_probability': implied_probability,
            'profit_potential': profit_potential,
            'EV': EV,
            'event_start_time': event_start_time,
            'competition_instance_name': competition_instance_name
        }

        # Append the filtered data to the list
        filtered_data_list.append(filtered_data)

    # Convert the list of filtered data to a DataFrame
    df = pd.DataFrame(filtered_data_list)

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records')

    # Update the JSON file
    json_file_path = "research/output7.json"
    with open(json_file_path, 'w') as f:
        json.dump(json.loads(json_data), f, indent=4)

    print(f"JSON file updated: {json_file_path}")
else:
    print("No advantages available for PLUS_EV_AVERAGE.")
