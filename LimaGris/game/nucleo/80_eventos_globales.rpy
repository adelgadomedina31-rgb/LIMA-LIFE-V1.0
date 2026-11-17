## =============================================================================
## LIMA GRIS - Eventos de la historia general (no de una sola persona)
## =============================================================================
## Día 5  (viernes)  After office en La Garúa
## Día 9  (martes)   Apagón en Los Ficus
## Día 18 (jueves)   Se cae producción: noche en la oficina
## Día 27 (sábado)   Parrillada en la azotea
## Día 33 (viernes)  Aniversario de Andina Data
## Siempre:          Llamado de Recursos Humanos / Sermón de Doña Gladys
## =============================================================================

init python:
    registrar_evento(id="glob_afteroffice", label="ev_glob_afteroffice", lugar="oficina", slots=[2], dia=5, prioridad=5)
    registrar_evento(id="glob_apagon", label="ev_glob_apagon", lugar=["casa", "edificio"], slots=[3], dia=9, prioridad=5)
    registrar_evento(id="glob_caida", label="ev_glob_caida", lugar="oficina", slots=[2], dia=18, prioridad=5)
    registrar_evento(id="glob_parrillada", label="ev_glob_parrillada", lugar=["casa", "edificio"], slots=[3], dia=27, prioridad=5)
    registrar_evento(id="glob_aniversario", label="ev_glob_aniversario", lugar="oficina", slots=[2], dia=33, prioridad=5)
    registrar_evento(id="glob_rrhh", label="ev_glob_rrhh", lugar="oficina", slots=[0, 1, 2], flags=["llamado_rrhh"],
                     repetible=True, prioridad=15, no_cuenta=False)
    registrar_evento(id="glob_sermon", label="ev_glob_sermon", lugar=["casa", "edificio"], slots=[0, 1, 2], flags=["sermon_pend"],
                     repetible=True, prioridad=15)

    def _revisar_rumores_diarios():
        if store.rumores.get("oficina", 0) >= 60 and not flag("rrhh_quincena_%d" % (store.dia // 14)):
            poner_flag("rrhh_quincena_%d" % (store.dia // 14))
            poner_flag("llamado_rrhh")
        if store.rumores.get("edificio", 0) >= 50 and not flag("sermon_%d" % (store.dia // 10)):
            poner_flag("sermon_%d" % (store.dia // 10))
            poner_flag("sermon_pend")


label ev_glob_afteroffice:
    "A las cinco de la tarde, Piero aparece en tu escritorio con la casaca puesta y cara de viernes."
    pi "Causa. Es viernes. La Garúa. Todo el equipo. No acepto un no. Bueno, sí acepto, pero me ofendo."
    menu:
        "Ir al after office":
            $ trabajo_hoy[2] = True
            $ slot = 3
            $ ubicacion = "barranco"
            scene expression fondo_lugar()
            "La Garúa es una casona vieja de Barranco con foquitos amarillos. Piero pide una jarra de chilcano 'para empezar'."
            "Están Valeria, que se sienta en la punta 'por si tiene que irse temprano'; Brenda, que habla de tres temas a la vez; y Fiorella, que dibuja en una servilleta."
            "Detrás de la barra, una bartender con los brazos tatuados agita una coctelera como si fuera un instrumento."
            call decir("carla", PJ["carla"]["presentacion"])
            $ R("carla")["conocida"] = True
            $ R("brenda")["conocida"] = True
            $ R("fiorella")["conocida"] = True
            pi "¡Por el nuevo! ¡Que dure más que el anterior!"
            br "¿Qué le pasó al anterior?"
            pi "Hizo un deploy un viernes."
            "Todos se ríen. Hasta Valeria."
            menu:
                "Sentarte al lado de Valeria":
                    va "Pensé que te ibas a sentar con Piero. Todos se sientan con Piero."
                    "Hablan una hora de series, de Comas, de Arequipa. Ella se va a las once, pero se va sonriendo."
                    $ cambiar("valeria", afecto=4, confianza=2, atraccion=2)
                "Conversar con Brenda y Fiorella":
                    "Brenda te cuenta su vida en tres minutos. Fiorella te dibuja en una servilleta: tienes cara de búho, según ella."
                    $ cambiar("brenda", afecto=4)
                    $ cambiar("fiorella", afecto=4)
                "Quedarte en la barra con Carla":
                    "Carla te hace un chilcano de maracuyá con hierbaluisa y te cuenta la vida de cada mesa del bar."
                    $ cambiar("carla", afecto=5, atraccion=2)
            $ gastar(45, "after office")
            "A la una de la mañana, Piero canta 'Contigo Perú' parado en una silla. Es momento de irse."
            $ necesita_dormir = True
        "Decirle que hoy no puedes":
            pi "Ya, causa. La próxima. Pero te pierdes de mi interpretación de 'Contigo Perú'."
    return


label ev_glob_apagon:
    scene black
    "A las nueve y cuarto, Lince entero se apaga. No solo tu edificio: toda la Av. Arequipa queda a oscuras."
    "En el pasillo se escuchan puertas. Alguien prende una vela. Después otra."
    gladys "¡Nadie se asuste! ¡Es Luz del Sur, que es una irresponsable! ¡Bajen a la escalera, que ahí corre aire!"
    "Terminan todos sentados en los escalones del segundo piso, con velas, linternas de celular y una olla de chocolate caliente que trae Lucía."
    if not R("lucia")["conocida"]:
        call decir("lucia", PJ["lucia"]["presentacion"])
        $ R("lucia")["conocida"] = True
    if not R("andrea")["conocida"]:
        call decir("andrea", PJ["andrea"]["presentacion"])
        $ R("andrea")["conocida"] = True
    ro "Esto es lo más social que ha sido este edificio desde el terremoto del 2007."
    lu "Yo traje chocolate. Andrea trajo galletas. Gladys trajo chismes."
    gladys "Yo no traigo chismes. Yo traigo información."
    an "Objeción, Doña Gladys."
    "Durante dos horas, entre velas, se cuentan historias de apagones, de terremotos, de mudanzas. Rocío se sienta a tu lado y te pasa media taza de chocolate sin decir nada."
    menu:
        "Contar una anécdota de Arequipa para todos":
            "Cuentas la vez que en Arequipa temblaste más que el temblor. Se ríen. Hasta Gladys, que intenta disimular."
            $ cambiar("rocio", afecto=3)
            $ cambiar("andrea", afecto=3)
            $ cambiar("lucia", afecto=3)
        "Quedarte conversando bajito con Rocío":
            ro "¿Sabes qué es lo bueno de los apagones? Que nadie ve las ojeras."
            "Hablan de sus mamás, que viven a cuatro cuadras en Arequipa, y de todo lo que no se dice en un pasillo con luz."
            $ cambiar("rocio", afecto=5, confianza=5, atraccion=2)
    if R("rocio")["estado"] < 1:
        $ poner_estado("rocio", 1)
    "A las once y media vuelve la luz. Todos aplauden como si hubiera aterrizado un avión."
    $ necesita_dormir = True
    return


label ev_glob_caida:
    "A las cinco de la tarde, todas las alertas se ponen rojas a la vez. El sistema de pagos de la cooperativa se cayó en producción. Tres mil socios no pueden retirar su plata."
    ma "Nadie se va. Bueno, el que quiera se va, pero que sepa que esto es lo único que importa hoy."
    menu:
        "Quedarte hasta que se arregle":
            $ trabajo_hoy[2] = True
            $ poner_flag("oficina_noche_18")
            $ presencias["18-3-valeria"] = "oficina"
            $ presencias["18-3-mariela"] = "oficina"
            $ presencias["18-3-piero"] = "oficina"
            $ slot = 3
            scene expression fondo_lugar()
            "Pizza, café de máquina y logs. Muchos logs. Valeria reproduce el error en el ambiente de pruebas; tú encuentras la consulta que bloquea la base de datos; Piero escribe el parche; Mariela habla por teléfono con el cliente sin perder la calma."
            "A las once y cuarenta, el sistema vuelve. Piero llora. Mariela pide que nadie diga 'deploy' por una semana."
            $ cambiar_desempeno(6, "salvaste producción")
            $ cambiar("valeria", afecto=3, confianza=3)
            $ cambiar("mariela", afecto=3, confianza=4)
            "Piero se va corriendo a alcanzar el último bus. En el piso nueve quedan tres personas: tú, Valeria y Mariela, recogiendo cajas de pizza."
            $ presencias["18-3-piero"] = None
            $ trasnoche = True
        "Irte a la hora de siempre":
            "Te vas. Al día siguiente, nadie te dice nada. Ese es el problema: nadie te dice nada."
            $ cambiar_desempeno(-6, "te fuiste en plena caída")
            $ cambiar("mariela", confianza=-5)
            $ trabajo_hoy[2] = True
            $ avanzar()
    return


label ev_glob_parrillada:
    scene expression Solid("#20261f")
    "Doña Gladys organizó una parrillada en la azotea 'para la integración vecinal'. En realidad, es para cobrar la cuota de mantenimiento con anticucho de por medio."
    $ gastar(30, "cuota de la parrillada")
    gladys "Cada vecino pone treinta soles. El que no pone, no come. Y el que come sin poner, lo anoto."
    "Lucía se encarga de la parrilla. Andrea pone música. Rocío trae una ensalada que nadie toca. Tú traes hielo, que es lo que te tocó."
    menu:
        "Ayudar a Lucía en la parrilla":
            lu "Así, mi rey. El anticucho se voltea una sola vez. El que lo voltea mucho, no tiene paciencia en la vida."
            $ cambiar("lucia", afecto=5, atraccion=2)
        "Bailar con Andrea":
            "Andrea pone una cumbia de Agua Marina y te saca a bailar. Gladys los mira y anota algo mentalmente."
            $ cambiar("andrea", afecto=5, atraccion=3)
            $ subir_rumor("edificio", 4)
        "Quedarte con Rocío en la baranda":
            ro "Mira, la cruz del San Cristóbal. Cuando era chica pensaba que era una estrella que se había quedado quieta."
            $ cambiar("rocio", afecto=5, confianza=3)
    "Al final de la noche, Gladys hace un discurso sobre 'la decencia del edificio' mirando a cada uno de los vecinos. Se detiene en ti un segundo de más."
    $ necesita_dormir = True
    return


label ev_glob_aniversario:
    "Kathy pasa por todos los escritorios repartiendo invitaciones doradas."
    ka "¡Hoy es el aniversario de Andina! Quince años. Fiesta en un local de Miraflores. Open bar hasta las doce. ¡Nadie se lo pierde!"
    menu:
        "Ir a la fiesta":
            $ trabajo_hoy[2] = True
            $ slot = 3
            $ ubicacion = "malecon"
            scene expression Solid("#241a2b")
            "El local está frente al malecón. Hay globos dorados, una orquesta que toca cumbia, salsa y 'Mi Perú', y un Benavides que baila con una corbata en la cabeza."
            be "¡Quince años, carajo! ¡Quince años!"
            "Todo Andina está ahí. Todos miran quién baila con quién."
            $ opciones_fiesta = [(PJ[x]["corto"], x) for x in ["valeria", "kathy", "mariela", "fiorella", "jimena", "brenda"] if R(x)["conocida"]]
            $ opciones_fiesta.append(("Quedarte en la barra con Piero", "piero"))
            "¿Con quién pasas la noche?"
            $ elegida = renpy.display_menu(opciones_fiesta)
            if elegida != "piero":
                $ nom_tmp = nom(elegida)
                "Bailas con [nom_tmp] media orquesta. Después salen a tomar aire al malecón, solos, con el ruido de la fiesta detrás."
                $ cambiar(elegida, afecto=6, confianza=3, atraccion=5)
                $ subir_rumor("oficina", 8)
                $ agregar_chisme(elegida, "oficina", "kathy" if elegida != "kathy" else "piero", n=4)
                $ presencias["%d-3-%s" % (dia, elegida)] = "malecon"
            else:
                "Piero y tú terminan cantando 'Contigo Perú' con la orquesta. Kathy lo graba. Mañana será viral en el grupo de WhatsApp de la oficina."
            $ gastar(20, "taxi y propinas")
        "Quedarte en casa":
            ka "¡Aburrido! Bueno, más chisme para mí."
    return


label ev_glob_rrhh:
    $ quitar_flag("llamado_rrhh")
    "Te llega un correo de Jimena Alvarado, Recursos Humanos. Asunto: 'Conversación breve'. Nunca es breve."
    ji "Siéntate. Esto no es un memorándum. Todavía."
    ji "Me han llegado comentarios sobre tu conducta. Fuera y dentro de horario. No me interesa tu vida privada, pero sí la imagen de la empresa y el ambiente de trabajo."
    menu:
        "Escucharla y pedir disculpas":
            ji "Bien. Que no se repita. Y si tienes algo que declarar, la puerta de Recursos Humanos está abierta. Para eso existe."
            $ cambiar_desempeno(-4)
            $ subir_rumor("oficina", -15)
        "Decirle que tu vida privada es tuya":
            ji "Tu vida privada sí. Lo que pasa en estas oficinas, no. Anotado."
            $ cambiar_desempeno(-8, "llamado de atención")
            $ subir_rumor("oficina", -5)
    return


label ev_glob_sermon:
    $ quitar_flag("sermon_pend")
    "Doña Gladys te espera en la portería con los brazos cruzados y la radio apagada. Eso es grave."
    gladys "Joven. Este es un edificio decente. Se escuchan cosas. Se ven cosas. Yo no digo nada, pero los vecinos sí."
    menu:
        "Pedirle disculpas con cara de santo":
            gladys "Ya, ya. Pero que no se repita. O que no se escuche, por lo menos."
            $ subir_rumor("edificio", -10)
        "Llevarle un pan con chicharrón para suavizarla":
            $ gastar(8, "pan con chicharrón para Gladys")
            gladys "...Esto no cambia nada. Pero está rico. Ya, váyase."
            $ subir_rumor("edificio", -15)
    return
