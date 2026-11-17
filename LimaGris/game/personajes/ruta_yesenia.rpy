## =============================================================================
## RUTA DE YESENIA HUAMÁN (Tambo, turno mañana)
## =============================================================================
## yes_01 El de siempre -> yes_02 Anatomía entre clientes -> yes_03 El borracho -> amiga
## yes_04 Domingo con Maribel -> yes_05 Farmacología (programas una app)
## yes_05b La app funciona -> saliendo
## yes_06 Uniforme blanco -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="yes_01", pj="yesenia", label="ev_yes_01", lugar="tambo", slots=[0], dia_min=2)
    registrar_evento(id="yes_02", pj="yesenia", label="ev_yes_02", lugar="tambo", slots=[1], afecto=10, eventos=["yes_01"])
    registrar_evento(id="yes_03", pj="yesenia", label="ev_yes_03", lugar="tambo", slots=[0], afecto=20, eventos=["yes_02"])
    registrar_evento(id="yes_04", pj="yesenia", label="ev_yes_04", lugar="parque", slots=[0], dias_semana=[6], confianza=22, eventos=["yes_03"])
    registrar_evento(id="yes_05", pj="yesenia", label="ev_yes_05", lugar="tambo", slots=[0, 1], afecto=38, confianza=33, eventos=["yes_04"])
    registrar_evento(id="yes_05b", pj="yesenia", label="ev_yes_05b", lugar="tambo", slots=[0, 1], atraccion=28, flags=["yes_app_lista"], eventos=["yes_05"])
    registrar_evento(id="yes_06", pj="yesenia", label="ev_yes_06", lugar="tambo", slots=[0, 1], estado=2, afecto=70, confianza=58, citas=3, eventos=["yes_05b"])


label ev_yes_01:
    "Siete y cincuenta. Entras al Tambo medio dormido. Antes de que digas nada, Yesenia ya tiene tu café en el mostrador."
    ye "Americano grande, sin azúcar, y un pan con pollo que no se va a comer hasta las once. ¿Me equivoco?"
    p "¿Cómo...?"
    ye "Usted tiene cara de lunes todos los días, joven. Las caras de lunes piden americano."
    menu:
        "Preguntarle qué cara tiene ella":
            ye "¿Yo? Cara de que me levanté a las cinco. Pero sonrío igual, porque si no, el supervisor me descuenta."
            $ cambiar("yesenia", afecto=3, confianza=3)
        "Decirle que tiene buena memoria":
            ye "Es por el instituto. Me tengo que aprender todos los huesos del cuerpo. Usted es más fácil: un café y un pan."
            $ cambiar("yesenia", afecto=4, atraccion=1)
    return


label ev_yes_02:
    "Al mediodía el Tambo está tranquilo. Yesenia tiene un libro de anatomía abierto debajo del mostrador y mueve los labios en silencio."
    ye "Escápula, clavícula, húmero... ¿Usted sabe cuántos huesos tiene la mano?"
    p "¿Cinco?"
    ye "Veintisiete. Usted es ingeniero y no sabe cuántos huesos tiene en la mano con la que escribe."
    "Se ríe, y por primera vez le ves la risa completa, la que no es de cajera."
    ye "Soy de Huancayo. Llegué a los diecinueve. Mi mamá quería que fuera profesora, pero yo quería ser enfermera desde que vi cómo cuidaron a mi abuelito en el hospital Carrión."
    menu:
        "Preguntarle si extraña Huancayo":
            ye "Todos los días. El frío, el pan de Huancayo, el mercado de los domingos. Aquí todo es gris. Hasta el pan."
            $ cambiar("yesenia", afecto=3, confianza=5)
        "Ofrecerte a tomarle la lección":
            "Le tomas la lección con el libro al revés. Se sabe todos. Bueno, casi todos. Confunde el radio con el cúbito y te echa la culpa."
            $ cambiar("yesenia", afecto=5, confianza=2)
    return


label ev_yes_03:
    "A las ocho de la mañana, un tipo que claramente no ha dormido está apoyado en el mostrador del Tambo."
    "Borracho" "Ya pe, flaquita, dame tu número. Te invito un desayuno. Dos desayunos."
    ye "Señor, le pido por favor que se retire. Hay gente esperando."
    "El tipo le agarra la muñeca. Yesenia se pone pálida."
    menu:
        "Intervenir con firmeza":
            p "Oe. Suéltala. Ahora."
            "Lo dices sin gritar. El tipo te mira, calcula y suelta. Se va murmurando algo sobre 'los de Lince'."
            $ cambiar("yesenia", afecto=5, confianza=6, atraccion=3)
        "Llamar al serenazgo y quedarte a su lado":
            "Marcas al serenazgo de Lince y te paras entre ella y el tipo sin decir nada. En cinco minutos llega una camioneta. El tipo se va antes."
            ye "Gracias por no hacer lío. Si hay lío, el supervisor me culpa a mí."
            $ cambiar("yesenia", afecto=4, confianza=8)
        "Distraerlo con una broma":
            p "Causa, el desayuno te lo invito yo. Pero en la pollería de la esquina, que este café es malísimo."
            "El tipo se ríe, se confunde y se va hacia la pollería, que está cerrada. Yesenia se tapa la boca para no reírse."
            $ cambiar("yesenia", afecto=6, confianza=4)
    ye "Le debo una, joven. ...No, ya no le digo joven. ¿Cómo te llamas de verdad?"
    p "[nombre]."
    ye "[nombre]. Ya. Ya no eres 'el de siempre'."
    if R("yesenia")["estado"] < 1:
        $ poner_estado("yesenia", 1)
    return


label ev_yes_04:
    scene expression Solid("#1c2a1f")
    "Domingo en el parque. En una banca hay una olla, un mantel de cuadros y dos mujeres: Yesenia y otra un poco mayor, con cara de pocas pulgas."
    ye "¡Hola! Ven. Ella es mi hermana Maribel. Maribel, él es... el del café."
    "Maribel" "Ah. El ingeniero. Siéntate. ¿Cuánto ganas? ¿Tienes deudas? ¿Eres casado? ¿Tienes hijos en provincia?"
    ye "¡Maribel!"
    "Maribel" "Pregunto nomás. En Lima hay mucho vivo."
    menu:
        "Contestar todo con paciencia y humor":
            p "Gano lo suficiente para pagar mi alquiler y comer menú. No tengo deudas, salvo con mi tía. No soy casado. Y mis hijos son los bugs que dejo en producción."
            "Maribel" "...Ya. Este me cae. Come."
            $ cambiar("yesenia", afecto=5, confianza=6)
        "Preguntarle a Maribel por su trabajo":
            "Maribel te cuenta de sus turnos de vigilante en un banco del Centro. Al final de la conversación, te sirve la mejor presa de pollo."
            $ cambiar("yesenia", afecto=4, confianza=7)
    "Comen caldo de gallina con papa amarilla mientras los patos se pelean por el pan. Yesenia te mira de reojo todo el rato."
    $ avanzar()
    return


label ev_yes_05:
    "Yesenia tiene ojeras y el libro de farmacología lleno de post-its de colores."
    ye "El jueves tengo el examen de farmacología. Si lo jalo, repito el ciclo. Y si repito el ciclo, no sé si me alcanza la plata para seguir."
    ye "Son doscientos medicamentos. Dosis, efectos, contraindicaciones. Mi cabeza ya no da."
    menu:
        "Ofrecerte a programarle una app de repaso":
            p "Dame tus apuntes. Esta noche te hago una app de tarjetas para el celular. Te pregunta, tú respondes, y repite lo que fallas."
            ye "¿Puedes hacer eso? ¿En una noche?"
            p "Soy ingeniero de sistemas. Es lo único útil que sé hacer."
            $ poner_flag("yes_app_pend")
            $ cambiar("yesenia", afecto=4, confianza=5)
        "Decirle que confíe en ella":
            ye "Gracias... pero confianza ya tengo. Lo que me falta es tiempo."
            "Al final igual le ofreces una app de repaso. Te mira como si le hubieras ofrecido un milagro."
            $ poner_flag("yes_app_pend")
            $ cambiar("yesenia", afecto=2, confianza=4)
    return


label accion_app_yesenia:
    "Pasas la noche escribiendo una app de tarjetas: la foto del medicamento, la pregunta, un botón de 'me la sé' y otro de 'repasar'."
    "A las dos de la mañana le mandas el link. Ella responde con un audio susurrado para no despertar a Maribel: 'Eres lo máximo. Ya duérmete'."
    $ cambiar_energia(-25)
    $ poner_flag("yes_app_lista")
    $ cambiar("yesenia", afecto=6, confianza=6, atraccion=3)
    $ trasnoche = (slot == 3)
    $ avanzar()
    return


label ev_yes_05b:
    "Apenas entras al Tambo, Yesenia sale de detrás del mostrador. Eso no lo hace nunca."
    ye "¡Diecisiete! ¡Saqué diecisiete en farmacología! ¡La más alta del salón!"
    ye "La app... la usé en el bus, en el baño, en la cola del banco. Mis compañeras me la pidieron. Ahora la usa todo el salón."
    "La de la otra caja carraspea. Yesenia vuelve a su puesto, pero te hace una seña: espérame afuera."
    "A la una, cuando termina su turno, sale con la mochila al hombro y se para frente a ti en la vereda."
    ye "Oye... ¿te puedo decir algo? Me gustas. Desde el café de las siete y cincuenta. No sé si eso está bien."
    menu:
        "Decirle que a ti también, y preguntarle si puedes besarla":
            ye "...Sí. Pero rápido, que la de la otra caja está mirando."
            "No es rápido. La de la otra caja aplaude desde adentro."
            $ R("yesenia")["beso"] = True
            $ poner_estado("yesenia", 2)
            $ cambiar("yesenia", afecto=6, confianza=5, atraccion=6)
        "Decirle que a ti también, y que vayan con calma":
            ye "Con calma. Sí. Así me gusta."
            "Te da la mano. Caminan tres cuadras así, sin decir nada, hasta la esquina de su casa."
            $ poner_estado("yesenia", 2)
            $ cambiar("yesenia", afecto=5, confianza=7, atraccion=3)
    $ subir_rumor("tambo", 8)
    return


label ev_yes_06:
    "Yesenia te espera en la puerta del Tambo con un sobre en la mano y una sonrisa que no le cabe en la cara."
    ye "Me titulé. Bueno, todavía no hay ceremonia, pero ya aprobé todo. Y... me llamaron de una clínica en Jesús María. Empiezo el lunes. Técnica en enfermería."
    ye "Esta es mi última semana en el Tambo."
    "Detrás de ella, la de la otra caja llora sin disimulo."
    ye "Mi mamá viene de Huancayo para la ceremonia. Quiero que la conozcas. Pero tengo que saber cómo presentarte."
    menu:
        "Decirle que como su enamorado":
            p "Como tu enamorado. Si tú quieres."
            ye "Claro que quiero, sonso. Mi mamá te va a traer queso de Huancayo y te va a preguntar cuándo te casas. Prepárate."
            $ poner_estado("yesenia", 3)
            $ cambiar("yesenia", afecto=10, confianza=10, atraccion=4)
    centered "{b}Ruta de Yesenia completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "yesenia"
    $ escena_lugar = "tambo"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("yesenia", "evento", "yes_06")
    if esc_mod:
        call expression esc_mod
    return
