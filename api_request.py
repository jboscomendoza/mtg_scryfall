import requests
import json
import re

# Lectura de decklist
# "S" al inicio indica que inicia texto de "Sideboard"
def leer_decklist(archivo):
    deck = open(archivo, "r")
    deck = deck.readlines()
    i = 0
    decklist = []
    while not deck[i].startswith("S"):
        linea = deck[i]
        nombre = re.sub("^(\d)+ ", "", linea)
        nombre = re.sub("\n", "", nombre)
        cantidad = re.sub(" .*", "", linea)
        cantidad = int(cantidad)
        i += 1
        decklist.append([cantidad, nombre])
    return(decklist)

infect_ruta = "Modern_Infect_by_sirpuffsalot.txt"
rdw_ruta = "Standard_Red_Deck_Wins_by_Adam_Bink.txt"
infect_deck = leer_decklist(ruta_infect)
rdw_deck = leer_decklist(ruta_rdw)

# Consulta al API de scryfall
scryfall = "https://api.scryfall.com"
carta_nombre = "/cards/named?fuzzy="
collection = "/cards/collection"

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

cartas_lista = {"identifiers":[
    {"name": "Shock"},
    {"name": "Viashino Pyromancer"}
]}

requests.post("https://api.scryfall.com/cards/collection", json=cartas_lista)

def crear_json(decklist):
    deck_json = []
    for carta in decklist:
        llave = "{\"name\": \"" + carta[1] + "\"}"
        deck_json.append(llave)
    deck_json = ", ".join(deck_json)
    deck_json = "{\"identifiers\":[" + deck_json + "]}"
    deck_json = json.loads(deck_json)
    return(deck_json)

rdw_json = crear_json(rdw_deck)

rdw_collection = requests.post("https://api.scryfall.com/cards/collection", json=rdw_json)

rdw_collection._content
rdw_dict = json.loads(rdw_collection._content)

for card in rdw_dict["data"]:
    print([card["name"], card["cmc"]])