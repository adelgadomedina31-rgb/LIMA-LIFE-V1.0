## =============================================================================
## MI MÓDULO - Variables
## =============================================================================
## Este archivo es tuyo. El juego base lo lee, pero no lo modifica.
##
## modulo_stats guarda tus estadísticas por personaje. La pantalla de perfil
## de cada personaje muestra AUTOMÁTICAMENTE lo que pongas aquí, en una
## sección llamada "Módulo".
##
## Formato:
##   modulo_stats = {
##       "valeria": {"Nombre de la estadística": 3, "Otra": 10},
##       "kathy":   {"Nombre de la estadística": 1},
##   }
##
## Ids de personajes: valeria, kathy, mariela, fiorella, jimena, brenda,
## yesenia, dani, mery, rocio, andrea, lucia, mila, camila, sofia, carla, paola
## (y "jugador" si quieres guardar algo tuyo).
## =============================================================================

default modulo_stats = {}

init python:

    def sumar_stat(personaje, stat, cantidad=1):
        """Suma 'cantidad' a la estadística 'stat' del personaje.
        Úsala en tus escenas:  $ sumar_stat(escena_personaje, "Mi stat", 1)
        """
        if personaje not in modulo_stats:
            modulo_stats[personaje] = {}
        modulo_stats[personaje][stat] = modulo_stats[personaje].get(stat, 0) + cantidad

    def leer_stat(personaje, stat):
        """Devuelve el valor de una estadística (0 si no existe)."""
        return modulo_stats.get(personaje, {}).get(stat, 0)
