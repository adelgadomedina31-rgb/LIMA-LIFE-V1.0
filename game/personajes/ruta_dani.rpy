## =============================================================================
## RUTA DE DANI TORRES (Tambo, turno noche)
## =============================================================================
## Empieza como secundaria: pasa seguido por el Tambo de noche.
## dan_01 La salchipapa de microondas -> dan_02 'Veneca' -> dan_03 El puente -> amiga
## dan_04 El lago y el mar -> dan_05 La apostilla -> saliendo
## dan_06 Casco blanco -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="dan_01", pj="dani", label="ev_dan_01", lugar="tambo", slots=[3])
    registrar_evento(id="dan_02", pj="dani", label="ev_dan_02", lugar="tambo", slots=[3], afecto=10, eventos=["dan_01"])
    registrar_evento(id="dan_03", pj="dani", label="ev_dan_03", lugar="tambo", slots=[3], principal=True, afecto=20, eventos=["dan_02"])
    registrar_evento(id="dan_04", pj="dani", label="ev_dan_04", lugar="malecon", slots=[2], dias_semana=[6], confianza=22, eventos=["dan_03"])
    registrar_evento(id="dan_05", pj="dani", label="ev_dan_05", lugar="tambo", slots=[3], afecto=38, confianza=33, atraccion=28, eventos=["dan_04"])
    registrar_evento(id="dan_06", pj="dani", label="ev_dan_06", lugar="tambo", slots=[3], estado=2, afecto=70, confianza=58, citas=3, eventos=["dan_05"])


label ev_dan_01:
    "Diez y media de la noche. El Tambo está vacío salvo por la cajera de rulos, que canta una gaita bajito mientras repone cigarros."
    da "Epa. ¿Insomnio o hambre?"
    p "Hambre. ¿Qué me recomiendas?"
    da "Todo menos la salchipapa del microondas. Esa es un crimen de lesa humanidad. Llévate el sándwich de pollo y un yogurt. Confía en mí."
    da "Dani, de Maracaibo. Tú eres el del cuarto piso de Los Ficus, ¿no? La señora Gladys viene a comprar y me cuenta todo."
    menu:
        "Preguntarle por Maracaibo":
            da "Calor, chamo. Calor de verdad. Y gaitas en diciembre. Y mi mamá, que es lo que más extraño."
            $ cambiar("dani", afecto=4, confianza=3)
        "Hacerle caso con el sándwich":
            "El sándwich está sorprendentemente bueno. Ella te mira comerlo con orgullo, como si lo hubiera cocinado."
            $ gastar(9, "sándwich y yogurt")
            $ cambiar("dani", afecto=4, atraccion=1)
    return


label ev_dan_02:
    "Estás en la cola del Tambo cuando el señor de adelante le tira el vuelto a Dani sobre el mostrador."
    "Señor" "Ustedes los venecos vienen a quitarnos la chamba. Cuenta bien, oye."
    "Dani cuenta el vuelto. Lo cuenta bien. No le tiemblan las manos, pero sí la mandíbula."
    menu:
        "Ponerle un alto al señor":
            p "Señor, ella contó bien. Y usted está siendo un maleducado. Pague y váyase."
            "El señor te mira, murmura algo y se va. Dani no dice nada por un rato."
            da "Gracias. Pero no tenías que meterte. Esto me pasa tres veces por semana."
            p "Por eso mismo."
            $ cambiar("dani", afecto=5, confianza=6)
        "Esperar a que se vaya y preguntarle si está bien":
            da "Sí, chamo. Normal. Ya tengo callo."
            "Pero se queda mirando la puerta un rato largo. Le compras un chocolate y se lo dejas en el mostrador sin decir nada."
            $ cambiar("dani", afecto=4, confianza=4)
        "Hacer un chiste para que el señor quede en ridículo":
            p "Tranquilo, señor, que a usted nadie le va a quitar la chamba. Para eso habría que saber qué hace."
            "La cola entera se ríe. El señor se va rojo. Dani se muerde los labios para no reírse."
            $ cambiar("dani", afecto=6, atraccion=2)
    return


label ev_dan_03:
    "Las once. El Tambo vacío. Dani te enseña su celular: fotos de un puente en construcción, gente con cascos, y ella en el medio con un plano en la mano."
    da "Ese es el puente de La Cañada. Trabajé ahí tres años. Yo calculé las vigas del tramo dos."
    da "Aquí soy 'la venezolana del Tambo'. Allá era la ingeniera Torres."
    da "Para trabajar de ingeniera aquí, tengo que convalidar el título en SUNEDU. Papeles, apostillas, traducciones. Llevo dos años en eso."
    menu:
        "Decirle que va a volver a ser la ingeniera Torres":
            da "...Ojalá, chamo. Ojalá. Gracias por decirlo como si fuera seguro."
            $ cambiar("dani", afecto=4, confianza=6)
        "Preguntarle cómo calculó las vigas":
            "Te explica durante veinte minutos, con un lapicero y una bolsa de papel del Tambo, cómo se calcula una viga postensada. No entiendes la mitad. Te encanta igual."
            $ cambiar("dani", afecto=5, confianza=4, atraccion=3)
    if R("dani")["estado"] < 1:
        $ poner_estado("dani", 1)
    return


label ev_dan_04:
    scene expression Solid("#1a2433")
    "Domingo en la tarde. En el malecón, apoyada en la baranda, Dani mira el mar sin parpadear."
    da "En Maracaibo no hay mar. Hay lago. Pero huele parecido. Cuando lo extraño mucho, vengo aquí."
    da "Hoy hablé con mi mamá. Está bien, pero la noté cansada. Le mando doscientos dólares al mes. A veces no llego, y le miento."
    menu:
        "Contarle de tu papá":
            p "Mi papá murió hace dos años. Yo estaba en Lima cuando se enfermó, y tardé en irme a Arequipa. Todavía me pesa."
            da "...Ay, chamo. Ven acá."
            "Te abraza fuerte, con el viento del Pacífico despeinándolos a los dos."
            $ cambiar("dani", afecto=5, confianza=7, atraccion=3)
        "Quedarte callado a su lado mirando el mar":
            "No dicen nada durante un buen rato. Cuando el sol se esconde detrás de la neblina, ella apoya la cabeza en tu hombro."
            $ cambiar("dani", afecto=5, confianza=5, atraccion=4)
    $ avanzar()
    return


label ev_dan_05:
    "Dani está en la caja con una carpeta llena de papeles y una cara de derrota que no le habías visto nunca."
    da "Ya casi. Me falta la traducción oficial del título y la apostilla de las notas. Son cuatrocientos cincuenta soles y llenar seis formularios que se caen cada vez que los envío."
    da "Este mes le mandé todo a mi mamá. No tengo ni para el pasaje."
    menu:
        "Pagarle el trámite (S/ 450)" if dinero >= 450:
            $ gastar(450, "trámite de Dani")
            $ poner_flag("dan_pago")
            da "No, no, no. ...Ay, chamo. Te lo devuelvo con mi primer sueldo de ingeniera. Y con intereses, que yo sé de finanzas."
            $ cambiar("dani", afecto=8, confianza=8)
        "Ofrecerte a llenar los formularios con ella por videollamada":
            p "Los formularios caídos son mi especialidad. Te ayudo a llenarlos una noche y vemos cómo juntar la plata de la traducción."
            $ poner_flag("dan_tramite_pend")
            $ cambiar("dani", afecto=6, confianza=8)
    "A las once, cierra la caja. Sales con ella a la vereda. Lince está vacío y huele a pan de la panadería de la esquina."
    da "Oye. ¿Te puedo decir algo sin que te asustes? Me gustas. Mucho. Desde lo del señor de las monedas."
    menu:
        "Decirle que a ti también y preguntarle si puedes besarla":
            da "Pensé que nunca ibas a preguntar."
            "Se besan bajo el letrero del Tambo, que parpadea como si también estuviera nervioso."
            $ R("dani")["beso"] = True
            $ poner_estado("dani", 2)
            $ cambiar("dani", afecto=6, atraccion=7)
        "Decirle que te gusta, pero que tienes miedo de complicarle la vida":
            da "Mi vida ya es complicada, chamo. Tú eres lo más fácil que me ha pasado."
            "Te da un beso en la mejilla y se va caminando a su casa, cantando."
            $ poner_estado("dani", 2)
            $ cambiar("dani", afecto=5, confianza=5, atraccion=4)
    $ subir_rumor("tambo", 6)
    return


label accion_tramite_dani:
    "Pasas la noche en videollamada con Dani llenando los seis formularios de SUNEDU. Tres veces se cae la página. Tres veces la levantas."
    "A la una de la mañana, el último formulario dice: 'Solicitud enviada'. Ella grita tan fuerte que su prima se despierta."
    "Además, Sofía, la de la librería, conoce a una traductora oficial que le hace precio de amiga."
    $ cambiar_energia(-20)
    $ poner_flag("dan_tramite_listo")
    $ cambiar("dani", afecto=6, confianza=6, atraccion=2)
    $ trasnoche = (slot == 3)
    $ avanzar()
    return


label ev_dan_06:
    "Dani te espera en la puerta del Tambo con un casco blanco en la mano. Un casco de obra de verdad."
    da "¡Me llegó! ¡La convalidación! ¡Soy ingeniera civil en el Perú, chamo!"
    da "Y ya tengo chamba. Asistente de residente en una obra en Carabayllo. Empiezo el lunes. Hoy es mi último turno en el Tambo."
    if flag("dan_pago"):
        da "Y con mi primer sueldo te devuelvo los cuatrocientos cincuenta. Con intereses. Te lo juré."
        $ ganar(450, "Dani te devolvió el préstamo")
        $ quitar_flag("dan_pago")
    da "Mi mamá lloró por videollamada. Me dijo que te diera las gracias. Y que te preguntara si vas en serio conmigo."
    menu:
        "Decirle que sí, que quieres ser su pareja":
            p "Dile que sí. Que voy en serio. Que soy tu enamorado."
            da "¡Ay! Ya le escribo. No. Mejor te pongo en la llamada de mañana. Prepárate para la entrevista maracucha."
            $ poner_estado("dani", 3)
            $ cambiar("dani", afecto=10, confianza=10, atraccion=4)
    centered "{b}Ruta de Dani completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "dani"
    $ escena_lugar = "tambo"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("dani", "evento", "dan_06")
    if esc_mod:
        call expression esc_mod
    if puede_intimidad("dani"):
        da "Mi último turno termina a las once. ¿Me esperas?"
        call intimidad("dani", "cita")
        if _return:
            return
    return
