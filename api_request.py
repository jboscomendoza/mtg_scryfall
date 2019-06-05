import requests
scryfall = "https://api.scryfall.com"
github = "https://api.github.com"
carta_nombre = "/cards/named?fuzzy="

war = requests.get(scryfall + "/sets/war")
eternal_witness = requests.get(scryfall + carta_nombre + "Eternal Witness")

war.status_code
war._content

eternal_witness.status_code
eternal_witness._content
