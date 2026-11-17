## =============================================================================
## LIMA GRIS - Aviso +18, inicio y prólogo
## =============================================================================

label splashscreen:
    scene black
    call screen aviso_adultos
    if not _return:
        $ renpy.quit()
    return


label start:
    scene black
    $ quick_menu = False
    centered "{size=+30}{color=#e0a040}LIMA GRIS{/color}{/size}\n\nUna novela de texto"
    $ nombre_tmp = renpy.input("¿Cómo se llama tu personaje? (déjalo vacío para 'Renzo')", length=16)
    $ nombre_tmp = nombre_tmp.strip()
    $ nombre = nombre_tmp if nombre_tmp else "Renzo"
    $ dinero = DINERO_INICIAL
    $ asegurar_rel()
    $ quick_menu = True

    centered "Lima. Marzo. El cielo color panza de burro de siempre."
    "Te llamas [nombre]. Tienes treinta años y eres ingeniero de sistemas."
    "Hace tres años te fuiste a Arequipa: tu papá estaba enfermo, tu relación con Paola se estaba cayendo a pedazos y necesitabas aire."
    "Tu papá ya no está. Tu mamá se quedó en Arequipa con tu hermana. Y tú volviste a Lima con dos maletas, una laptop y un trabajo nuevo."
    "Alquilaste un minidepartamento en el cuarto piso del Edificio Los Ficus, en Lince. Mil cien soles al mes. Ventana a la Av. Arequipa. Agua caliente, a veces."
    "Hoy es lunes. Tu primer día en Andina Data, una empresa de software en San Isidro que hace sistemas para cooperativas de ahorro."
    scene expression Solid("#20261f")
    "A las siete y media bajas las escaleras. En la portería, una señora de chompa tejida te detiene con la mirada."
    call decir("gladys", PJ["gladys"]["presentacion"])
    $ R("gladys")["conocida"] = True
    p "Estamos, señora."
    gladys "Doña Gladys. Y que le vaya bien en su primer día, joven. Se le nota en la cara."

    scene expression Solid("#2a1f22")
    "En la esquina está el Tambo. Entras por un café para no dormirte en el micro."
    call decir("yesenia", PJ["yesenia"]["presentacion"])
    $ R("yesenia")["conocida"] = True
    $ cambiar("yesenia", afecto=2, aviso_=False)
    $ gastar(6, "café", silencioso=True)

    scene expression Solid("#1a2228")
    "El micro te deja en la Av. Javier Prado. El edificio de Andina Data es de vidrio y tiene un ascensor que habla."
    call decir("kathy", PJ["kathy"]["presentacion"])
    $ R("kathy")["conocida"] = True
    "Kathy te da tu fotocheck. En la foto sales con cara de detenido."
    call decir("piero", PJ["piero"]["presentacion"])
    $ R("piero")["conocida"] = True
    call decir("mariela", PJ["mariela"]["presentacion"])
    $ R("mariela")["conocida"] = True
    call decir("valeria", PJ["valeria"]["presentacion"])
    $ R("valeria")["conocida"] = True
    "A las once pasa un señor de terno hablando por celular. Piero se pone serio de golpe."
    pi "Ese es Benavides. El gerente. Si te pregunta algo, di 'estamos en eso'. Siempre funciona."
    $ R("benavides")["conocida"] = True
    "Pasas la mañana instalando programas, leyendo documentación de 2016 y aprendiendo los nombres de todos."
    $ trabajo_hoy[0] = True
    $ slot = 1
    $ ubicacion = "oficina"

    scene expression fondo_lugar()
    centered "{b}Cómo se juega{/b}\n\nCada día tiene cuatro momentos: mañana, mediodía, tarde y noche.\nDe lunes a viernes, en la mañana y en la tarde, usa 'Trabajar' en la oficina.\nHablar con la gente no gasta tiempo. Trabajar, entrenar, salir o esperar, sí.\nUsa el Mapa para moverte. Cada persona tiene su rutina: búscala donde suele estar."
    centered "Visita seguido a quien te interese: así la conoces de verdad.\nLos regalos, las citas y las conversaciones cuentan.\nY ojo: en Lima todo se sabe. Lo que hagas, y dónde lo hagas, tiene consecuencias."
    show screen hud
    jump hub
