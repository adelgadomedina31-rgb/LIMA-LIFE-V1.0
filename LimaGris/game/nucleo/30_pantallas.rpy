## =============================================================================
## LIMA GRIS - Pantallas del juego (todo es texto, sin imágenes)
## =============================================================================

## Tamaños (se agrandan en celulares con la variante "small")
init offset = -2

define gui.lg_txt = 30
define gui.lg_btn = 32
define gui.lg_titulo = 52
define gui.lg_sub = 36
define gui.lg_hud = 28
define gui.lg_pad = 16

init python:
    @gui.variant
    def small():
        gui.lg_txt = 38
        gui.lg_btn = 40
        gui.lg_titulo = 58
        gui.lg_sub = 42
        gui.lg_hud = 34
        gui.lg_pad = 22

init offset = 0

## ---------------------------------------------------------------- Colores
define C_ACENTO = "#e0a040"
define C_TEXTO = "#e9e6df"
define C_SUAVE = "#9aa0ab"
define C_PANEL = "#141821e8"
define C_BOTON = "#262b36"
define C_BOTON_HOVER = "#3a4256"

## ---------------------------------------------------------------- Estilos
style lg_texto is default:
    size gui.lg_txt
    color C_TEXTO
    font gui.text_font

style lg_suave is lg_texto:
    color C_SUAVE
    italic True

style lg_titulo is lg_texto:
    size gui.lg_titulo
    color C_ACENTO
    bold True

style lg_sub is lg_texto:
    size gui.lg_sub
    color C_ACENTO

style lg_panel is default:
    background Solid(C_PANEL)
    padding (36, 28)

style lg_boton is default:
    background Solid(C_BOTON)
    hover_background Solid(C_BOTON_HOVER)
    insensitive_background Solid("#1a1d24")
    padding (24, gui.lg_pad)
    xfill True

style lg_boton_text is default:
    size gui.lg_btn
    color C_TEXTO
    hover_color "#ffd27a"
    insensitive_color "#5f646e"
    font gui.text_font

style lg_nav is lg_boton:
    xfill False
    xminimum 200
    padding (22, gui.lg_pad)

style lg_nav_text is lg_boton_text:
    xalign 0.5

style lg_bar is default:
    left_bar Solid(C_ACENTO)
    right_bar Solid("#2e333f")
    ysize 22
    xsize 520

style lg_toast is default:
    background Solid("#000000d0")
    padding (22, 12)

style lg_toast_text is lg_texto:
    size gui.lg_hud

style lg_vscroll is vscrollbar:
    base_bar Solid("#1b1e26")
    thumb Solid("#4a5163")
    xsize 14
    unscrollable "hide"


## =============================================================== Avisos
screen toasts():
    zorder 300
    if AVISOS:
        timer 0.4 repeat True action Function(limpiar_avisos)
        vbox:
            xalign 0.98
            ypos 110
            spacing 8
            for m in AVISOS[-5:]:
                frame:
                    style "lg_toast"
                    xalign 1.0
                    text m[0] style "lg_toast_text"

init python:
    config.overlay_screens.append("toasts")


## ================================================================= HUD
screen hud():
    zorder 40
    frame:
        background Solid("#0d0f14f0")
        xfill True
        ypos 0
        padding (30, 14)
        hbox:
            spacing 36
            text "Día %d · %s" % (dia, texto_fecha()) style "lg_texto" size gui.lg_hud color C_ACENTO
            text texto_hora() style "lg_texto" size gui.lg_hud
            text soles(dinero) style "lg_texto" size gui.lg_hud color ("#8fd18f" if dinero >= 0 else "#ff7a7a")
            text "Energía [energia]" style "lg_texto" size gui.lg_hud color ("#e9e6df" if energia > 25 else "#ff9a6a")
            text LUGARES[ubicacion]["nombre"] style "lg_suave" size gui.lg_hud


## ================================================================= HUB
## Pantalla principal de cada momento del día: quién está, qué puedes hacer.
screen hub():
    modal True
    $ L = LUGARES[ubicacion]
    $ gente = gente_aqui()
    $ acciones = acciones_aqui()

    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 860
        vbox:
            spacing 10
            text L["nombre"] style "lg_titulo"
            text descripcion_lugar() style "lg_suave"
            null height 12
            hbox:
                spacing 40
                ## --- Personas
                vbox:
                    xsize 880
                    spacing 10
                    text "Aquí ahora" style "lg_sub"
                    viewport:
                        ysize 560
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"
                        vbox:
                            spacing 10
                            xsize 850
                            if not gente:
                                text "No hay nadie conocido por aquí." style "lg_suave"
                            for pj in gente:
                                textbutton etiqueta_pj(pj) style "lg_boton" action Return(("hablar", pj))
                ## --- Acciones
                vbox:
                    xsize 880
                    spacing 10
                    text "Qué hacer" style "lg_sub"
                    viewport:
                        ysize 560
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"
                        vbox:
                            spacing 10
                            xsize 850
                            for a in acciones:
                                textbutton a[1]:
                                    style "lg_boton"
                                    action Return(("accion", a[0]))
                                    sensitive a[2]

    hbox:
        xalign 0.5
        ypos 960
        spacing 14
        textbutton "Mapa" style "lg_nav" action Return(("mapa",))
        textbutton "Contactos" style "lg_nav" action Return(("contactos",))
        textbutton "Agenda" style "lg_nav" action Return(("agenda",))
        textbutton "Mochila" style "lg_nav" action Return(("mochila",))
        if slot < 3:
            textbutton "Esperar" style "lg_nav" action Return(("esperar",))
        else:
            textbutton ("Dormir" if ubicacion == "casa" else "Volver a dormir") style "lg_nav" action Return(("dormir",))
        textbutton "Guardar" style "lg_nav" action ShowMenu("save")


## ================================================================ MAPA
screen mapa():
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "¿A dónde vas?" style "lg_titulo"
            text "Estás en %s (%s). De día vas en micro; de noche, en taxi por aplicativo." % (LUGARES[ubicacion]["nombre"], LUGARES[ubicacion]["zona"]) style "lg_suave"
            viewport:
                ysize 700
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vpgrid:
                    cols 2
                    spacing 12
                    xsize 1780
                    for lid in ORDEN_LUGARES:
                        $ abierto = lugar_abierto(lid)
                        $ costo = costo_viaje(lid)
                        $ aqui = (lid == ubicacion)
                        textbutton etiqueta_lugar(lid):
                            style "lg_boton"
                            xsize 880
                            action Return(lid)
                            sensitive (abierto and not aqui and puede_pagar(costo))
            textbutton "Volver" style "lg_nav" action Return(None)


## =========================================================== CONTACTOS
screen contactos():
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "Contactos" style "lg_titulo"
            text "Las personas que conoces. Toca un nombre para ver su perfil." style "lg_suave"
            viewport:
                ysize 680
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vpgrid:
                    cols 2
                    spacing 12
                    xsize 1780
                    for pj in ORDEN_PJ:
                        if R(pj)["conocida"]:
                            textbutton etiqueta_contacto(pj):
                                style "lg_boton"
                                xsize 880
                                action Return(pj)
            textbutton "Volver" style "lg_nav" action Return(None)


## ============================================================== PERFIL
screen perfil(pj):
    modal True
    $ d = PJ[pj]
    $ r = R(pj)
    $ extra = modulo_stats_de(pj)
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                xsize 1760
                text "%s, %d años" % (d["nombre"], d["edad"]) style "lg_titulo"
                text d["rol"] style "lg_sub"
                text d["bio"] style "lg_texto"
                if es_romance(pj):
                    null height 8
                    text "Relación: %s%s" % (ESTADOS[r["estado"]], "" if r["tipo"] == "principal" else "  ·  (todavía es alguien de paso en tu vida)") style "lg_texto" color C_ACENTO
                    hbox:
                        spacing 20
                        text "Afecto" style "lg_texto" min_width 220
                        bar value StaticValue(r["afecto"], 100) style "lg_bar"
                        text str(r["afecto"]) style "lg_texto"
                    hbox:
                        spacing 20
                        text "Confianza" style "lg_texto" min_width 220
                        bar value StaticValue(r["confianza"], 100) style "lg_bar"
                        text str(r["confianza"]) style "lg_texto"
                    hbox:
                        spacing 20
                        text "Atracción" style "lg_texto" min_width 220
                        bar value StaticValue(r["atraccion"], 100) style "lg_bar"
                        text str(r["atraccion"]) style "lg_texto"
                    text "Citas: %d   ·   Visitas: %d   ·   WhatsApp: %s" % (r["citas"], r["visitas"], "sí" if r["numero"] else "todavía no") style "lg_suave"
                    null height 8
                    text "Lo que sabes de sus gustos" style "lg_sub"
                    if r["gustos_vistos"]:
                        for cat in r["gustos_vistos"]:
                            $ g = d.get("gustos", {}).get(cat, 0)
                            text "• %s: %s" % (NOMBRE_CATEGORIA[cat], {2: "le encanta", 1: "le gusta", 0: "le da igual", -1: "no le gusta"}[g]) style "lg_texto"
                    else:
                        text "Todavía no le has regalado nada." style "lg_suave"
                    if r["confidencias"]:
                        null height 8
                        text "Lo que te ha contado" style "lg_sub"
                        for i in range(r["confidencias"]):
                            text "• " + d["confidencias"][i][1] style "lg_texto"
                null height 8
                text "Horario" style "lg_sub"
                if r["horario"]:
                    for l in texto_horario(pj):
                        text l style "lg_texto" size gui.lg_txt - 4
                else:
                    text "Todavía no conoces bien su rutina. Sigue viéndola." style "lg_suave"
                if extra:
                    null height 8
                    text "Módulo" style "lg_sub"
                    for k in sorted(extra):
                        text "• %s: %s" % (k, extra[k]) style "lg_texto"
                null height 14
                hbox:
                    spacing 14
                    if es_romance(pj) and r["numero"] and puede_invitar(pj):
                        textbutton "Escribirle para salir" style "lg_nav" action Return("invitar")
                    textbutton "Volver" style "lg_nav" action Return(None)


## ============================================================== TIENDA
screen tienda(lugar):
    modal True
    $ items = items_tienda(lugar)
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "Comprar" style "lg_titulo"
            text "Tienes %s." % soles(dinero) style "lg_suave"
            viewport:
                ysize 680
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vpgrid:
                    cols 2
                    spacing 12
                    xsize 1780
                    for i in items:
                        $ it = ITEMS[i]
                        textbutton "%s — %s%s" % (it["nombre"], soles(it["precio"]), ("  (tienes %d)" % inventario[i]) if i in inventario else ""):
                            style "lg_boton"
                            xsize 880
                            action Function(comprar, i)
                            sensitive puede_pagar(it["precio"])
            textbutton "Listo" style "lg_nav" action Return(None)


## ============================================================= MOCHILA
screen mochila():
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "Mochila" style "lg_titulo"
            text "Los regalos se entregan hablando con la persona. Lo demás lo puedes usar aquí." style "lg_suave"
            viewport:
                ysize 680
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vbox:
                    spacing 10
                    xsize 1780
                    if not inventario:
                        text "Está vacía. Solo hay un cargador y un chicle viejo." style "lg_suave"
                    for i in sorted(inventario):
                        $ it = ITEMS[i]
                        if it["cat"] == "consumo":
                            textbutton "%s x%d   ·   usar" % (it["nombre"], inventario[i]) style "lg_boton" action Function(usar_item, i)
                        else:
                            textbutton "%s x%d   ·   regalo (%s)" % (it["nombre"], inventario[i], NOMBRE_CATEGORIA[it["cat"]]) style "lg_boton" action NullAction()
            textbutton "Volver" style "lg_nav" action Return(None)


## ============================================================== AGENDA
screen agenda():
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                xsize 1760
                text "Agenda" style "lg_titulo"
                text "Hoy es %s. Desempeño en la chamba: %d/100. Estado físico: %d/100." % (texto_fecha(), desempeno, forma) style "lg_texto"
                if membresia_hasta >= dia:
                    text "Gimnasio pagado hasta el %s." % texto_fecha(membresia_hasta) style "lg_suave"
                null height 6
                text "Citas" style "lg_sub"
                if not citas_agendadas:
                    text "No tienes citas agendadas." style "lg_suave"
                for c in sorted(citas_agendadas, key=lambda x: (x["dia"], x["slot"])):
                    text "• %s — %s con %s" % (texto_fecha_corta(c["dia"], c["slot"]), CITAS[c["lugar"]]["nombre"], nom(c["pj"])) style "lg_texto"
                null height 6
                text "Freelance" style "lg_sub"
                if freelance:
                    text "• %s — faltan %d sesiones · pago %s · entrega hasta el %s" % (freelance["titulo"], freelance["sesiones"], soles(freelance["pago"]), texto_fecha(freelance["plazo"])) style "lg_texto"
                else:
                    text "Sin encargos. Revisa ofertas desde la laptop de tu depa." style "lg_suave"
                null height 6
                text "Pagos y cobros próximos" style "lg_sub"
                for l in proximos_pagos():
                    text "• " + l style "lg_texto"
                null height 6
                text "Rumores" style "lg_sub"
                for l in texto_rumores():
                    text "• " + l style "lg_texto"
                null height 6
                text "Cómo funciona" style "lg_sub"
                text "De lunes a viernes, en la mañana y en la tarde, tienes que 'Trabajar' en Andina Data. Si faltas, baja tu desempeño. El mediodía y la noche son tuyos. Los fines de semana, libres." style "lg_texto"
                text "Hablar con alguien no gasta tiempo; trabajar, entrenar, salir o esperar sí. A la noche, al hacer algo más, te vas a dormir." style "lg_texto"
                null height 10
                textbutton "Volver" style "lg_nav" action Return(None)


## =========================================================== FREELANCE
screen ofertas_freelance(ofertas):
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "ChambaDev — ofertas de hoy" style "lg_titulo"
            text "Solo puedes tener un encargo a la vez. Cada sesión es una tarde o una noche de trabajo en tu depa." style "lg_suave"
            for o in ofertas:
                textbutton "%s\n{size=-6}%d sesión%s · pago %s · entrega hasta el %s{/size}" % (o["titulo"], o["sesiones"], "" if o["sesiones"] == 1 else "es", soles(o["pago"]), texto_fecha(o["plazo"])):
                    style "lg_boton"
                    action Return(o)
                    sensitive (freelance is None)
            textbutton "Cerrar" style "lg_nav" action Return(None)


## ======================================================= ELEGIR REGALO
screen elegir_regalo(pj):
    modal True
    frame:
        style "lg_panel"
        xalign 0.5
        ypos 90
        xsize 1860
        ysize 940
        vbox:
            spacing 14
            text "¿Qué le regalas a %s?" % nom(pj) style "lg_titulo"
            viewport:
                ysize 700
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vbox:
                    spacing 10
                    for i in regalos_en_mochila():
                        textbutton "%s (x%d)" % (ITEMS[i]["nombre"], inventario[i]) style "lg_boton" action Return(i)
            textbutton "Mejor no" style "lg_nav" action Return(None)


## ======================================================== AVISO +18
screen aviso_adultos():
    modal True
    add Solid("#0b0d12")
    frame:
        style "lg_panel"
        xalign 0.5
        yalign 0.5
        xsize 1500
        vbox:
            spacing 24
            text "Aviso para adultos" style "lg_titulo" xalign 0.5
            text "Lima Gris es una historia para personas mayores de 18 años. Trata temas de relaciones de pareja, alcohol y situaciones íntimas entre adultos que dan su consentimiento. Las escenas íntimas no se muestran: el texto hace un fundido a negro." style "lg_texto"
            text "Todos los personajes son ficticios y mayores de edad. Los lugares de Lima son reales, pero las personas y los negocios que aparecen no." style "lg_texto"
            text "¿Tienes 18 años o más?" style "lg_sub" xalign 0.5
            hbox:
                xalign 0.5
                spacing 40
                textbutton "Sí, soy mayor de edad" style "lg_nav" action Return(True)
                textbutton "No, salir" style "lg_nav" action Return(False)
