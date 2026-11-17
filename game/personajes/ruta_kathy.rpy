## =============================================================================
## RUTA DE KATHY SALAS (recepción, Andina Data)
## =============================================================================
## kat_01 El mapa del chisme -> kat_02 Modelo de contorno -> kat_03 La escalera
## kat_04 Salsa en La Garúa  -> kat_05 Los seiscientos soles -> saliendo
## kat_06 La primera novia   -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="kat_01", pj="kathy", label="ev_kat_01", lugar="oficina", slots=[0], dia_min=2)
    registrar_evento(id="kat_02", pj="kathy", label="ev_kat_02", lugar="oficina", slots=[1], afecto=10, eventos=["kat_01"])
    registrar_evento(id="kat_03", pj="kathy", label="ev_kat_03", lugar="oficina", slots=[2], afecto=20, eventos=["kat_02"])
    registrar_evento(id="kat_04", pj="kathy", label="ev_kat_04", lugar="barranco", slots=[3], dias_semana=[5], confianza=20, eventos=["kat_03"])
    registrar_evento(id="kat_05", pj="kathy", label="ev_kat_05", lugar="oficina", slots=[1], afecto=40, confianza=35, atraccion=28, eventos=["kat_04"])
    registrar_evento(id="kat_06", pj="kathy", label="ev_kat_06", lugar="oficina", slots=[2], estado=2, afecto=70, confianza=58, citas=3, eventos=["kat_05"])


label ev_kat_01:
    "Kathy te hace una seña desde recepción. Tiene un post-it en la mano con un dibujo."
    ka "Ven, ven. Te hice el mapa de la oficina. No el de los baños: el del chisme."
    "En el post-it hay escritorios con flechas y corazones. Uno dice 'NO PRESTARLE PLATA'. Otro, 'LLORA LOS LUNES'. Otro, 'SE COME TU TÁPER'."
    ka "Y aquí estás tú. Todavía no tienes etiqueta. Depende de ti."
    menu:
        "Reírte y pedirle que te ponga una buena etiqueta":
            ka "Mmm. Por ahora, 'nuevo con potencial'. Ya veremos."
            $ cambiar("kathy", afecto=4, atraccion=1)
        "Preguntarle cuál es su etiqueta":
            ka "¿La mía? Nadie me pregunta eso."
            ka "...'Llega a las ocho aunque viva en la otra punta de Lima'. Esa sería."
            $ cambiar("kathy", afecto=3, confianza=4)
        "Decirle que no te gustan los chismes":
            ka "Ay, ya, ya. El señor serio. Normal. Ya te vas a enterar de todo igual."
            $ cambiar("kathy", afecto=-1, confianza=2)
    return


label ev_kat_02:
    "En la hora de almuerzo, Kathy te intercepta con una cosmetiquera del tamaño de una maleta."
    ka "Necesito un modelo. Tengo que practicar contorno en caras de hombre para un curso. Y tú tienes pómulos de ingeniero."
    p "¿Eso existe?"
    ka "Ahora sí. Siéntate."
    "Durante veinte minutos, Kathy te pinta la cara con una concentración absoluta. Piero pasa, te ve y sale corriendo a buscar a Brenda."
    ka "Listo. Mírate."
    "En el espejo de su polvera hay un hombre con una mandíbula que no es la tuya y unos pómulos de estrella de telenovela."
    ka "Quiero hacer esto. En serio. Hay un curso profesional de seis meses. Cuesta dos mil ochocientos. Ya tengo casi dos mil."
    menu:
        "Decirle que tiene un talento real":
            ka "¿De verdad? ...Gracias. La gente cree que es un hobby. No es un hobby."
            $ cambiar("kathy", afecto=4, confianza=4)
        "Pedirle una foto para tu mamá":
            ka "¡Jajaja! ¡Sí! Ponle de pie de foto: 'Por Kathy Salas Makeup'."
            $ cambiar("kathy", afecto=5, atraccion=2)
    "Te pasas la tarde desmaquillándote con papel higiénico en el baño. No sale del todo. Valeria te mira raro en la daily."
    return


label ev_kat_03:
    "Bajas por la escalera de emergencia para evitar el ascensor. En el descanso del sexto piso, Kathy está sentada, llorando bajito."
    ka "Ay, no. No me mires. Se me corrió todo."
    "Un mensajero dejó un sobre del cliente en recepción y se perdió. El Sr. Benavides le gritó delante de todos que 'para eso le pagan'."
    ka "Yo no lo perdí. Lo firmó el de seguridad. Pero nadie le pregunta al de seguridad, ¿no? Le preguntan a la recepcionista."
    menu:
        "Sentarte a su lado y escucharla":
            "Te sientas en la escalera. No dices nada. Le pasas tu pañuelo, que está limpio de casualidad."
            ka "Gracias. Eres el primero que no me dice 'ya, no llores'."
            $ cambiar("kathy", afecto=4, confianza=6)
        "Hacerla reír":
            p "Si quieres, le hago contorno a Benavides. Le pongo cara de buena gente."
            ka "¡Jajaja! ¡No! ¡Ay, me duele! Imposible. No hay base que tape eso."
            $ cambiar("kathy", afecto=6, confianza=3)
        "Ir a hablar con Benavides":
            "Subes a la oficina de Benavides y le explicas, con calma, que el sobre lo firmó seguridad. Él te mira como si fueras un bug."
            be "Joven, usted vino a programar, no a defender recepcionistas."
            "Pero esa tarde, Benavides pasa por recepción y le dice a Kathy un 'disculpe' casi inaudible."
            $ cambiar_desempeno(-3, "te peleaste con el gerente")
            $ cambiar("kathy", afecto=6, confianza=8, atraccion=2)
    if R("kathy")["estado"] < 1:
        $ poner_estado("kathy", 1)
    return


label ev_kat_04:
    scene expression Solid("#2a1717")
    "Los sábados en la noche, La Garúa es salsa. La pista está llena y el piso de madera tiembla."
    "En el centro, Kathy baila como si la gravedad fuera opcional. Te ve y te señala con el dedo."
    ka "¡Tú! ¡Ven! ¡Ni se te ocurra quedarte ahí parado!"
    menu:
        "Salir a bailar con todo":
            if forma >= 30:
                "Resulta que en Arequipa aprendiste algo. Le sigues el ritmo, la haces girar, y al final de la canción la gente aplaude."
                ka "¡¿Y eso?! ¡Me engañaste! ¡Bailas!"
                $ cambiar("kathy", afecto=5, atraccion=7)
            else:
                "Bailas con el entusiasmo de un ingeniero y la coordinación de un router viejo. Ella se ríe tanto que tiene que sentarse."
                ka "¡Eres horrible! ¡Me encanta! ¡Otra vez!"
                $ cambiar("kathy", afecto=6, atraccion=4)
        "Pedirle que te enseñe":
            ka "Ya. Uno, dos, tres... cinco, seis, siete. No, el otro pie. El OTRO pie."
            "Al final de la noche ya no pisas tanto. Ella no te suelta la mano en todo el camino al paradero."
            $ cambiar("kathy", afecto=5, confianza=3, atraccion=5)
    "A la una, la acompañas hasta el taxi colectivo que la lleva a San Juan de Lurigancho."
    ka "Avísame cuando llegues, ¿ya? Yo te aviso cuando llegue. En dos horas, ja."
    $ avanzar()
    return


label ev_kat_05:
    "A la hora del almuerzo, Kathy no sale a comer. Está en recepción con una calculadora y los ojos rojos."
    ka "Mañana vence la matrícula del curso. Me faltan seiscientos soles. Mi hermano se enfermó y tuve que pagar la consulta."
    ka "No te lo cuento para que hagas nada, ¿ya? Solo... necesitaba decírselo a alguien."
    menu:
        "Prestarle los S/ 600" if dinero >= 600:
            $ gastar(600, "préstamo a Kathy")
            $ poner_flag("kat_prestamo")
            ka "No. No, no, no. ...¿En serio? Te lo devuelvo. Con mi primer cliente. Te lo juro por mi mamá."
            $ cambiar("kathy", afecto=8, confianza=8)
        "Ofrecerle armarle una web para conseguir clientes":
            p "No tengo los seiscientos, pero tengo una laptop. Te armo una web con tu portafolio y reservas por WhatsApp. Con eso sacas clientas este mes."
            ka "¿Harías eso? ¿Por mí?"
            $ poner_flag("kat_web_pend")
            $ cambiar("kathy", afecto=6, confianza=8)
        "Animarla a hablar con el instituto para pagar en cuotas":
            p "Llama al instituto. Diles que pagas la mitad ahora y la mitad en quince días. Les conviene más que perderte."
            "Llama. Le dicen que sí. Cuelga y se queda mirando el teléfono como si fuera magia."
            ka "No necesitaba que me salvaras. Necesitaba que alguien creyera que podía. Gracias."
            $ cambiar("kathy", afecto=4, confianza=6)
    "Entonces Kathy sale de detrás del mostrador, mira a los dos lados del pasillo y te jala hacia la escalera de emergencia."
    ka "Oye. Te voy a preguntar algo y me dices la verdad. ¿Te puedo dar un beso?"
    menu:
        "Decirle que sí":
            "Te besa en el descanso de la escalera, entre el olor a cera y el ruido del ascensor. Cuando se separa, se arregla el labial con el dedo."
            ka "Ya. Ahora sí estamos saliendo. No le digas a nadie. Yo controlo la información en esta oficina."
            $ R("kathy")["beso"] = True
            $ poner_estado("kathy", 2)
            $ cambiar("kathy", atraccion=6)
        "Decirle que prefieres ir más despacio":
            ka "...Ah. Ya. No, normal. Normal."
            "Se le nota la vergüenza. Pero al rato te manda un sticker de un gato con lentes de sol. Todo bien."
            $ cambiar("kathy", afecto=-2, confianza=3)
    return


label accion_web_kathy:
    "Pasas la noche armando la web de Kathy: fotos de sus trabajos, precios, un botón de reserva por WhatsApp y un logo que diseñas tú (y que Fiorella después va a criticar)."
    "A las doce le mandas el link. Te responde con quince audios gritando."
    $ cambiar_energia(-25)
    $ poner_flag("kat_web_lista")
    $ cambiar("kathy", afecto=6, confianza=5, atraccion=3)
    $ trasnoche = (slot == 3)
    $ avanzar()
    return


label ev_kat_06:
    "Kathy te recibe en recepción con el celular en la mano, temblando."
    ka "Mira. Mira, mira, mira."
    "Es un mensaje: una novia quiere que la maquille para su matrimonio. Ella y cuatro damas. Paga mil doscientos soles."
    ka "Mi primera novia. Mi primera clienta de verdad. Con contrato y todo."
    if flag("kat_prestamo"):
        ka "Y lo primero que voy a hacer es devolverte tus seiscientos. Ni me discutas."
        $ ganar(600, "Kathy te devolvió el préstamo")
        $ quitar_flag("kat_prestamo")
    if flag("kat_web_lista"):
        ka "Me encontró por la web que me hiciste. Por tu web. ¿Entiendes lo que significa eso?"
    ka "Oye, ¿y nosotros qué somos? Porque yo a mi mamá ya le dije 'mi enamorado'. Y a mi hermano. Y al chofer del Metropolitano."
    menu:
        "Decirle que quieres ser su pareja":
            p "Somos eso. Tu enamorado. Oficialmente."
            ka "¡AY! Ya. Ya, ya, ya. Me voy a poner a llorar y tengo pestañas puestas."
            $ poner_estado("kathy", 3)
            $ cambiar("kathy", afecto=10, confianza=10, atraccion=4)
    centered "{b}Ruta de Kathy completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "kathy"
    $ escena_lugar = "oficina"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("kathy", "evento", "kat_06")
    if esc_mod:
        call expression esc_mod
    $ trabajo_hoy[2] = True
    $ slot = 3
    $ ubicacion = "malecon"
    "Esa noche celebran en el malecón con un helado de lúcuma y una botella de espumante barato que compraron en el Tambo."
    if puede_intimidad("kathy"):
        ka "No quiero agarrar el bus todavía. ¿Y si...?"
        call intimidad("kathy", "cita")
        if _return:
            return
    $ necesita_dormir = True
    return
