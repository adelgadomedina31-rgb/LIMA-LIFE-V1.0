## =============================================================================
## RUTA DE ROCÍO ZEVALLOS (vecina del 302, enfermera)
## =============================================================================
## roc_01 Sin llaves (noche del día 1) -> roc_02 La laptop y Arequipa
## roc_03 Pisco en la escalera (si te perdiste el apagón) -> amiga
## roc_04 Después del turno -> roc_05 Julio en la puerta -> saliendo
## roc_06 La firma -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="roc_01", pj="rocio", label="ev_roc_01", lugar=["casa", "edificio"], slots=[3], dia=1, presente=False, prioridad=10)
    registrar_evento(id="roc_02", pj="rocio", label="ev_roc_02", lugar="edificio", slots=[2, 3], afecto=8, eventos=["roc_01"])
    registrar_evento(id="roc_03", pj="rocio", label="ev_roc_03", lugar="edificio", slots=[3], afecto=20, eventos=["roc_02"],
                     cond=lambda: R("rocio")["estado"] < 1)
    registrar_evento(id="roc_04", pj="rocio", label="ev_roc_04", lugar="edificio", slots=[3], dias_semana=[4], confianza=22, estado=1)
    registrar_evento(id="roc_05", pj="rocio", label="ev_roc_05", lugar="edificio", slots=[3], afecto=38, confianza=33, atraccion=28, eventos=["roc_04"])
    registrar_evento(id="roc_06", pj="rocio", label="ev_roc_06", lugar="edificio", slots=[3], estado=2, afecto=70, confianza=58, citas=3, eventos=["roc_05"])


label ev_roc_01:
    scene expression Solid("#20261f")
    "Cuando llegas al tercer piso, una mujer en uniforme celeste de enfermera está sentada en la escalera, con la cartera volteada a su lado."
    call decir("rocio", PJ["rocio"]["presentacion"])
    ro "Dejé las llaves en el casillero del hospital. Después de veinticuatro horas de turno. Soy una profesional de la salud, como ves."
    ro "Doña Gladys tiene copia, pero ya se fue a dormir, y si la despierto me lo va a cobrar hasta el día de mi muerte."
    menu:
        "Llamar a un cerrajero y pagarlo tú (S/ 60)" if dinero >= 60:
            $ gastar(60, "cerrajero")
            "El cerrajero llega en media hora, abre la puerta en treinta segundos y cobra sesenta soles. Ella intenta pagarte. No la dejas."
            ro "Te debo un favor, vecino. Y yo pago mis favores. Si alguna vez te cortas cocinando, toca el 302."
            $ cambiar("rocio", afecto=6, confianza=4)
        "Despertar a Doña Gladys para que le dé la copia":
            "Doña Gladys abre en bata, con ruleros y cara de juicio final. Le da la llave a Rocío mirándote a ti."
            gladys "Qué amigos tan rápido, ¿no? Buenas noches."
            ro "Gracias, vecino. Y perdón por meterte en el radar de la Gladys tan pronto."
            $ cambiar("rocio", afecto=4, confianza=3)
            $ subir_rumor("edificio", 5)
        "Invitarla a esperar en tu depa con un café":
            "Le preparas un café y le prestas tu sillón. A los diez minutos está dormida, con la taza en la mano."
            "La tapas con una frazada. A las seis de la mañana, cuando Doña Gladys abre la portería, ella se va con la llave y te deja un post-it: 'Gracias, vecino. Te debo una. R.'"
            $ cambiar("rocio", afecto=6, confianza=6, atraccion=2)
            $ subir_rumor("edificio", 8)
    $ R("rocio")["conocida"] = True
    $ registrar_visita("rocio")
    return


label ev_roc_02:
    "Rocío toca tu puerta con una laptop en los brazos, como si cargara un paciente."
    ro "Vecino, emergencia. Mi laptop está llena de ventanas que dicen que gané un iPhone. Y hoy tengo videollamada con mi mamá en Arequipa."
    "Le limpias la laptop en su sala. Su depa es igual al tuyo, pero ordenado, lleno de plantas y con una foto de una señora en el Misti."
    ro "¿Tú viviste en Arequipa, no? La Gladys me dijo."
    p "Tres años. Mi mamá sigue allá."
    ro "¡No! ¿En qué parte?"
    "Resulta que sus mamás viven a cuatro cuadras una de la otra, en Cayma. Se ríen de lo chico que es el mundo."
    "La videollamada funciona. La mamá de Rocío te ve por la cámara y pregunta: '¿Y ese joven?'. Rocío cierra la laptop de golpe."
    $ cambiar("rocio", afecto=5, confianza=5, atraccion=2)
    return


label ev_roc_03:
    "Rocío está sentada en la escalera con una botella de pisco y dos vasitos de plástico."
    ro "Siéntate, vecino. Hoy se me murió un paciente. Un señor de ochenta que me contaba chistes. No me preguntes nada, solo tómate uno conmigo."
    "Se toman un pisco en silencio. Después otro. Después ella empieza a contar los chistes del señor, y se ríen hasta que Doña Gladys golpea el techo con una escoba."
    $ poner_estado("rocio", 1)
    $ cambiar("rocio", afecto=5, confianza=6)
    return


label ev_roc_04:
    "Viernes en la noche. Rocío llega al edificio arrastrando los pies después de su turno de noche del jueves y de una mañana de papeleo."
    ro "No tengo fuerzas ni para abrir la puerta. Y no he comido nada desde ayer."
    menu:
        "Cocinarle un caldito en tu depa":
            "Le haces un caldo de pollo con fideos, papa y kión, como el de tu mamá. No te sale como el de tu mamá, pero se acerca."
            ro "...Esto sabe a Arequipa. ¿Cómo hiciste para que sepa a Arequipa?"
            "Se queda dormida en tu sillón otra vez. Esta vez, al despertarse, no se va corriendo. Se queda conversando hasta la medianoche."
            $ cambiar("rocio", afecto=6, confianza=7, atraccion=2)
        "Pedir delivery de pollo a la brasa para los dos":
            $ gastar(45, "pollo a la brasa")
            "Comen un cuarto de pollo cada uno en su sala, con las manos, viendo un programa de concursos horrible."
            ro "Esto es lo más cerca que he estado de una cita en un año. Qué triste. Qué bonito."
            $ cambiar("rocio", afecto=6, confianza=5, atraccion=3)
    return


label ev_roc_05:
    "A las diez de la noche, alguien golpea la puerta del 302 con fuerza. Una voz de hombre, pastosa de alcohol."
    "Julio" "¡Rocío! ¡Ábreme! ¡Solo quiero hablar! ¡Es mi casa también!"
    "Rocío abre tu puerta, que está al lado, y se mete en tu depa con la cara blanca."
    ro "Es Julio. Mi ex. Bueno, mi esposo, técnicamente. No ha firmado el divorcio."
    menu:
        "Salir a hablar con él, con calma, mientras ella decide qué hacer":
            "Sales al pasillo. Julio es un tipo grande, con los ojos rojos. Le dices, despacio, que Rocío no quiere hablar hoy, que vuelva mañana sobrio."
            "Él te mira de arriba abajo, calcula, y se le cae algo en la cara. Se sienta en la escalera y llora."
            "Rocío sale. Le habla bajito. Le pide un taxi. Julio se va."
            ro "Gracias por no hacerte el macho. Eso lo hubiera empeorado."
            $ cambiar("rocio", afecto=6, confianza=8)
        "Llamar al serenazgo y quedarte con ella adentro":
            "El serenazgo llega en diez minutos y se lleva a Julio, que no opone resistencia. Doña Gladys lo ve todo desde la portería."
            ro "Gracias. Yo no podía llamar. No sé por qué. Doce años."
            $ cambiar("rocio", afecto=5, confianza=7)
            $ subir_rumor("edificio", 6)
        "Preguntarle a ella qué quiere hacer":
            p "¿Qué necesitas que haga? Lo que tú digas."
            ro "...Nadie me pregunta eso nunca. Quédate aquí conmigo. Él se va a ir solo. Siempre se va."
            "Y se va. A los veinte minutos, los golpes paran."
            $ cambiar("rocio", afecto=6, confianza=10)
    "Más tarde suben a la azotea con lo que queda del pisco. Entre la ropa tendida, las macetas y una ruda que, según ella, es contra la mala vibra."
    ro "En Lima no se ven estrellas. Se ve una sola, y siempre es un avión."
    ro "Oye. Me gustas. Y eso me asusta más que Julio. ¿Puedo...?"
    menu:
        "Decirle que sí":
            "Te besa entre una sábana tendida y un limonero enano. Abajo, Lima sigue con su ruido de siempre."
            $ R("rocio")["beso"] = True
            $ poner_estado("rocio", 2)
            $ cambiar("rocio", afecto=5, atraccion=8)
        "Decirle que hoy no, que fue un día muy duro para ella":
            ro "...Tienes razón. Eres buena gente, vecino. Demasiado. Otro día."
            "Te da un beso en la frente y baja a su depa. Pero a la mañana siguiente encuentras un post-it en tu puerta: 'Otro día = pronto. R.'"
            $ poner_estado("rocio", 2)
            $ cambiar("rocio", afecto=4, confianza=6, atraccion=3)
    return


label ev_roc_06:
    "Rocío te espera en la azotea con un sobre de manila y una botella de vino de Ica."
    ro "Julio firmó. Hoy. Ya está. Soy una mujer divorciada, vecino."
    "Brindan en vasos de plástico. Ella riega sus plantas con lo que queda del vino. 'Para que celebren también', dice."
    ro "Oye. Estoy cansada de esconderme de la Gladys. De salir diez minutos después que tú. De hacer como que no te conozco en la escalera."
    ro "¿Y si somos algo de verdad? Con la Gladys y todo."
    menu:
        "Decirle que sí, que quieres ser su pareja":
            p "Sí. Con la Gladys y todo."
            "Bajan juntos de la mano. Doña Gladys está en la portería. Los mira. Ve las manos."
            gladys "...Ya era hora, pues. Se les notaba desde la cuadra."
            $ poner_estado("rocio", 3)
            $ cambiar("rocio", afecto=10, confianza=10, atraccion=4)
            $ poner_flag("roc_publico")
            $ subir_rumor("edificio", -30)
    centered "{b}Ruta de Rocío completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "rocio"
    $ escena_lugar = "azotea"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("rocio", "evento", "roc_06")
    if esc_mod:
        call expression esc_mod
    if puede_intimidad("rocio"):
        ro "¿Bajamos? Mi depa está más ordenado que el tuyo."
        call intimidad("rocio", "cita")
        if _return:
            return
    return
