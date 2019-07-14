import requests
import json
import re
import io
from PIL import Image
from PIL.ImageQt import ImageQt
from random import choices, seed

# Funciones auxiliares
def aplanar_lista(lista):
    flat = []
    for sub_lista in lista:
        for elemento in sub_lista:
            flat.append(elemento)
    return(flat)

def get_tipo(carta):
    # Reemplaza subtipos
    carta = re.sub(r" . (.*)", "", carta)
    # Quita super tipos mas comunes
    carta = re.sub(r"(Legendary|Snow|Tribal|Basic) ", "", carta)
    return(carta)


def checar_deck(deck_clean):
    # Patron para: numero de cartas, nombre de carta
    patron_deck = r"^\d{1,2} \w+"
    estado = all(re.match(patron_deck, elemento) for elemento in deck_clean)
    return(estado)


# Lectura de decklist
# "S" al inicio indica que inicia texto de "Sideboard"
def leer_deck_raw(archivo):
    deck_raw = open(archivo, "r")
    deck_raw = deck_raw.readlines()
    deck_clean = []
    for carta in deck_raw:
        if not carta.startswith(("S", "/")):
            carta = re.sub(r"\[.*?\]", "", carta)
            carta = re.sub(r" {2,}", " ", carta)
            deck_clean.append(carta)
    if checar_deck(deck_clean):
        return(deck_clean)
    else:
        return("Decklist invalido")

def crear_deck_list(deck_raw):
    deck_list = []
    i = 0
    for linea in deck_raw:
        nombre = re.sub(r"^(\d)+ ", "", linea)
        nombre = re.sub(r"\n", "", nombre)
        cantidad = re.sub(r" .*", "", linea)
        cantidad = re.sub(r"\n", "", cantidad)
        try:
            cantidad = int(cantidad)
        except ValueError:
            cantidad = 0
        i += 1
        deck_list.append([cantidad, nombre])
    return(deck_list)


def crear_json(deck_list):
    deck_json = []
    for carta in deck_list:
        llave = "{\"name\": \"" + carta[1] + "\"}"
        deck_json.append(llave)
    deck_json = ", ".join(deck_json)
    deck_json = "{\"identifiers\":[" + deck_json + "]}"
    deck_json = json.loads(deck_json)
    return(deck_json)


def get_collection(deck_json):
    deck_collection = requests.post(SCRYFALL + COLLECTION, json=deck_json)
    deck_collection = json.loads(deck_collection._content)["data"]
    return(deck_collection)


def get_decklist_text(collection, deck_raw):
    main_deck = range(len(collection))
    deck_data = [["Cantidad", "Nombre", "Costo", "Tipo", "Rareza", "Precio"]]

    for elemento in main_deck:
        carta = collection[elemento]
        nombre = carta["name"]
        
        numero = 0
        for texto in deck_raw:
            if nombre in texto:
                numero = re.sub(r" .*\n", "", texto)
        
        costo = carta["mana_cost"]
        if len(costo) == 0:
            costo = ""
        else:
            costo = re.sub(r"\W", "", costo)
        
        tipo = get_tipo(carta["type_line"])
        rareza = carta["rarity"]
        rareza = rareza.capitalize()
        precio = carta["prices"]["usd"]
        
        carta_data = [numero, nombre, costo, tipo, rareza, precio]
        #carta_data = "; ".join(carta_data)
        carta_data = carta_data# + "\n"
        
        deck_data.append(carta_data)
    deck_data = aplanar_lista(deck_data)
    return(deck_data)


def generar_mazo(ruta):
    deck_raw = leer_deck_raw(ruta)
    deck_list = crear_deck_list(deck_raw)
    mazo_json = crear_json(deck_list)
    collection = get_collection(mazo_json)
    decklist_text = get_decklist_text(collection, deck_raw)
    #decklist_text = "".join(decklist_text)
    mazo = {
        "decklist": deck_list, 
        "decklist_text": decklist_text, 
        "collection": collection
    }
    return(mazo)


# Simulacion
def crear_pool(deck):
    pool = []
    for elemento in deck:
        copias = elemento[0] * [elemento[1]]
        pool.append(copias)
    pool = aplanar_lista(pool)
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
    hit_rate = (hits / len(draws)) * 100
    hit_rate = round(hit_rate, 2)
    hit_rate = str(hit_rate) + "%"
    resultados = {"Hits": hits, "Misses": misses, "Hit rate": hit_rate}
    return(resultados)


def generar_simulacion(mazo, cartas_buscadas, reps=10000):
    if isinstance(cartas_buscadas, str):
        cartas_buscadas = [cartas_buscadas]
    pool = crear_pool(mazo["decklist"])
    trials = crear_trials(pool, reps)
    draws = probar_draws(cartas_buscadas, trials)
    return(draws)


def print_sim(simulacion):
    sim_texto = []
    for key, value in simulacion.items():
        texto = key + ": " + str(value) + "\n"
        sim_texto.append(texto)
    sim_texto = "".join(sim_texto)
    return(sim_texto)


def get_carta_pic(nombre_carta):
    carta_url = SCRYFALL + CARDNAME + nombre_carta + "&format=image&version=normal"
    carta_data = requests.get(carta_url)
    carta_data = carta_data.content
    carta_stream = io.BytesIO(carta_data)
    carta_pic = Image.open(carta_stream)
    return(carta_pic)


SCRYFALL = "https://api.scryfall.com"
CARDNAME = "/cards/named?fuzzy="
COLLECTION = "/cards/collection"


# leer_deck_raw("decklist_invalido.txt")
# leer_deck_raw("Standard_Esper_Hero_Control_by_Brad_Nelson.mwDeck")
#
# rdw_ruta = "Standard_Red_Deck_Wins_by_Adam_Bink.txt"
# rdw_buscadas = ["Mountain", "Fanatical Firebrand", "Light Up the Stage"]
# rdw_mazo = generar_mazo(rdw_ruta)
# rdw_simulacion = generar_simulacion(rdw_mazo, rdw_buscadas, 10000)
# print_sim(rdw_simulacion)
#
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
