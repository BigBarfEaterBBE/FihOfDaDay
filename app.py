from flask import Flask, render_template, jsonify
import datetime
import json
import requests

app = Flask(__name__)

# def get_fish_list():
#     return [
#         {
#             "scientific_name": "Paracanthurus hepatus",
#             "common_name": "Blue Tang"
#         },
#         {
#             "scientific_name": "Amphiprion ocellaris",
#             "common_name": "Clownfish"
#         }
#     ]

def get_fish_species_list():
    # temporary subset
    return [
        "Paracanthurus hepatus",
        "Amphiprion ocellaris",
        "Gadus morhua",
        "Thunnus albacares"
    ]

def get_fish_of_the_day():
    species_list = get_fish_species_list()
    if not species_list:
        return {
            "common_name": "No fish found",
            "scientific_name": "",
            "image_url": "",
            "habitat": ""
        }
    today = datetime.date.today()
    days_since_start = (today - datetime.date(2026, 4, 20)).days
    index = days_since_start % len(species_list)
    return species_list[index]

def get_inaturalist_image(scientific_name):
    url = "https://api.inaturalist.org/v1/observations"

    params = {
        "taxon_name": scientific_name,
        "photos": "true",
        "per_page": 1
    }

    res = requests.get(url,params=params)
    data = res.json()

    try:
        return data["results"][0]["photos"][0]["url"].replace("square", "medium")
    except:
        return None
    
def get_fishbase_data(scientific_name):
    try:
        genus, species = scientific_name.split(" ")

        url = "https://fishbase.ropensci.org/species"
        params = {
            "Genus": genus,
            "Species": species
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["data"]:
            info = data["data"][0]

            return {
                "common_name": info.get("FBname", scientific_name),
                "max_length_cm": info.get("Length"),
                "habitat": info.get("Habitat"),
                "family": info.get("Family")
            }
    except Exception as e:
        print("FishBase error:", e)

    return None
    
def enrich_fish(fish):
    #placeholder facts for now
    facts = {
        "Paracanthurus hepatus": {
            "habitat": "Coral reefs in the Indo-Pacific",
            "max_length_cm": 31,
            "fun_fact": "Can change color when stressed or sleeping."
        },
        "Amphiprion ocellaris": {
            "habitat": "Protected coral reefs",
            "max_length_cm": 11,
            "fun_fact": "Lives in symbiosis with sea anemones."
        }
    }

    data = facts.get(fish["scientific_name"], {
        "habitat": "Unknown",
        "max_length_cm": "Unknown",
        "fun_fact": "No available data yet"
    })

    fish.update(data)
    return fish

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/fish-of-the-day")
def fish_api():
    species_list = get_fish_species_list()

    today = datetime.date.today()
    days_since_start = (today - datetime.date(2026,4,20)).days

    index = days_since_start % len(species_list)
    species = species_list[index]

    # FishBase facts (placeholder for now)
    fish = {
        "scientific_name": species,
    }

    # add extra facts
    fishbase_data = get_fishbase_data(species)

    if fishbase_data:
        fish.update(fishbase_data)
    else:
        fish["common_name"] = species
        fish["max_length_cm"] = "Unknown"
        fish["habitat"] = "Unknown"
        fish["family"] = "Unknown"

    # iNaturalist image
    fish["image_url"] = get_inaturalist_image(fish["scientific_name"])

    return jsonify(fish)

if __name__ == "__main__":
    app.run(debug=True)