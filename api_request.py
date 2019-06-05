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

ruta_infect = "Modern_Infect_by_sirpuffsalot.txt"
ruta_rdw = "Standard_Red_Deck_Wins_by_Adam_Bink.txt"
deck_infect = leer_decklist(ruta_infect)
deck_rdw = leer_decklist(ruta_rdw)

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

rdw_json = []
for carta in deck_rdw:
    llave = "{\"name\": \"" + carta[1] + "\"}"
    rdw_json.append(llave)
rdw_json = ", ".join(rdw_json)
rdw_json = "{\"identifiers\":[" + rdw_json + "]}"
rdw_json = json.loads(rdw_json)

rdw_collection = requests.post("https://api.scryfall.com/cards/collection", json=rdw_json)

rdw_collection._content