import requests
import json

scryfall = "https://api.scryfall.com"
github = "https://api.github.com"
carta_nombre = "/cards/named?fuzzy="

war = requests.get(scryfall + "/sets/war")
eternal_witness = requests.get(scryfall + carta_nombre + "Eternal Witness")

war.status_code
war._content

eternal_witness.status_code
eternal_witness._content

ew_json = json.loads(eternal_witness._content)
ew_json["flavor_text"]

ew_json["cmc"] <= 2
"Creature" in ew_json["type_line"]
