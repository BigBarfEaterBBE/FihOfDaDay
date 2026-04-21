import requests
import json
import time

BASE_URL = "https://fishbase.ropensci.org/species"

all_species = []
limit = 500 # num per request
offset = 0
max_records = 12000 # num of total species

print("starting download...")

while offset < max_records:
    print(f"Fetching offset {offset}...")

    params = {
        "limit": limit,
        "offset": offset
    }

    response = requests.get(BASE_URL,params=params, verify=False)
    
    print(response.status_code)
    print(response.text[:500])

    if not data["data"]:
        break

    for fish in data["data"]:
        if fish.get("Genus") and fish.get("Species"):
            all_species.append({
                "scientific_name": f"{fish['Genus']} {fish['Species']}",
                "common_name": fish.get("FBname"),
                "family": fish.get("Family"),
                "max_length_cm": fish.get("Length"),
                "habitat": fish.get("Habitat")
            })
        
    offset += limit
    time.sleep(0.5) # give time to API

print("Download complete")
print(f"Total species collected: {len(all_species)}")

with open("fish_data.json", "w", encoding="utf-8") as f:
    json.dump(all_species, f, indent=2)

print("saved to fish_data.json")