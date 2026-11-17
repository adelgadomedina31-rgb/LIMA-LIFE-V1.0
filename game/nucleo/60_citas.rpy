## =============================================================================
## LIMA GRIS - Citas
## =============================================================================

init -5 python:

    def menu_lugares_cita(pj):
        res = []
        for lid in ORDEN_CITAS:
            info = CITAS[lid]
            res.append(("%s  (%s para los dos)" % (info["nombre"], soles(info["costo"])), lid))
        res.append(("Mejor otro día", "cancelar"))
        return res

    def menu_cuando(pj, lid):
        res = []
        info = CITAS[lid]
        if (ubic_pj(pj) == store.ubicacion and store.slot in info["slots"]
                and disponible_cita(pj, store.dia, store.slot)):
            res.append(("Ahora mismo", "ahora"))
        for d, s in opciones_agenda(pj, lid):
            res.append((texto_fecha_corta(d, s), (d, s)))
        res.append(("Mejor otro día", "cancelar"))
        return res


## ===================================================== INVITAR A SALIR
label invitar_salir(pj):
    "¿A dónde la invitas?"
    $ lugar_inv = renpy.display_menu(menu_lugares_cita(pj))
    if lugar_inv == "cancelar":
        return None
    $ gusto_inv = PJ[pj].get("citas_gusto", {}).get(lugar_inv, 0)
    if gusto_inv < 0:
        $ di(pj, PJ[pj].get("cita_no_lugar", "Mmm, ese plan no es mucho lo mío. ¿Y si mejor otra cosa?"))
        $ cambiar(pj, afecto=-1)
        return None
    $ cuando_inv = renpy.display_menu(menu_cuando(pj, lugar_inv))
    if cuando_inv == "cancelar":
        $ di(pj, "Ya, avísame cuando tengas tiempo, pues.")
        return None
    $ di(pj, renpy.random.choice(PJ[pj].get("cita_si", ["¡Ya, vamos!"])))
    if cuando_inv == "ahora":
        call cita(pj, lugar_inv)
        return "fin"
    $ agendar_cita(pj, lugar_inv, cuando_inv[0], cuando_inv[1])
    return None


## ================================================= CITA QUE LLEGA
label cita_agendada(c):
    $ quitar_cita(c)
    $ pj_cita = c["pj"]
    $ lugar_cita = c["lugar"]
    $ nom_tmp = nom(pj_cita)
    $ lugar_tmp = CITAS[lugar_cita]["nombre"]
    "Te llega un WhatsApp de [nom_tmp]: '¿Sigue en pie lo de hoy?'. Tienen planeado: [lugar_tmp]."
    menu:
        "Ir a la cita":
            call cita(pj_cita, lugar_cita)
        "Cancelarle a último minuto":
            $ di(pj_cita, "...Ya. Normal. Otro día será.")
            $ cambiar(pj_cita, afecto=-8, confianza=-8)
    return


## ============================================================= CITA
label cita(pj, lugar):
    $ info_c = CITAS[lugar]
    $ costo_c = info_c["costo"]
    $ viaje_c = costo_zona(info_c["zona"])
    $ hr = R(pj)
    if not puede_pagar(costo_c + viaje_c):
        "Revisas la app del banco con disimulo. No te alcanza."
        if hr["afecto"] >= 40:
            $ di(pj, "Oye, tranquilo. Vamos a medias, pues. Estamos en el siglo veintiuno.")
            $ costo_c = costo_c / 2.0
        else:
            $ di(pj, "Ah... ya. Bueno, otro día, ¿no?")
            $ cambiar(pj, afecto=-3)
            return
    $ gastar(costo_c + viaje_c, "cita: " + info_c["nombre"])
    $ ubicacion = {"bar": "barranco", "malecon": "malecon", "cena": "malecon"}.get(lugar, ubicacion)
    scene expression Solid("#22192a")
    $ nom_c = nom(pj)
    "[info_c[intro]]"
    $ gusto_c = PJ[pj].get("citas_gusto", {}).get(lugar, 0)
    if gusto_c >= 2:
        $ di(pj, PJ[pj].get("cita_le_encanta", "¡Me encanta este sitio! ¿Cómo sabías?"))
    elif gusto_c == 0:
        "[nom_c] mira alrededor sin mucho entusiasmo, pero se acomoda."

    ## --- Dos rondas de conversación
    $ temas_usados = []
    $ puntos = gusto_c * 2
    $ ronda = 0
    while ronda < 2:
        $ libres = [t for t in TEMAS if t not in temas_usados]
        $ opciones_t = renpy.random.sample(libres, 3)
        $ tema = renpy.display_menu([(TEMAS[t], t) for t in opciones_t])
        $ temas_usados.append(tema)
        $ valor_t, linea_t = PJ[pj]["temas"].get(tema, (0, "c|Ajá... ya."))
        call decir(pj, [linea_t])
        $ puntos += valor_t
        if tema in ("familia", "suenos") and valor_t > 0:
            $ cambiar(pj, confianza=2, aviso_=False)
        if tema == "coqueteo" and valor_t > 0:
            $ cambiar(pj, atraccion=3, aviso_=False)
        $ ronda += 1

    $ puntos += renpy.random.randint(-1, 1)
    $ hr["citas"] += 1
    $ extra_atr = 2 if lugar in ("cena", "bar") else 0
    $ cambiar(pj, afecto=max(1, 3 + puntos), confianza=2, atraccion=2 + extra_atr)
    if puntos >= 3:
        $ di(pj, renpy.random.choice(PJ[pj].get("cita_bien", ["Qué bonito la pasé. En serio."])))
    elif puntos >= 1:
        $ di(pj, "Estuvo bien. Me gustó salir contigo.")
    else:
        $ di(pj, renpy.random.choice(PJ[pj].get("cita_mal", ["Bueno... fue distinto. Ya hablamos, ¿sí?"])))

    ## --- ¿Alguien los vio?
    $ testigos_c = testigos_en(info_c["lugar"], slot, pj)
    if testigos_c and renpy.random.randint(1, 100) <= 55:
        $ t_c = testigos_c[0]
        $ nom_t = nom(t_c)
        $ circ_t = PJ[t_c].get("circulo") or "barrio"
        "Al salir, ves a [nom_t] a unos metros. Te saluda con la mano y una sonrisita que no te gusta nada."
        $ agregar_chisme(pj, circ_t, t_c, n=8)

    ## --- Gancho para el módulo externo (punto "cita")
    $ escena_personaje = pj
    $ escena_lugar = lugar
    $ escena_punto = "cita"
    $ esc_mod = modulo_buscar_escena(pj, "cita", lugar)
    if esc_mod:
        call expression esc_mod

    ## --- Final de la cita
    if slot == 3 and puede_intimidad(pj) and puntos >= 1:
        "La noche está agradable. Ninguno de los dos tiene ganas de que se acabe."
        menu:
            "Preguntarle si quiere que la noche siga":
                call intimidad(pj, "cita")
                if _return:
                    return
            "Acompañarla a tomar su taxi y despedirte con un beso":
                "Se despiden con un beso largo mientras el taxista finge que no ve nada."
                $ cambiar(pj, atraccion=2)
    elif not hr["beso"] and hr["afecto"] >= 40 and hr["atraccion"] >= 35:
        $ di(pj, "Bueno... llegamos.")
        "Se quedan mirándose un segundo de más."
        menu:
            "Preguntarle si puedes besarla":
                if hr["atraccion"] >= 40:
                    $ di(pj, PJ[pj].get("beso", "...Sí. Pensé que nunca ibas a preguntar."))
                    "Se besan. Corto, un poco torpe, perfecto."
                    $ hr["beso"] = True
                    $ cambiar(pj, atraccion=5, afecto=2)
                    $ escena_punto = "beso"
                    $ esc_mod = modulo_buscar_escena(pj, "beso", lugar)
                    if esc_mod:
                        call expression esc_mod
                else:
                    $ di(pj, "Todavía no... pero me gustó que preguntaras. En serio.")
                    $ cambiar(pj, confianza=3)
            "Despedirte con un abrazo":
                "La abrazas. Huele a perfume y a la garúa de la noche."
                $ cambiar(pj, afecto=1)

    if slot == 3:
        $ necesita_dormir = True
    else:
        "Se despiden y regresas a Lince."
        $ ubicacion = "casa"
        $ avanzar()
    return
