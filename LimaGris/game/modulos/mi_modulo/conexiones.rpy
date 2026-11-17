## =============================================================================
## MI MÓDULO - Conexiones
## =============================================================================
## Aquí dices QUÉ escena tuya se usa, CON QUIÉN y CUÁNDO.
## El juego revisa la lista de arriba hacia abajo y usa la PRIMERA que cumpla
## los requisitos. Si la escena (label) no existe, la ignora y sigue.
## Si ninguna cumple, el juego hace su fundido a negro normal.
##
## Cada conexión es un diccionario:
##   {
##     "personaje": "valeria",        # id del personaje, o "*" para cualquiera
##     "escena": "mi_label",          # nombre del label en escenas/*.rpy
##     "requisitos": { ... },         # ver abajo (todo es opcional)
##   }
##
## Requisitos posibles:
##   "punto":      "intimidad" (por defecto), "despertar", "beso", "cita", "evento"
##   "lugar":      un lugar o lista de lugares. Para "intimidad" y "despertar":
##                 depa_tuyo, depa_ella, hostal, hotel, oficina, azotea,
##                 callejon, carro, almacen, vestidor, trastienda.
##                 Para "cita": cafe, cevicheria, cine, malecon, cena, bar.
##                 Para "evento": el id del evento (ej. "val_05", "kat_06").
##   "afecto", "confianza", "atraccion":  mínimo (0-100)
##   "estado":     mínimo: "Conocida", "Amiga", "Saliendo", "Pareja" (o 0-3)
##   "veces_min" / "veces_max":  cuántas noches juntos llevan. En "intimidad"
##                 y "despertar" ya cuenta la de esa noche (1 = la primera).
##   "citas_min":  número mínimo de citas
##   "dia_min":    día del juego mínimo
##   "slot":       0 mañana, 1 mediodía, 2 tarde, 3 noche
##   "flag":       un flag que debe estar activo
##   "evento":     un evento que ya debe haberse visto (ej. "roc_05")
##   "stats":      {"Mi stat": 3}  -> mínimos de tus modulo_stats
##
## Variables que tu escena puede leer:
##   escena_personaje  (id del personaje)
##   escena_lugar      (id del lugar)
##   escena_punto      (el punto del gancho)
## =============================================================================

define modulo_conexiones = [

    ## Ejemplo activo y sin contenido: un desayuno al despertar con cualquiera.
    ## Sirve para comprobar que el módulo funciona. Bórralo cuando quieras.
    {
        "personaje": "*",
        "escena": "mi_modulo_desayuno",
        "requisitos": {"punto": "despertar"},
    },

    ## Plantilla (descoméntala y cambia los valores):
    # {
    #     "personaje": "valeria",
    #     "escena": "mi_modulo_valeria_hostal",
    #     "requisitos": {"punto": "intimidad", "lugar": "hostal", "afecto": 60},
    # },

]
