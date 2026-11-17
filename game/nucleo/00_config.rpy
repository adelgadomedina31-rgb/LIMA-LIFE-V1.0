## =============================================================================
## LIMA GRIS - Configuración general (datos que no cambian durante la partida)
## =============================================================================
## Aquí están el calendario, los lugares, la tienda, las citas y el freelance.
## Si quieres agregar un lugar, un regalo o un tipo de cita, este es el archivo.
## =============================================================================

init -20 python:

    import random

    ## ---------------------------------------------------------------- Tiempo
    SLOTS = ["Mañana", "Mediodía", "Tarde", "Noche"]
    SLOT_HORA = ["08:00", "13:00", "16:30", "20:30"]
    DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    MESES = [
        ("enero", 31), ("febrero", 28), ("marzo", 31), ("abril", 30),
        ("mayo", 31), ("junio", 30), ("julio", 31), ("agosto", 31),
        ("septiembre", 30), ("octubre", 31), ("noviembre", 30), ("diciembre", 31),
    ]
    ## El día 1 del juego es lunes 2 de marzo.
    MES_INICIO = 2
    DIA_MES_INICIO = 2

    ## -------------------------------------------------------------- Economía
    SUELDO_QUINCENA = 2400.0
    BONO_DESEMPENO = 300.0
    ALQUILER = 1100.0
    SERVICIOS = 160.0          ## luz, agua e internet, el día 10
    GASTO_DIARIO = 25.0        ## comida, pasajes y gastos chicos
    MEMBRESIA_GYM = 120.0
    DINERO_INICIAL = 1450.0

    ## Zonas: costo aproximado de ir en micro (de día) o en taxi por app (de noche)
    ZONAS = {
        "Lince":      {"micro": 0.0, "taxi": 0.0},
        "San Isidro": {"micro": 2.5, "taxi": 12.0},
        "Miraflores": {"micro": 3.0, "taxi": 18.0},
        "Barranco":   {"micro": 3.5, "taxi": 22.0},
        ## Zonas donde viven algunos personajes (solo para ir a su casa)
        "Pueblo Libre": {"micro": 2.5, "taxi": 12.0},
        "Jesús María": {"micro": 2.0, "taxi": 9.0},
        "San Borja": {"micro": 3.0, "taxi": 16.0},
        "Los Olivos": {"micro": 3.5, "taxi": 28.0},
        "San Juan de Lurigancho": {"micro": 4.0, "taxi": 35.0},
    }

    ## --------------------------------------------------------------- Lugares
    ## abierto: lista de franjas (0 mañana, 1 mediodía, 2 tarde, 3 noche)
    ## dias: días de la semana en que abre (0 lunes ... 6 domingo)
    LUGARES = {
        "casa": dict(
            nombre="Tu depa", zona="Lince", abierto=[0, 1, 2, 3], dias=list(range(7)),
            color="#1b2130",
            desc=[
                "Un minidepartamento en el cuarto piso: sala-comedor, un cuarto y una ventana que da a la Av. Arequipa.",
                "Huele a café recalentado. La laptop te mira desde la mesa como si te debiera plata.",
                "El ruido de los micros sube hasta la ventana. Ya ni lo notas.",
            ],
        ),
        "edificio": dict(
            nombre="Edificio Los Ficus", zona="Lince", abierto=[0, 1, 2, 3], dias=list(range(7)),
            color="#20261f",
            desc=[
                "Pasillos con olor a cera, una escalera que cruje y una azotea con cordeles de ropa y macetas.",
                "En la puerta, el periódico de Doña Gladys y su radio con la novela de la tarde.",
                "Alguien está friendo algo en el segundo piso. Huele a gloria.",
            ],
        ),
        "oficina": dict(
            nombre="Andina Data", zona="San Isidro", abierto=[0, 1, 2], dias=[0, 1, 2, 3, 4],
            color="#1a2228", circulo="oficina",
            desc=[
                "Piso 9 de un edificio de vidrio en San Isidro. Open space, pizarras llenas de flechas y una máquina de café que nunca funciona del todo.",
                "Se escucha el teclado de todos a la vez, como lluvia que en Lima nunca cae.",
                "En la pizarra grande alguien escribió: PROYECTO CHASQUI - FALTAN 40 DÍAS.",
            ],
        ),
        "tambo": dict(
            nombre="El Tambo de la esquina", zona="Lince", abierto=[0, 1, 2, 3], dias=list(range(7)),
            color="#2a1f22", circulo="tambo",
            desc=[
                "Luz blanca, refrigeradoras zumbando y la promoción de dos chelas que nunca termina.",
                "La cola llega hasta los panetones que nadie compra en marzo.",
                "En la caja suena una cumbia bajito, casi en secreto.",
            ],
        ),
        "bodega": dict(
            nombre="Bodega Don Teo", zona="Lince", abierto=[0, 1, 2, 3], dias=list(range(7)),
            color="#2a2418", circulo="barrio",
            desc=[
                "Una bodega de barrio de las de antes: reja, mostrador de madera y una radio con noticias.",
                "Hay panes en una canasta, sacos de arroz y un letrero escrito a mano: HOY NO SE FÍA, MAÑANA SÍ.",
            ],
        ),
        "gimnasio": dict(
            nombre="Gimnasio Fuerza Lince", zona="Lince", abierto=[0, 2, 3], dias=list(range(7)),
            color="#1f2226", circulo="gimnasio",
            desc=[
                "Pesas que suenan, reguetón a todo volumen y un espejo enorme que no perdona.",
                "Un letrero dice: 'EL DOLOR ES TEMPORAL, LA MEMBRESÍA ES MENSUAL'.",
            ],
        ),
        "parque": dict(
            nombre="Parque de Lince", zona="Lince", abierto=[0, 1, 2], dias=list(range(7)),
            color="#1c2a1f",
            desc=[
                "Árboles viejos, una laguna con patos y señores jugando ajedrez en las bancas.",
                "Huele a pasto mojado por el regador. Pasa un heladero tocando su corneta.",
            ],
        ),
        "mercado": dict(
            nombre="Mercado de Lince", zona="Lince", abierto=[0, 1], dias=list(range(7)),
            color="#2b2618",
            desc=[
                "Puestos de fruta, juguerías y casera gritando ofertas: '¡Lleve, lleve, caserito!'",
                "El olor a culantro y a pescado fresco te despierta más que el café.",
            ],
        ),
        "tiendas": dict(
            nombre="Tiendas de la Av. Arequipa", zona="Lince", abierto=[1, 2, 3], dias=list(range(7)),
            color="#241f2b",
            desc=[
                "Una florería, una chocolatería, una licorería y la Librería El Zorro, todas en la misma cuadra.",
                "Vitrinas iluminadas y gente apurada saliendo del trabajo.",
            ],
        ),
        "malecon": dict(
            nombre="Malecón de Miraflores", zona="Miraflores", abierto=[0, 2, 3], dias=list(range(7)),
            color="#1a2433",
            desc=[
                "El acantilado, el mar gris y los parapentes flotando como cometas grandes.",
                "Corredores, perros con chompa y parejas sentadas mirando un sol que casi nunca sale.",
            ],
        ),
        "barranco": dict(
            nombre="Bar La Garúa (Barranco)", zona="Barranco", abierto=[3], dias=list(range(7)),
            color="#2a1b1b", circulo="barranco",
            desc=[
                "Una casona antigua convertida en bar: piso de madera, foquitos amarillos y una barra larga.",
                "Suena un vals criollo remezclado. Huele a pisco y a limón.",
            ],
        ),
    }

    ## Orden en que se muestran en el mapa
    ORDEN_LUGARES = ["casa", "edificio", "tambo", "bodega", "gimnasio", "parque",
                     "mercado", "tiendas", "oficina", "malecon", "barranco"]

    ## ---------------------------------------------------------- Objetos
    ## cat: categoría de regalo (flores, chocolates, vino, pisco, cerveza, libros)
    ##      o "consumo" para cosas que usas tú.
    ## tiendas: lugares donde se vende.
    ITEMS = {
        "girasoles":        dict(nombre="Ramo de girasoles", cat="flores", precio=35.0, tiendas=["tiendas", "mercado"]),
        "rosas":            dict(nombre="Ramo de rosas", cat="flores", precio=45.0, tiendas=["tiendas"]),
        "orquidea":         dict(nombre="Orquídea en maceta", cat="flores", precio=75.0, tiendas=["tiendas"]),
        "chocolate_tienda": dict(nombre="Chocolate de tienda", cat="chocolates", precio=6.0, tiendas=["tambo", "bodega"]),
        "chocolate_cusco":  dict(nombre="Chocolate artesanal de Cusco", cat="chocolates", precio=28.0, tiendas=["tiendas"]),
        "bombones":         dict(nombre="Caja de bombones finos", cat="chocolates", precio=58.0, tiendas=["tiendas"]),
        "vino_ica":         dict(nombre="Vino tinto de Ica", cat="vino", precio=38.0, tiendas=["tiendas", "tambo"]),
        "vino_importado":   dict(nombre="Vino tinto importado", cat="vino", precio=89.0, tiendas=["tiendas"]),
        "pisco_quebranta":  dict(nombre="Pisco quebranta", cat="pisco", precio=45.0, tiendas=["tiendas", "bodega"]),
        "pisco_acholado":   dict(nombre="Pisco acholado premium", cat="pisco", precio=95.0, tiendas=["tiendas"]),
        "six_pack":         dict(nombre="Six-pack de cerveza", cat="cerveza", precio=30.0, tiendas=["tambo", "bodega", "tiendas"]),
        "cerveza_artesanal":dict(nombre="Pack de cervezas artesanales", cat="cerveza", precio=48.0, tiendas=["tiendas"]),
        "novela":           dict(nombre="Novela de autor peruano", cat="libros", precio=55.0, tiendas=["tiendas"]),
        "poemario":         dict(nombre="Poemario", cat="libros", precio=39.0, tiendas=["tiendas"]),
        "libro_cocina":     dict(nombre="Libro de cocina peruana", cat="libros", precio=79.0, tiendas=["tiendas"]),
        "cafe":             dict(nombre="Café para llevar", cat="consumo", precio=6.0, tiendas=["tambo"], energia=12),
        "jugo":             dict(nombre="Jugo surtido", cat="consumo", precio=8.0, tiendas=["mercado"], energia=15),
        "rehidratante":     dict(nombre="Bebida rehidratante", cat="consumo", precio=5.0, tiendas=["tambo", "bodega", "gimnasio"], energia=8),
    }

    CATEGORIAS_REGALO = ["flores", "chocolates", "vino", "pisco", "cerveza", "libros"]
    NOMBRE_CATEGORIA = {
        "flores": "Flores", "chocolates": "Chocolates", "vino": "Vino", "pisco": "Pisco",
        "cerveza": "Cerveza", "libros": "Libros",
    }

    ## ------------------------------------------------------------- Citas
    ## lugar: ubicación del mapa donde ocurre (para saber quién te puede ver)
    CITAS = {
        "cafe":       dict(nombre="Un café en San Isidro", costo=35.0, slots=[1, 2], zona="San Isidro", lugar=None,
                           intro="Un café chiquito con mesas en la vereda. El barista te pregunta si quieres 'el filtrado del día' como si fuera un secreto."),
        "cevicheria": dict(nombre="Almuerzo en El Muelle de Lucía (Lince)", costo=90.0, slots=[1], zona="Lince", lugar="cevicheria",
                           intro="Una cevichería de barrio con manteles a cuadros. Llega la leche de tigre de cortesía y la conversación se ablanda solita."),
        "cine":       dict(nombre="Cine en San Isidro", costo=55.0, slots=[2, 3], zona="San Isidro", lugar=None,
                           intro="Canchita salada y dulce, mitad y mitad. La película es lo de menos."),
        "malecon":    dict(nombre="Paseo por el malecón de Miraflores", costo=15.0, slots=[2, 3], zona="Miraflores", lugar="malecon",
                           intro="Caminan junto al acantilado con un helado en la mano. Abajo, el mar hace su ruido de siempre."),
        "cena":       dict(nombre="Cena en Miraflores", costo=180.0, slots=[3], zona="Miraflores", lugar=None,
                           intro="Un restaurante con luz baja y carta de fusión. El mozo recomienda el pulpo al olivo con una seriedad conmovedora."),
        "bar":        dict(nombre="Tragos en La Garúa (Barranco)", costo=120.0, slots=[3], zona="Barranco", lugar="barranco",
                           intro="La Garúa está llena. Consiguen dos bancos en la barra y piden chilcanos."),
    }
    ORDEN_CITAS = ["cafe", "cevicheria", "cine", "malecon", "cena", "bar"]

    ## Temas de conversación en las citas
    TEMAS = {
        "trabajo":  "Hablar de la chamba",
        "suenos":   "Preguntarle por sus sueños",
        "familia":  "Hablar de la familia",
        "humor":    "Contarle una anécdota graciosa",
        "coqueteo": "Coquetearle",
        "lima":     "Quejarse del tráfico de Lima",
    }

    ## ---------------------------------------------------------- Freelance
    ## (título, sesiones de trabajo, pago en soles)
    FREELANCE_OFERTAS = [
        ("Landing page para una pollería en Los Olivos", 2, 280.0),
        ("Arreglar el WordPress hackeado de una ferretería", 1, 150.0),
        ("Script en Python para cuadrar planillas de un contador", 2, 320.0),
        ("App de reservas para una barbería en Surco", 4, 900.0),
        ("Migrar una base de datos de Access a PostgreSQL", 3, 650.0),
        ("Bot de WhatsApp para pedidos de una juguería", 3, 520.0),
        ("Dashboard de ventas para una distribuidora de abarrotes", 4, 850.0),
        ("Formulario web para una ONG de Villa El Salvador", 1, 120.0),
        ("Tienda online para una marca de chompas de alpaca", 4, 950.0),
        ("Corregir reportes en Excel con macros de una constructora", 2, 300.0),
        ("Sistema de inventario para un minimarket en Comas", 3, 600.0),
        ("Página web para un consultorio dental en Jesús María", 2, 340.0),
    ]

    ## ------------------------------------------------- Estados de relación
    ESTADOS = ["Conocida", "Amiga", "Saliendo", "Pareja"]

    ## Umbrales generales
    UMBRAL_PRINCIPAL_VISITAS = 5
    UMBRAL_PRINCIPAL_AFECTO = 18
    UMBRAL_NUMERO = 15            ## confianza para tener su WhatsApp
    UMBRAL_HORARIO = 3            ## visitas para conocer su horario
