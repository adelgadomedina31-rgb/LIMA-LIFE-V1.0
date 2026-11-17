## =============================================================================
## LIMA GRIS - Intimidad: consentimiento, lugar y consecuencias
## =============================================================================
## Este juego NO contiene escenas explícitas. Cuando dos personajes adultos
## deciden pasar la noche juntos:
##   1. Se pregunta y ella responde con claridad (puede decir que no).
##   2. Se elige un lugar realista según dónde están y con quién.
##   3. Se busca una escena del módulo externo (game/modulos/...). Si no hay,
##      se hace un fundido a negro.
##   4. Se resuelven las consecuencias del lugar elegido y amanece.
## =============================================================================

init -5 python:

    def chance_humor(pj, origen):
        r = R(pj)
        c = 70 + (r["atraccion"] - 55) // 2 + r["estado"] * 5
        if origen == "cita":
            c += 10
        f = PJ[pj].get("humor_func")
        if f:
            c += f()
        return max(5, min(95, c))

    def texto_opcion_lugar(pj, lid, texto, costo):
        if costo > 0:
            t = "%s  (%s)" % (texto, soles(costo))
        else:
            t = texto
        return t


label intimidad(pj, origen="charla"):
    $ hr = R(pj)
    $ nom_i = nom(pj)
    "Le preguntas, sin rodeos pero con cuidado, si quiere que esta noche siga. Que si no, no pasa nada."
    if renpy.random.randint(1, 100) > chance_humor(pj, origen):
        $ di(pj, PJ[pj].get("intimidad_no", "Hoy no, ¿ya? Pero me gustó que me preguntaras así."))
        "Le dices que no hay apuro. Y lo dices en serio."
        $ cambiar(pj, confianza=2)
        return False
    $ di(pj, PJ[pj].get("intimidad_si", "Sí. Yo también quiero."))

label intimidad_elegir_lugar:
    "¿A dónde van?"
    $ ops_i = opciones_lugar_intimo(pj)
    $ menu_i = []
    python:
        for lid_i, txt_i, costo_i in ops_i:
            if puede_pagar(costo_i):
                menu_i.append((texto_opcion_lugar(pj, lid_i, txt_i, costo_i), (lid_i, costo_i)))
            else:
                menu_i.append((texto_opcion_lugar(pj, lid_i, txt_i, costo_i) + " (no te alcanza)", None))
        menu_i = [m for m in menu_i if m[1] is not None]
        menu_i.append(("Mejor lo dejamos para otro día", "cancelar"))
    $ eleccion_i = renpy.display_menu(menu_i)
    if eleccion_i == "cancelar":
        $ di(pj, "Okey. No pasa nada. Me gusta que no me apures.")
        $ cambiar(pj, confianza=2)
        return False
    $ lugar_i, costo_i = eleccion_i

    ## ¿Ella acepta ese lugar?
    $ pref_i = pref_lugar(pj, lugar_i)
    if lugar_i == "depa_ella":
        $ posible_i, motivo_i = casa_ella_posible(pj)
        if not posible_i:
            $ di(pj, PJ[pj].get("rechazo_casa", "A mi casa no se puede, de verdad. Otro sitio."))
            jump intimidad_elegir_lugar
    if pref_i < 0 or (pref_i == 0 and hr["atraccion"] < 80):
        $ rech_i = PJ[pj].get("rechazos", {}).get(lugar_i, "¿Ahí? No, ni loca. Elige otra cosa.")
        $ di(pj, rech_i)
        jump intimidad_elegir_lugar
    if pref_i >= 2:
        $ di(pj, PJ[pj].get("lugar_favorito", "Buena idea. Me encanta."))

    ## Pago y llegada
    if costo_i > 0:
        $ gastar(costo_i, "la noche: " + NOMBRE_LUGAR_INTIMO[lugar_i])
    call intimidad_llegada(pj, lugar_i)

    ## Escena (módulo externo) o fundido a negro
    $ escena_personaje = pj
    $ escena_lugar = lugar_i
    $ escena_punto = "intimidad"
    $ hr["noches"] += 1
    $ hr["ult_noche"] = dia
    $ esc_mod = modulo_buscar_escena(pj, "intimidad", lugar_i)
    if esc_mod:
        call expression esc_mod
    else:
        call fundido_negro
    $ cambiar(pj, afecto=4 + max(0, pref_i - 1) * 2, confianza=3, atraccion=2)

    ## Consecuencias según el lugar y amanecer
    call intimidad_consecuencias(pj, lugar_i)
    return True


## Llegada al lugar (texto corto según el sitio)
label intimidad_llegada(pj, lugar):
    if lugar == "depa_tuyo":
        "Suben las escaleras de Los Ficus de puntitas, aguantándose la risa en cada escalón que cruje."
    elif lugar == "depa_ella" and PJ[pj].get("vivienda") == "vecina":
        "Suben las escaleras de Los Ficus en silencio y ella abre su puerta con la llave ya lista en la mano, para no hacer ruido."
    elif lugar == "depa_ella":
        $ zona_i = PJ[pj].get("zona_casa", "Lince")
        "Toman un taxi hasta su casa en [zona_i]. En el asiento de atrás, ella te agarra la mano y no te la suelta."
    elif lugar == "hostal":
        "El hostal tiene un letrero de neón al que le falta una letra. El recepcionista ni levanta la vista del celular."
    elif lugar == "hotel":
        "El hotel tiene alfombra, música suave y vista al mar. Ella te mira como diciendo: 'te pasaste'."
    elif lugar == "oficina":
        "El piso nueve está a oscuras, salvo por la luz de emergencia y el brillo de los monitores en reposo."
    elif lugar == "azotea":
        "Suben a la azotea. Entre la ropa tendida y las macetas, la ciudad es solo un murmullo naranja."
    elif lugar == "callejon":
        "Se meten en un pasaje a la vuelta, entre una pared con grafitis y una buganvilla. Se escucha el bar a lo lejos."
    elif lugar == "carro":
        "Ella maneja hasta una calle tranquila cerca del malecón, apaga las luces y se ríe nerviosa."
    elif lugar == "almacen":
        "Ella baja la mitad de la luz del Tambo y te jala hacia el almacén, entre cajas de galletas y gaseosas."
    elif lugar == "vestidor":
        "El gimnasio ya cerró. Solo quedan las luces del pasillo y el olor a desinfectante."
    elif lugar == "trastienda":
        "La reja de la bodega ya está abajo. En la trastienda hay sacos de arroz, una radio apagada y mucho silencio."
    return


label fundido_negro:
    scene black with Dissolve(1.5)
    centered "{i}. . .{/i}"
    "Lo que pasa después queda entre ustedes dos."
    return


## ======================================================= CONSECUENCIAS
label intimidad_consecuencias(pj, lugar):
    $ hr = R(pj)
    $ circ_i = PJ[pj].get("circulo")
    $ dado = renpy.random.randint(1, 100)
    $ dormir_aqui = True

    if lugar == "depa_tuyo":
        $ riesgo = 60 if circ_i == "edificio" else 35
        if dado <= riesgo:
            "Al entrar, la puerta de la portería se entreabre. Doña Gladys, en bata y con ruleros, los mira por encima de los lentes."
            gladys "Buenas noches, joven. Buenas noches... señorita."
            "Mañana lo sabe todo el edificio. Y probablemente el Tambo."
            $ agregar_chisme(pj, "edificio", "gladys", n=12)
        if renpy.random.randint(1, 100) <= 25:
            "En algún momento, alguien golpea la pared desde el depa de al lado. Tres golpes secos. Se mueren de risa."
            $ subir_rumor("edificio", 5)

    elif lugar == "depa_ella":
        $ viv_i = PJ[pj].get("vivienda", "sola")
        if viv_i == "vecina":
            if dado <= 55:
                "En el pasillo, una puerta se abre dos centímetros y se cierra de golpe. No hace falta adivinar quién fue."
                $ agregar_chisme(pj, "edificio", "gladys", n=15)
        elif viv_i == "roomie":
            if dado <= 50:
                $ poner_flag("roomie_" + pj)
                "En la mañana, su roomie te encuentra en la cocina buscando el azúcar. Te mira de pies a cabeza, te sirve café y te hace un interrogatorio de veinte minutos."
                $ cambiar(pj, confianza=2)
        elif viv_i == "hermana":
            if dado <= 30:
                "Su hermana llega una hora antes de lo previsto. Se encuentran los tres en la sala en un silencio largo, larguísimo."
                "Al final, la hermana suspira: 'Por lo menos es ingeniero'. Y se va a dormir."
        elif viv_i == "prima":
            if dado <= 40:
                "A las seis de la mañana, la prima sale del baño con una toalla en la cabeza, te ve y dice: 'Buenos días, cuñado'. Ella quiere morirse."
                $ subir_rumor("tambo", 5)
        elif viv_i == "hija":
            "En la refrigeradora hay dibujos de una niña: un sol, una casa, una mamá con lentes. Ella te pide que salgas antes de las siete, antes de que traigan a su hija."
            $ cambiar_energia(-10)

    elif lugar == "hostal":
        if dado <= 10:
            "Al salir, un vecino del barrio los reconoce desde la vereda de enfrente. Levanta las cejas y sigue caminando."
            $ agregar_chisme(pj, "barrio", None, n=8)

    elif lugar == "hotel":
        "En la mañana piden desayuno a la habitación y ven el mar gris desde la ventana. Por un rato, Lima es otra ciudad."
        $ cambiar(pj, atraccion=2, aviso_=False)

    elif lugar == "oficina":
        $ riesgo = 25 if pj == "kathy" else 45
        if dado <= riesgo:
            "Se escuchan pasos en el pasillo. Una linterna. Don Eusebio, el vigilante de noche, hace su ronda."
            "No ve nada... o eso quieren creer. Pero las cámaras sí graban, y Don Eusebio conversa con todo el mundo."
            $ agregar_chisme(pj, "oficina", None, n=30)
            $ poner_flag("llamado_rrhh")
        else:
            "Nadie los ve. Bajan por la escalera de emergencia, conteniendo la risa como dos practicantes."
        $ trasnoche = True

    elif lugar == "azotea":
        if dado <= 40:
            "Cuando bajan, Doña Gladys está en el descanso de la escalera, 'regando las plantas' a medianoche."
            $ agregar_chisme(pj, "edificio", "gladys", n=20)
        $ trasnoche = True

    elif lugar == "callejon":
        if dado <= 35:
            "Una camioneta del Serenazgo dobla la esquina con la circulina prendida. Los alumbran con una linterna."
            "Sereno" "A ver, jóvenes, a sus casas, que esto no es un hotel. Avancen, avancen."
            "Se van caminando rápido, rojos como rocoto, mientras el sereno sacude la cabeza."
            $ subir_rumor("barranco", 10)
            if PJ[pj].get("atrevida", 0) >= 2:
                $ di(pj, "¡Qué roche! Pero igual... valió la pena.")
                $ cambiar(pj, atraccion=3)
            else:
                $ di(pj, "Nunca más. Nunca. Más. ¿Me oíste?")
                $ cambiar(pj, afecto=-3)
        $ testigos_i = [x for x in gente_aqui() if x != pj and R(x)["conocida"]]
        if testigos_i and renpy.random.randint(1, 100) <= 30:
            $ nom_t = nom(testigos_i[0])
            "Y al volver a la calle principal, te cruzas con [nom_t], que viene saliendo del bar."
            $ agregar_chisme(pj, PJ[testigos_i[0]].get("circulo") or "barranco", testigos_i[0], n=10)
        $ trasnoche = True

    elif lugar == "carro":
        if dado <= 25:
            "Unos golpecitos en la ventana. Un vigilante con chaleco reflectante: 'Acá no se puede estacionar, señora'. Ella prende el carro sin mirarlo."
        $ trasnoche = True

    elif lugar == "almacen":
        if dado <= 40:
            "La puerta del Tambo suena. Es el supervisor del distrito, que viene a hacer arqueo de caja sin avisar."
            "Ella sale del almacén acomodándose el polo, con una caja de galletas en la mano como coartada. Él no se lo cree."
            $ di(pj, "Me van a mandar un memorándum. Te mato. Bueno... no. Pero casi.")
            $ cambiar(pj, afecto=-6, confianza=-8)
            $ agregar_chisme(pj, "tambo", None, n=20)
        $ trasnoche = True

    elif lugar == "vestidor":
        if dado <= 40:
            "Se prende la luz del pasillo. Otro entrenador volvió por su mochila. Los ve. Los dos fingen buscar unas llaves."
            $ agregar_chisme(pj, "gimnasio", None, n=25)
            $ cambiar(pj, confianza=-8)
        $ trasnoche = True

    elif lugar == "trastienda":
        if dado <= 30:
            "Se escuchan pasos en la escalera que baja del segundo piso. '¿Mery? ¿Estás ahí, hija?'. Es Don Teo, en pijama."
            "Ella contesta que está contando el sencillo. Tú pasas la noche más larga de tu vida detrás de un saco de azúcar."
            $ agregar_chisme(pj, "barrio", "teofilo", n=15)
        $ trasnoche = True

    ## --- Amanece
    $ escena_punto = "despertar"
    $ esc_mod = modulo_buscar_escena(pj, "despertar", lugar)
    if esc_mod:
        call expression esc_mod

    if renpy.random.randint(1, 100) <= 50 or lugar in ("depa_tuyo", "hotel", "depa_ella"):
        $ di(pj, PJ[pj].get("despues", "Buenos días. ...No me mires así, tengo la cara de almohada."))

    $ ubicacion = "casa"
    $ resumen = nuevo_dia()
    scene expression fondo_lugar()
    $ texto_resumen = "\n".join(["{b}" + texto_fecha() + "{/b}"] + resumen)
    centered "[texto_resumen]"
    if lugar not in ("depa_tuyo", "azotea"):
        "Pasas por tu depa a bañarte y cambiarte antes de empezar el día."
        $ cambiar_energia(-5)
    if flag("llamada_norma"):
        $ quitar_flag("llamada_norma")
        call llamada_norma
    $ necesita_dormir = False
    return
