## =============================================================================
## LIMA GRIS - Hablar con la gente
## =============================================================================
## Las líneas de cada personaje están en personajes/datos.rpy.
## Formato de una línea: "c|texto" (habla ella), "p|texto" (hablas tú),
## "n|texto" (narración) o "<id>|texto" (habla otro personaje, ej. "piero|...").
## =============================================================================

init -5 python:

    def partir_linea(l):
        if "|" in l:
            q, t = l.split("|", 1)
            return q.strip(), t
        return "n", l

    def di(pj, texto):
        """Dice una sola línea. Si no tiene prefijo 'x|', la dice el personaje."""
        if "|" in texto:
            q, t = partir_linea(texto)
        else:
            q, t = "c", texto
        renpy.say(quien(q, pj), t)

    def quien(q, pj):
        if q == "c":
            return ch(pj)
        if q == "p":
            return store.p
        if q == "n":
            return store.narrator
        if q in PJ:
            return ch(q)
        return store.narrator

    def siguiente_confidencia(pj):
        r = R(pj)
        lista = PJ[pj].get("confidencias", [])
        i = r["confidencias"]
        if i < len(lista) and r["confianza"] >= lista[i][0]:
            return i
        return None

    def puede_declarar(pj):
        r = R(pj)
        return (es_romance(pj) and not PJ[pj].get("ruta") and es_principal(pj) and r["estado"] == 1
                and r["afecto"] >= 50 and r["confianza"] >= 40 and r["citas"] >= 2)

    def puede_pareja_generica(pj):
        r = R(pj)
        return (es_romance(pj) and not PJ[pj].get("ruta") and r["estado"] == 2
                and r["afecto"] >= 80 and r["confianza"] >= 70 and r["citas"] >= 5)

    FRASES_COQUETEO = [
        "Le dices que con esa sonrisa deberían cobrarle impuesto a la renta.",
        "Le comentas, como quien no quiere la cosa, que hoy se ve especialmente bien.",
        "Le preguntas si siempre fue así de bacán o si es algo que practica.",
        "Le dices que eres ingeniero y que acabas de detectar un error: ella todavía no tiene tu número favorito... el de ella.",
        "Le sostienes la mirada un segundo más de lo normal y sonríes.",
    ]


## Dice una lista de líneas con el formato "q|texto"
label decir(pj, lineas):
    $ di_i = 0
    while di_i < len(lineas):
        $ di_q, di_t = partir_linea(lineas[di_i])
        $ renpy.say(quien(di_q, pj), di_t)
        $ di_i += 1
    return


## ============================================================ HABLAR
label hablar(pj):
    if not es_romance(pj):
        call hablar_npc(pj)
        return

    if not R(pj)["conocida"]:
        call decir(pj, PJ[pj]["presentacion"])
        $ R(pj)["conocida"] = True
        $ registrar_visita(pj)
        $ cambiar(pj, afecto=2, aviso_=False)
        return

    $ idx_chisme = chisme_para(pj)
    if idx_chisme is not None:
        call confrontacion(pj, idx_chisme)
        return

    $ registrar_visita(pj)
    $ saludo_tmp = PJ[pj]["saludo"][R(pj)["estado"] if R(pj)["estado"] < len(PJ[pj]["saludo"]) else -1]
    call decir(pj, [saludo_tmp])
    call hablar_menu(pj)
    return


label hablar_menu(pj):
label hablar_menu_bucle:
    $ hr = R(pj)
    menu:
        "Conversar" if hr["ult_charla"] != dia:
            call charla(pj)
        "Preguntarle por su vida" if siguiente_confidencia(pj) is not None and hr["ult_confidencia"] != dia:
            call confidencia(pj)
        "Coquetearle" if hr["afecto"] >= 15 and hr["ult_coqueteo"] != dia:
            call coquetear(pj)
        "Darle un regalo" if regalos_en_mochila() and hr["ult_regalo"] != dia:
            call regalar(pj)
        "Invitarla a salir" if puede_invitar(pj):
            call invitar_salir(pj)
            if _return == "fin":
                return
        "Pedirle que salgan en serio" if puede_declarar(pj):
            call declaracion(pj)
        "Proponerle que sean pareja" if puede_pareja_generica(pj):
            call pareja_generica(pj)
        "Proponerle que la noche siga juntos" if slot == 3 and puede_intimidad(pj):
            call intimidad(pj, "charla")
            if _return:
                return
        "Ver su perfil":
            call screen perfil(pj)
            if _return == "invitar":
                call invitar_salir(pj)
                if _return == "fin":
                    return
        "Despedirte":
            $ despedida_tmp = renpy.random.choice(PJ[pj].get("despedida", ["c|Ya, nos vemos."]))
            call decir(pj, [despedida_tmp])
            return
    jump hablar_menu_bucle


## ============================================================ CHARLA
label charla(pj):
    $ hr = R(pj)
    $ hr["ult_charla"] = dia
    $ pool = PJ[pj]["charla_cerca"] if (hr["estado"] >= 2 and PJ[pj].get("charla_cerca")) else PJ[pj]["charla"]
    $ lineas_tmp = pool[hr["charla_idx"] % len(pool)]
    $ hr["charla_idx"] += 1
    call decir(pj, lineas_tmp)
    $ cambiar(pj, afecto=(3 if hr["estado"] >= 2 else 2), confianza=1)
    return


## ======================================================= CONFIDENCIA
label confidencia(pj):
    $ hr = R(pj)
    $ i_conf = siguiente_confidencia(pj)
    $ hr["ult_confidencia"] = dia
    "Le preguntas por ella. No por la chamba ni por el clima: por ella."
    call decir(pj, PJ[pj]["confidencias"][i_conf][2])
    $ hr["confidencias"] = i_conf + 1
    $ cambiar(pj, afecto=2, confianza=3)
    return


## ========================================================= COQUETEAR
label coquetear(pj):
    $ hr = R(pj)
    $ hr["ult_coqueteo"] = dia
    $ frase_tmp = renpy.random.choice(FRASES_COQUETEO)
    "[frase_tmp]"
    $ chance = 40 + hr["atraccion"] // 2 + forma // 10 + hr["estado"] * 10
    if ubicacion == "oficina" and es_horario_laboral():
        $ chance -= 10
    if renpy.random.randint(1, 100) <= chance:
        $ resp_tmp = renpy.random.choice(PJ[pj]["coqueteo_bien"])
        call decir(pj, [resp_tmp])
        $ cambiar(pj, afecto=1, atraccion=renpy.random.randint(3, 5))
    else:
        $ resp_tmp = renpy.random.choice(PJ[pj]["coqueteo_mal"])
        call decir(pj, [resp_tmp])
        $ cambiar(pj, afecto=-2)
    $ otros = [x for x in gente_aqui() if x != pj and R(x)["conocida"]]
    if otros and LUGARES[ubicacion].get("circulo"):
        $ subir_rumor(LUGARES[ubicacion]["circulo"], 3)
        $ nom_tmp = nom(otros[0])
        "Por el rabillo del ojo ves que [nom_tmp] se ha dado cuenta."
    return


## ============================================================ REGALAR
label regalar(pj):
    call screen elegir_regalo(pj)
    if not _return:
        return
    $ item_tmp = _return
    $ hr = R(pj)
    $ hr["ult_regalo"] = dia
    $ quitar_item(item_tmp)
    $ cat_tmp = ITEMS[item_tmp]["cat"]
    $ g_tmp = PJ[pj].get("gustos", {}).get(cat_tmp, 0)
    $ nom_item = ITEMS[item_tmp]["nombre"].lower()
    "Le das: [nom_item]."
    call decir(pj, [PJ[pj]["regalo"][g_tmp]])
    if cat_tmp not in hr["gustos_vistos"]:
        $ hr["gustos_vistos"].append(cat_tmp)
    $ caro = 2 if ITEMS[item_tmp]["precio"] >= 55 else 0
    if g_tmp == 2:
        $ cambiar(pj, afecto=6 + caro, confianza=2, atraccion=2)
    elif g_tmp == 1:
        $ cambiar(pj, afecto=3 + caro // 2, confianza=1, atraccion=1)
    elif g_tmp == 0:
        $ cambiar(pj, afecto=1)
    else:
        $ cambiar(pj, afecto=-3, atraccion=-1)
    if item_tmp == PJ[pj].get("favorito"):
        "Se le ilumina la cara. Le atinaste de lleno."
        $ cambiar(pj, afecto=4, confianza=2)
    if ubicacion == "oficina" and len(gente_aqui()) > 2:
        $ subir_rumor("oficina", 4)
        "Detrás de ti, alguien carraspea. En Andina Data, un regalo en público es noticia."
    return


## ======================================================= DECLARACIÓN
label declaracion(pj):
    "Respiras hondo. Le dices que te gusta pasar tiempo con ella, que no es solo amistad, y le preguntas si quiere que salgan en serio."
    $ hr = R(pj)
    if hr["atraccion"] >= 45:
        call decir(pj, PJ[pj].get("si_salir", ["c|...Sí. Yo también lo estaba pensando."]))
        $ poner_estado(pj, 2)
        $ cambiar(pj, afecto=5, confianza=5, atraccion=3)
    else:
        call decir(pj, PJ[pj].get("no_salir", ["c|Me caes muy bien... pero todavía no lo siento así. ¿Me das tiempo?"]))
        $ cambiar(pj, confianza=2)
    return


label pareja_generica(pj):
    "Le dices que quieres algo más formal: ser su pareja, presentarte con su gente, hacer planes."
    call decir(pj, PJ[pj].get("si_pareja", ["c|Pensé que nunca me lo ibas a pedir. Sí."]))
    $ poner_estado(pj, 3)
    $ cambiar(pj, afecto=8, confianza=8)
    return


## ======================================================== CONFRONTACIÓN
## Cuando alguien con quien sales se entera de que te vieron con otra persona.
label confrontacion(pj, idx):
    $ hr = R(pj)
    $ hr["chisme_idx"] = idx + 1
    $ otra_tmp = nom(chismes[idx]["pj"])
    $ testigo_tmp = chismes[idx].get("testigo")
    $ fuente_tmp = ("Me lo contó " + nom(testigo_tmp) + ".") if (testigo_tmp and testigo_tmp != pj and testigo_tmp in PJ) else "Ya sabes cómo es la gente."
    "Apenas te ve, sabes que algo pasa. No sonríe."
    $ di(pj, "Oye. Tenemos que hablar. Me dijeron que te vieron con " + otra_tmp + ". " + fuente_tmp)
    menu:
        "Decirle la verdad":
            if hr["estado"] >= 3:
                $ di(pj, "Por lo menos no me mientes. Pero me duele, ¿sabes? Pensé que estábamos en la misma.")
                $ cambiar(pj, afecto=-12, confianza=-5)
                menu:
                    "Pedirle perdón y prometer que no va a pasar otra vez":
                        $ di(pj, "Las promesas las cumples o no las haces. Voy a ver qué haces, no qué dices.")
                        $ cambiar(pj, confianza=3)
                    "Decirle que necesitas espacio":
                        $ di(pj, "Ya. Entonces tómatelo. Pero no esperes que yo me quede igual.")
                        $ poner_estado(pj, 2)
            else:
                $ di(pj, "No habíamos dicho que fuéramos exclusivos... pero igual quiero saber dónde estoy parada.")
                $ cambiar(pj, afecto=-4, confianza=3)
                menu:
                    "Proponerle que solo salgan entre ustedes dos":
                        $ di(pj, "...Ya. Me gusta cómo suena eso. Pero va en serio, ¿ah?")
                        $ cambiar(pj, afecto=4, confianza=4)
                        $ poner_flag("exclusivo_" + pj)
                    "Decirle que por ahora prefieres no amarrarte":
                        $ di(pj, "Okey. Al menos eres honesto. Yo también voy a hacer mi vida, entonces.")
                        $ cambiar(pj, afecto=-6)
        "Negarlo todo":
            if renpy.random.randint(1, 100) <= hr["confianza"] - 10:
                $ di(pj, "...Ya. Te creo. Pero que no me lo vuelvan a contar.")
                $ cambiar(pj, afecto=-2)
            else:
                $ di(pj, "No me mientas en la cara. Eso sí que no.")
                $ cambiar(pj, afecto=-10, confianza=-20)
                if hr["estado"] >= 3:
                    $ poner_estado(pj, 2)
    return


## =============================================================== NPC
label hablar_npc(pj):
    if not R(pj)["conocida"]:
        call decir(pj, PJ[pj]["presentacion"])
        $ R(pj)["conocida"] = True
        return
    $ hr = R(pj)
    if hr["ult_charla"] == dia:
        $ di(pj, renpy.random.choice(PJ[pj]["ocupado_txt"]))
        return
    $ hr["ult_charla"] = dia
    $ lineas_tmp = PJ[pj]["charla"][hr["charla_idx"] % len(PJ[pj]["charla"])]
    $ hr["charla_idx"] += 1
    call decir(pj, lineas_tmp)
    ## Pista sobre la rutina de alguien
    $ pistas_tmp = [x for x in PJ[pj].get("pistas", []) if not R(x)["horario"]]
    if pistas_tmp:
        $ obj_tmp = pistas_tmp[0]
        $ R(obj_tmp)["horario"] = True
        $ di(pj, PJ[obj_tmp]["pista"])
        $ nom_tmp = nom(obj_tmp)
        $ aviso("Ahora conoces el horario de %s." % nom_tmp)
    ## Comentario sobre los rumores
    $ circ_tmp = PJ[pj].get("circulo")
    if circ_tmp and rumores.get(circ_tmp, 0) >= 30:
        $ di(pj, PJ[pj]["rumor_txt"])
    return
