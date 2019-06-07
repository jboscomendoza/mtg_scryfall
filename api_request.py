import requests
import json
import re
from random import choices, seed

# Lectura de decklist
# "S" al inicio indica que inicia texto de "Sideboard"
def leer_decklist(archivo):
    deck = open(archivo, "r")
    deck = deck.readlines()
    i = 0
    decklist = []
    while not deck[i].startswith("S"):
        linea = deck[i]
        nombre = re.sub(r"^(\d)+ ", "", linea)
        nombre = re.sub(r"\n", "", nombre)
        cantidad = re.sub(" .*", "", linea)
        cantidad = int(cantidad)
        i += 1
        decklist.append([cantidad, nombre])
    return(decklist)


def crear_json(decklist):
    deck_json = []
    for carta in decklist:
        llave = "{\"name\": \"" + carta[1] + "\"}"
        deck_json.append(llave)
    deck_json = ", ".join(deck_json)
    deck_json = "{\"identifiers\":[" + deck_json + "]}"
    deck_json = json.loads(deck_json)
    return(deck_json)


def get_tipo(carta):
    carta = re.sub(" —(.*)", "", carta)
    carta = re.sub("(Legendary|Snow|Tribal|Basic) ", "", carta)
    return(carta)


def crear_stats(datos):
    nombres = []
    for carta in datos:
        nombres.append(carta["name"])
    
    stats = []
    for carta in datos:
        cmc = carta["cmc"]
        tipo = get_tipo(carta["type_line"])
        stats.append({"cmc": cmc, "tipo": tipo})
    
    dict_stats = dict(zip(nombres, stats))
    return(dict_stats)


def flat_lista(lista):
    flat = []
    for sub_lista in lista:
        for elemento in sub_lista:
            flat.append(elemento)
    return(flat)


def crear_pool(deck):
    pool = []
    for elemento in deck:
        copias = elemento[0] * [elemento[1]]
        pool.append(copias)
    pool = flat_lista(pool)
    return(pool)


scryfall = "https://api.scryfall.com"
carta_nombre = "/cards/named?fuzzy="
collection = "/cards/collection"


infect_ruta = "Modern_Infect_by_sirpuffsalot.txt"
infect_deck = leer_decklist(infect_ruta)


rdw_ruta = "Standard_Red_Deck_Wins_by_Adam_Bink.txt"

rdw_deck = leer_decklist(rdw_ruta)
rdw_json = crear_json(rdw_deck)
rdw_collection = requests.post(scryfall + collection, json=rdw_json)
rdw_dict = json.loads(rdw_collection._content)["data"]
rdw_stats = crear_stats(rdw_dict)
rdw_pool = crear_pool(rdw_deck)

def crear_trials(pool, num_trials):
    trials = []
    iteracion = 0
    while iteracion < num_trials:
        draw = choices(pool, k=7)
        trials.append(draw)
        iteracion += 1
    return(trials)

rdw_trials = crear_trials(rdw_pool, 100)

cartas_buscadas = ["Mountain", "Shock", "Lightning Strike"]

def probar_draws(cartas_buscadas, trials):
    resultados = []
    for trial in trials:
        exito = set(cartas_buscadas).issubset(trial)
        resultados.append(exito)
    return(sum(resultados) / len(resultados))

probar_draws(cartas_buscadas, rdw_trials)