## =============================================================================
## LIMA GRIS - Estado de la partida (todo lo que se guarda)
## =============================================================================
## Todo lo que se declara con 'default' entra en la partida guardada.
## =============================================================================

## --- Jugador
default nombre = "Renzo"
default dinero = 0.0
default energia = 100
default forma = 20                ## estado físico 0-100
default desempeno = 50            ## desempeño en Andina Data 0-100
default rep_freelance = 0

## --- Tiempo y lugar
default dia = 1
default slot = 0
default ubicacion = "casa"
default necesita_dormir = False
default trasnoche = False
default trabajo_hoy = [False, False, False, False]
default ev_marca = None           ## (dia, slot, lugar) del último evento automático
default presencias = {}         ## "dia-slot-pj" -> lugar (para eventos)

## --- Relaciones: se llena en iniciar_partida() y en asegurar_rel()
default rel = {}

## --- Rumores por círculo social (0-100)
default rumores = {"oficina": 0, "edificio": 0, "tambo": 0, "gimnasio": 0, "barranco": 0, "barrio": 0}
default chismes = []              ## [{"pj":..., "circulo":..., "testigo":..., "dia":...}]

## --- Inventario y compras
default inventario = {}
default membresia_hasta = 0       ## día hasta el que tienes gimnasio pagado

## --- Citas agendadas: [{"pj":..., "lugar":..., "dia":..., "slot":...}]
default citas_agendadas = []

## --- Freelance
default freelance = None          ## {"titulo", "sesiones", "pago", "plazo"}
default freelance_ofertas_dia = -1
default freelance_ofertas = []
default freelance_hechos = 0

## --- Historia
default eventos_vistos = []
default flags = []
default historial_gastos = []

## --- Variables que se pasan a las escenas del módulo externo
default escena_personaje = None
default escena_lugar = None
default escena_punto = None
