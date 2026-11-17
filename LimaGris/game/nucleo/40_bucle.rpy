## =============================================================================
## LIMA GRIS - Bucle principal: el día a día
## =============================================================================

init -5 python:

    def descripcion_lugar():
        L = LUGARES[store.ubicacion]
        opciones = L["desc"]
        return opciones[(store.dia + store.slot) % len(opciones)]

    def _oscurecer(hexcol, f):
        hexcol = hexcol.lstrip("#")
        r, g, b = int(hexcol[0:2], 16), int(hexcol[2:4], 16), int(hexcol[4:6], 16)
        return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))

    def fondo_lugar(lid=None):
        if lid is None:
            lid = store.ubicacion
        base = LUGARES[lid]["color"] if lid in LUGARES else "#15171c"
        f = [1.0, 1.1, 0.9, 0.6][store.slot]
        return Solid(_oscurecer(base, min(f, 1.0)))

    def etiqueta_pj(pj):
        d = PJ[pj]
        r = R(pj)
        if not r["conocida"]:
            return "%s\n{size=-6}{color=#9aa0ab}Todavía no se conocen{/color}{/size}" % d["desconocida"]
        if not es_romance(pj):
            return "%s\n{size=-6}{color=#9aa0ab}%s{/color}{/size}" % (d["nombre"], d["rol"])
        extra = ESTADOS[r["estado"]]
        if r["tipo"] != "principal":
            extra += " · de paso"
        return "%s  {color=#e0a040}%s{/color}\n{size=-6}{color=#9aa0ab}%s · %s{/color}{/size}" % (d["nombre"], corazones(pj), d["rol"], extra)

    def etiqueta_contacto(pj):
        d = PJ[pj]
        r = R(pj)
        if not es_romance(pj):
            return "%s\n{size=-6}{color=#9aa0ab}%s{/color}{/size}" % (d["nombre"], d["rol"])
        return "%s  {color=#e0a040}%s{/color}\n{size=-6}{color=#9aa0ab}%s · %s{/color}{/size}" % (d["nombre"], corazones(pj), ESTADOS[r["estado"]], d["rol"])

    def etiqueta_lugar(lid):
        L = LUGARES[lid]
        abierto = lugar_abierto(lid)
        if lid == store.ubicacion:
            estado = "estás aquí"
        elif not abierto:
            estado = "cerrado ahora"
        else:
            c = costo_viaje(lid)
            estado = "gratis" if c == 0 else soles(c)
        n = len([p for p in gente_aqui(lid) if R(p)["conocida"]]) if abierto else 0
        gente = ("%d conocido%s" % (n, "" if n == 1 else "s")) if n else "nadie conocido"
        return "%s\n{size=-6}{color=#9aa0ab}%s · %s · %s{/color}{/size}" % (L["nombre"], L["zona"], estado, gente)

    def acciones_aqui():
        u = store.ubicacion
        s = store.slot
        lab = es_horario_laboral()
        a = []
        if u == "casa":
            a.append(("siesta", "Echarte una siesta (+30 energía)", s < 3))
            a.append(("series", "Ver series y descansar (+15 energía)", True))
            a.append(("ofertas", "Revisar ofertas de freelance en la laptop", True))
            if store.freelance:
                a.append(("freelance", "Trabajar en: %s (%d ses.)" % (store.freelance["titulo"], store.freelance["sesiones"]),
                          s in (1, 2, 3) and store.energia >= 25 and not lab))
            if flag("yes_app_pend") and not flag("yes_app_lista"):
                a.append(("app_yesenia", "Programar la app de repaso para Yesenia", s in (1, 2, 3) and store.energia >= 25 and not lab))
            if flag("kat_web_pend") and not flag("kat_web_lista"):
                a.append(("web_kathy", "Armar la web de maquillaje de Kathy", s in (1, 2, 3) and store.energia >= 25 and not lab))
            if flag("dan_tramite_pend") and not flag("dan_tramite_listo"):
                a.append(("tramite_dani", "Llenar con Dani los formularios de SUNEDU (videollamada)", s in (1, 2, 3) and store.energia >= 20 and not lab))
        elif u == "oficina":
            if lab:
                hecho = bool(store.trabajo_hoy[s])
                a.append(("trabajar", "Trabajar en tu sprint" + ("  (ya cumpliste)" if hecho else ""), not hecho and store.energia >= 5))
            if s == 1:
                a.append(("almorzar", "Almorzar un menú (S/ 14)", puede_pagar(14)))
            if s == 3:
                a.append(("horas_extra", "Quedarte haciendo horas extra", store.energia >= 15))
        elif u in ("tambo", "bodega", "tiendas"):
            a.append(("comprar", "Comprar algo", True))
        elif u == "mercado":
            a.append(("comprar", "Comprar algo", True))
            a.append(("desayuno", "Desayunar un pan con chicharrón y un jugo (S/ 12)", puede_pagar(12)))
        elif u == "gimnasio":
            if store.membresia_hasta < store.dia:
                a.append(("membresia", "Pagar la membresía (S/ 120 por 30 días)", puede_pagar(MEMBRESIA_GYM)))
            a.append(("entrenar", "Entrenar (−20 energía, +forma)", store.membresia_hasta >= store.dia and store.energia >= 20))
            a.append(("comprar", "Comprar una bebida", True))
        elif u == "parque":
            a.append(("correr", "Salir a correr (−15 energía, +forma)", store.energia >= 15))
            a.append(("pasear", "Sentarte a mirar los patos un rato", True))
        elif u == "malecon":
            a.append(("caminar", "Caminar por el malecón", True))
        elif u == "barranco":
            a.append(("barra", "Tomarte un chilcano en la barra (S/ 25)", puede_pagar(25)))
        elif u == "edificio":
            a.append(("azotea", "Subir a la azotea a despejarte", True))
        return a

    def avanzar():
        s = store.slot
        if es_horario_laboral(s) and not store.trabajo_hoy[s]:
            cambiar_desempeno(-5, "faltaste a la chamba")
            store.trabajo_hoy[s] = "x"
        if s >= 3:
            store.necesita_dormir = True
        else:
            store.slot = s + 1

    def proximos_pagos():
        res = []
        for d in range(store.dia, store.dia + 21):
            dm = dia_mes(d)
            if dm == 1:
                res.append("%s: alquiler del depa (%s)" % (texto_fecha(d), soles(ALQUILER)))
            if dm == 10:
                res.append("%s: luz, agua e internet (%s)" % (texto_fecha(d), soles(SERVICIOS)))
            if dm == 15 or es_fin_de_mes(d):
                res.append("%s: quincena (+%s)" % (texto_fecha(d), soles(SUELDO_QUINCENA)))
        return res[:6]

    def texto_rumores():
        nombres = {"oficina": "En la oficina", "edificio": "En el edificio", "tambo": "En el Tambo",
                   "gimnasio": "En el gimnasio", "barranco": "En Barranco", "barrio": "En el barrio"}
        res = []
        for k in ["oficina", "edificio", "tambo", "gimnasio", "barranco", "barrio"]:
            v = store.rumores.get(k, 0)
            if v >= 60:
                t = "todo el mundo habla de ti"
            elif v >= 30:
                t = "hay cuchicheos"
            elif v >= 10:
                t = "algún comentario suelto"
            else:
                t = "tranquilo"
            res.append("%s: %s (%d)" % (nombres[k], t, v))
        return res

    def nuevo_dia():
        """Cierra el día y abre el siguiente. Devuelve líneas de resumen."""
        res = []
        ## Cierre del día laboral
        if es_laborable():
            for s in (0, 2):
                if s >= store.slot and not store.trabajo_hoy[s]:
                    cambiar_desempeno(-5, "faltaste a la chamba")
                    store.trabajo_hoy[s] = "x"
            if store.trabajo_hoy[0] is True and store.trabajo_hoy[2] is True:
                cambiar_desempeno(2)
        gastar(GASTO_DIARIO, "comida y pasajes", silencioso=True)
        res.append("Gastos del día (comida, pasajes, cositas): %s." % soles(GASTO_DIARIO))

        store.dia += 1
        store.slot = 0
        store.energia = 75 if store.trasnoche else 100
        store.trasnoche = False
        store.trabajo_hoy = [False, False, False, False]
        store.ev_marca = None
        for k in list(store.rumores.keys()):
            store.rumores[k] = max(0, store.rumores[k] - 1)

        ## Citas a las que no fuiste
        for c in list(store.citas_agendadas):
            if c["dia"] < store.dia:
                store.citas_agendadas.remove(c)
                cambiar(c["pj"], afecto=-10, confianza=-10)
                res.append("Dejaste plantada a %s. No te lo va a olvidar tan rápido." % nom(c["pj"]))

        dm = dia_mes()
        if dm == 1:
            gastar(ALQUILER, "alquiler", silencioso=True)
            res.append("Hoy se paga el alquiler: %s." % soles(ALQUILER))
        if dm == 10:
            gastar(SERVICIOS, "luz, agua e internet", silencioso=True)
            res.append("Llegaron los recibos de luz, agua e internet: %s." % soles(SERVICIOS))
        if dm == 15 or es_fin_de_mes():
            ganar(SUELDO_QUINCENA, "quincena", silencioso=True)
            res.append("¡Cayó la quincena! +%s." % soles(SUELDO_QUINCENA))
            if es_fin_de_mes() and store.desempeno >= 70:
                ganar(BONO_DESEMPENO, "bono por desempeño", silencioso=True)
                res.append("Bono por buen desempeño: +%s." % soles(BONO_DESEMPENO))
        if store.membresia_hasta == store.dia - 1 and store.membresia_hasta > 0:
            res.append("Se venció tu membresía del gimnasio.")
        if store.freelance and store.dia > store.freelance["plazo"]:
            res.append("El cliente de '%s' se cansó de esperar y canceló el encargo." % store.freelance["titulo"])
            store.freelance = None
            store.rep_freelance = max(0, store.rep_freelance - 1)
        if store.dinero < 0:
            res.append("Estás en rojo: debes %s. Doña Gladys ya te miró feo." % soles(-store.dinero))
            subir_rumor("edificio", 3)
        if dow() == 6:
            poner_flag("llamada_norma")
        _revisar_rumores_diarios()
        return res


## ============================================================== HUB
label hub:
    $ asegurar_rel()
    scene expression fondo_lugar()
    show screen hud

    if necesita_dormir:
        call dormir
        jump hub

    ## 1. ¿Hay una cita agendada para este momento?
    $ cita_actual = cita_ahora()
    if cita_actual:
        call cita_agendada(cita_actual)
        jump hub

    ## 2. ¿Hay un evento de historia aquí y ahora?
    $ ev_id = buscar_evento()
    if ev_id:
        $ marcar_evento(ev_id)
        call expression evento_por_id(ev_id)["label"]
        jump hub

    ## 3. El jugador decide
    call screen hub
    $ r_hub = _return

    if r_hub[0] == "hablar":
        call hablar(r_hub[1])
    elif r_hub[0] == "accion":
        call expression "accion_" + r_hub[1]
    elif r_hub[0] == "mapa":
        call ir_mapa
    elif r_hub[0] == "contactos":
        call ver_contactos
    elif r_hub[0] == "agenda":
        call screen agenda
    elif r_hub[0] == "mochila":
        call screen mochila
    elif r_hub[0] == "esperar":
        $ avanzar()
    elif r_hub[0] == "dormir":
        $ necesita_dormir = True
    jump hub


label ir_mapa:
    call screen mapa
    if _return:
        call ir_a(_return)
    return

label ir_a(destino):
    $ costo = costo_viaje(destino)
    if costo:
        $ gastar(costo, "taxi" if slot == 3 else "pasaje")
    $ ubicacion = destino
    scene expression fondo_lugar()
    return

label ver_contactos:
    call screen contactos
    if _return:
        call ver_perfil(_return)
        jump ver_contactos
    return

label ver_perfil(pj):
    call screen perfil(pj)
    if _return == "invitar":
        $ nom_tmp = nom(pj)
        "Le escribes a [nom_tmp] por WhatsApp."
        call invitar_salir(pj)
    return


## ============================================================ DORMIR
label dormir:
    $ necesita_dormir = False
    if ubicacion != "casa":
        $ costo = costo_viaje("casa", 3)
        if costo:
            $ gastar(costo, "taxi a casa")
            "Pides un taxi por aplicativo. El chofer pone salsa de los noventa y maneja como si la Vía Expresa fuera suya."
        else:
            "Caminas de regreso a tu depa por la Arequipa, con las manos en los bolsillos."
        $ ubicacion = "casa"
    scene black
    $ frase_sueno = renpy.random.choice([
        "Te tiras a la cama. El techo tiene una mancha con forma de Sudamérica. Te duermes contándole los países.",
        "Pones el celular a cargar, la alarma a las seis y media, y te quedas dormido antes de soltarlo.",
        "Afuera un perro le ladra a un micro. Adentro, tú ya estás soñando con un deploy que no termina.",
        "Te lavas los dientes, revisas la puerta dos veces y apagas la luz. Lima suena lejos.",
    ])
    "[frase_sueno]"
    $ resumen = nuevo_dia()
    scene expression fondo_lugar()
    $ texto_resumen = "\n".join(["{b}" + texto_fecha() + "{/b}"] + resumen)
    centered "[texto_resumen]"
    if flag("llamada_norma"):
        $ quitar_flag("llamada_norma")
        call llamada_norma
    return


## =========================================================== ACCIONES
label accion_trabajar:
    $ texto_chamba = renpy.random.choice([
        "Te pones los audífonos y le metes al ticket CHQ-214: un servicio que devuelve saldos negativos cuando la cooperativa cierra caja.",
        "Daily de quince minutos que dura cuarenta. Después, dos horas de código limpio. Casi te sientes feliz.",
        "Revisas el pull request de Piero. Tiene más comentarios tuyos que líneas de código. Lo apruebas igual, por amor.",
        "Peleas con un contenedor que funciona en tu máquina y en ninguna otra. Al final era una variable de entorno. Siempre es una variable de entorno.",
        "Escribes pruebas para un módulo de 2014 sin documentación. Encuentras un comentario que dice: 'no tocar, no sé por qué funciona'.",
        "Reunión con el cliente de la cooperativa. Te piden 'algo como WhatsApp, pero para préstamos'. Asientes con cara de profesional.",
    ])
    "[texto_chamba]"
    $ trabajo_hoy[slot] = True
    $ cambiar_desempeno(2 if energia >= 40 else 1, "buena jornada" if energia >= 40 else "")
    $ cambiar_energia(-15)
    $ avanzar()
    return

label accion_almorzar:
    $ gastar(14, "menú")
    $ cambiar_energia(10)
    $ comensales = [p for p in gente_aqui() if R(p)["conocida"] and es_romance(p)]
    if comensales:
        $ pj_alm = renpy.random.choice(comensales)
        $ nom_tmp = nom(pj_alm)
        "Bajas al menú de la esquina: sopa de quinua, seco con frejoles y refresco de cebada. [nom_tmp] se sienta en tu mesa."
        $ cambiar(pj_alm, afecto=2, confianza=1)
        $ registrar_visita(pj_alm)
    else:
        "Bajas al menú de la esquina: sopa de quinua, seco con frejoles y refresco de cebada. Comes revisando el celular, como todo Lima."
    $ avanzar()
    return

label accion_horas_extra:
    "Te quedas cuando el piso ya está casi vacío. Solo se escuchan el aire acondicionado y tu teclado."
    $ cambiar_desempeno(3, "horas extra")
    $ cambiar_energia(-15)
    $ trasnoche = True
    $ avanzar()
    return

label accion_comprar:
    call screen tienda(ubicacion)
    return

label accion_desayuno:
    $ gastar(12, "desayuno")
    $ cambiar_energia(15)
    "La casera te sirve un pan con chicharrón con su camote y salsa criolla, y un jugo surtido 'con yapa'. Resucitas."
    return

label accion_membresia:
    $ gastar(MEMBRESIA_GYM, "membresía del gimnasio")
    $ membresia_hasta = dia + 30
    "El chico de recepción te toma una foto horrible para el carnet. 'Bienvenido a la familia Fuerza Lince, mi king.'"
    return

label accion_entrenar:
    $ cambiar_energia(-20)
    $ cambiar_forma(2)
    if ubic_pj("mila") == "gimnasio" and R("mila")["conocida"]:
        "Mila pasa a tu costado y te corrige la postura sin decir nada. Solo te empuja la espalda con dos dedos. Duele, pero bien."
        $ cambiar("mila", afecto=1)
    else:
        $ texto_gym = renpy.random.choice([
            "Pecho y tríceps. El reguetón no te deja pensar en el trabajo, y eso es justo lo que necesitabas.",
            "Piernas. Bajar la escalera mañana va a ser una experiencia religiosa.",
            "Espalda y un poco de cardio. El espejo y tú hacen las paces, más o menos.",
        ])
        "[texto_gym]"
    $ avanzar()
    return

label accion_correr:
    $ cambiar_energia(-15)
    $ cambiar_forma(1)
    "Das cinco vueltas al parque. En la tercera te pasa un señor de setenta años en buzo. Te lo tomas como motivación."
    $ avanzar()
    return

label accion_pasear:
    $ cambiar_energia(5)
    "Te sientas en una banca. Un pato te mira con desprecio. Le das la razón y te quedas un rato sin pensar en nada."
    $ avanzar()
    return

label accion_caminar:
    $ cambiar_energia(5)
    "Caminas por el malecón hasta el Parque del Amor y de regreso. El mar huele a sal y a algo que se fue."
    $ avanzar()
    return

label accion_barra:
    $ gastar(25, "chilcano")
    if ubic_pj("carla") == "barranco" and R("carla")["conocida"]:
        "Carla te sirve el chilcano con un guiño y te cuenta, entre pedido y pedido, el chisme de la mesa del fondo."
        $ cambiar("carla", afecto=2)
        $ registrar_visita("carla")
    else:
        "Te tomas un chilcano de maracuyá mirando a la gente. Alguien canta un vals desafinado en una mesa y nadie lo detiene."
    $ avanzar()
    return

label accion_azotea:
    $ cambiar_energia(5)
    "Subes a la azotea. Entre la ropa tendida se ve un pedazo del cerro San Cristóbal con su cruz encendida. Respiras."
    $ avanzar()
    return

label accion_siesta:
    $ cambiar_energia(30)
    "Te echas 'cinco minutitos'. Despiertas con la cara marcada por el cojín y la sensación de haber viajado en el tiempo."
    $ avanzar()
    return

label accion_series:
    $ cambiar_energia(15)
    "Ves dos capítulos de una serie coreana que te recomendaron en la oficina. Ahora tienes opiniones sobre un CEO ficticio."
    $ avanzar()
    return

label accion_ofertas:
    call screen ofertas_freelance(generar_ofertas())
    if _return:
        $ freelance = dict(_return)
        "Aceptas el encargo: [freelance[titulo]]. El cliente responde con tres audios de dos minutos cada uno."
    return

label accion_freelance:
    $ cambiar_energia(-25)
    $ freelance["sesiones"] -= 1
    if freelance["sesiones"] <= 0:
        "Terminas el encargo, lo subes, lo pruebas en el celular del cliente (que tiene la pantalla rota) y funciona."
        $ ganar(freelance["pago"], "freelance")
        $ rep_freelance += 1
        $ freelance_hechos += 1
        $ freelance = None
    else:
        "Le avanzas al encargo con un café al lado y lo-fi de fondo. Faltan [freelance[sesiones]] sesiones."
    $ trasnoche = (slot == 3)
    $ avanzar()
    return


## ============================================== LLAMADA DE LOS DOMINGOS
label llamada_norma:
    "Suena el celular. 'TÍA NORMA' en la pantalla."
    norma "¡Sobrino! ¿Estás vivo? Ya ni llamas a tu tía, ingrato."
    $ frase_norma = renpy.random.choice([
        "¿Y ya tienes enamorada? No me digas que sigues pensando en la Paola esa.",
        "Hice ají de gallina. Mucho ají de gallina. Demasiado. Tienes que venir.",
        "Tu mamá me dijo que en Arequipa estabas más gordito. Lima te está secando, hijito.",
        "¿Estás comiendo bien? No me mientas, que te conozco desde que usabas pañal.",
    ])
    norma "[frase_norma]"
    menu:
        "Ir a almorzar a Breña con la tía Norma":
            "Cruzas media Lima para comer el mejor ají de gallina del mundo. La tía te manda con tres táperes de regreso."
            $ cambiar_energia(10)
            $ agregar_item("chocolate_tienda", 1)
            norma "Y llévate este chocolatito para la chica que te guste. No me mires así."
            $ avanzar()
        "Decirle que hoy no puedes, pero que la quieres":
            norma "Ay, ya, ya. Pero la próxima vienes, ¿ah? Cuídate, sobrino."
    return
