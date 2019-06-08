import requests
import json
import re
from random import choices, seed


def flat_lista(lista):
    flat = []
    for sub_lista in lista:
        for elemento in sub_lista:
            flat.append(elemento)
    return(flat)


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
    # Reemplaza subtipos
    carta = re.sub(" . (.*)", "", carta)
    # Quita super tipos mas comunes
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


def crear_pool(deck):
    pool = []
    for elemento in deck:
        copias = elemento[0] * [elemento[1]]
        pool.append(copias)
    pool = flat_lista(pool)
    return(pool)


def crear_trials(pool, num_trials):
    trials = []
    iteracion = 0
    while iteracion < num_trials:
        draw = choices(pool, k=7)
        trials.append(draw)
        iteracion += 1
    return(trials)


def probar_draws(cartas_buscadas, trials):
    draws = []
    for trial in trials:
        exito = set(cartas_buscadas).issubset(trial)
        draws.append(exito)
    hits = sum(draws)
    misses = len(draws) - hits
    hit_rate = hits / len(draws)
    resultados = {"hits": hits, "misses": misses, "hit_rate": hit_rate}
    return(resultados)


def get_collection(deck_json):
    deck_collection = requests.post(SCRYFALL + COLLECTION, json=deck_json)
    deck_collection = json.loads(deck_collection._content)["data"]
    return(deck_collection)


def generar_mazo(ruta):
    decklist = leer_decklist(ruta)
    mazo_json = crear_json(decklist)
    collection = get_collection(mazo_json)
    stats = crear_stats(collection)
    mazo = {"decklist": decklist, "stats": stats}
    return(mazo)


def generar_simulacion(mazo, cartas_buscadas, reps=10000):
    pool = crear_pool(mazo["decklist"])
    trials = crear_trials(pool, reps)
    draws = probar_draws(cartas_buscadas, trials)
    return(draws)


SCRYFALL = "https://api.scryfall.com"
CARDNAME = "/cards/named?fuzzy="
COLLECTION = "/cards/collection"


rdw_ruta = "Standard_Red_Deck_Wins_by_Adam_Bink.txt"
rdw_buscadas = ["Mountain", "Fanatical Firebrand", "Light Up the Stage"]

rdw_mazo = generar_mazo(rdw_ruta)
rdw_simulacion = generar_simulacion(rdw_mazo, rdw_buscadas, 10000)


# infect_ruta = "Modern_Infect_by_sirpuffsalot.txt"
# infect_buscadas = ["Glistener Elf", "Vines of Vastwood"]
# infect_deck = leer_decklist(infect_ruta)
#
# infect_deck = leer_decklist(infect_ruta)
# infect_json = crear_json(infect_deck)
# infect_collection = get_collection(infect_json)
# infect_stats = crear_stats(infect_collection)
# 
# infect_pool = crear_pool(infect_deck)
# infect_trials = crear_trials(infect_pool, 5000)
# infect_draws = probar_draws(cartas_buscadas, infect_trials)
