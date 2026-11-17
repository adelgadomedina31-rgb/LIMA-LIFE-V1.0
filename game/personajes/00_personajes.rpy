## =============================================================================
## LIMA GRIS - Personajes: objetos Character y orden
## =============================================================================
## Para agregar un personaje nuevo:
##   1. Crea su Character aquí (define xx = Character(...)).
##   2. Agrega su ficha en PJ (mira cualquier archivo datos_*.rpy como ejemplo).
##   3. Agrega su id a ORDEN_PJ.
##   Las partidas guardadas viejas lo reconocen solas al cargar.
## =============================================================================

define p = Character("[nombre]", color="#e0a040")
define narrator = Character(None, what_color="#e9e6df")

## Oficina
define va = Character("Valeria", color="#8fc7ff")
define ka = Character("Kathy", color="#ff9ecf")
define ma = Character("Mariela", color="#c9a7ff")
define fi = Character("Fiorella", color="#9ee6b8")
define ji = Character("Jimena", color="#d9c08f")
define br = Character("Brenda", color="#ffb98a")
define pi = Character("Piero", color="#a0b4c8")
define be = Character("Sr. Benavides", color="#b0b0b0")

## Tambo y barrio
define ye = Character("Yesenia", color="#ffd36e")
define da = Character("Dani", color="#ff8a8a")
define me = Character("Mery", color="#e6a86e")
define te = Character("Don Teo", color="#b9a58c")

## Edificio Los Ficus
define ro = Character("Rocío", color="#7fd6d0")
define an = Character("Andrea", color="#b8c4ff")
define lu = Character("Lucía", color="#f2b880")
define gladys = Character("Doña Gladys", color="#c0b7a8")

## Gimnasio
define mi = Character("Mila", color="#a6e36e")
define ca = Character("Camila", color="#ff9bb0")

## Otros
define so = Character("Sofía", color="#d8b4e2")
define cr = Character("Carla", color="#f08080")
define pa = Character("Paola", color="#b0c4de")
define norma = Character("Tía Norma", color="#d4b483")

init -2 python:
    PJ = {}

init 1 python:
    ORDEN_PJ = [
        "valeria", "kathy", "mariela", "fiorella", "jimena", "brenda", "piero", "benavides",
        "yesenia", "dani", "mery", "teofilo",
        "rocio", "andrea", "lucia", "gladys",
        "mila", "camila",
        "sofia", "carla", "paola",
    ]
    ## Cualquier personaje agregado en PJ que no esté en la lista, va al final.
    for _k in PJ:
        if _k not in ORDEN_PJ:
            ORDEN_PJ.append(_k)
