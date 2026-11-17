## =============================================================================
## MI MÓDULO - Escenas
## =============================================================================
## Pon aquí tus escenas como labels de Ren'Py. Puedes crear todos los archivos
## .rpy que quieras dentro de esta carpeta.
##
## Reglas:
##   - Cada escena es un label y termina con 'return'.
##   - Usa los personajes del juego: va (Valeria), ka (Kathy), ma (Mariela),
##     ye (Yesenia), da (Dani), ro (Rocío), fi, ji, br, an, lu, mi, ca, me, so,
##     cr, pa, y p para el protagonista.
##   - O, si es genérica, usa:  $ di(escena_personaje, "texto")
##   - Para sumar estadísticas:  $ sumar_stat(escena_personaje, "Nombre", 1)
##   - No cambies 'dia', 'slot' ni 'ubicacion' aquí: el juego se encarga.
## =============================================================================

label mi_modulo_desayuno:
    $ nom_mod = nom(escena_personaje)
    "Desayunan juntos: pan, palta y café. [nom_mod] te roba la mitad de tu pan sin pedir permiso."
    $ sumar_stat(escena_personaje, "Desayunos juntos", 1)
    return


## Plantilla vacía para una escena de intimidad (escribe tu propio contenido):
# label mi_modulo_valeria_hostal:
#     scene black with dissolve
#     "..."
#     $ sumar_stat("valeria", "Mi estadística", 1)
#     return
