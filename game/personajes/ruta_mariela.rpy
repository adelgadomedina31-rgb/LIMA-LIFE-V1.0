## =============================================================================
## RUTA DE MARIELA CORNEJO (jefa de proyecto, Andina Data)
## =============================================================================
## Empieza como secundaria: háblale seguido en la oficina para que sea principal.
## mar_01 Sprint review         -> mar_02 Jueves de horas extra (requiere principal)
## mar_03 El carro que no arranca -> amiga
## mar_04 Cevichería en Surquillo -> mar_05 Sábado en el malecón -> saliendo
## mar_crisis Se habla de ustedes  (si hay rumores en la oficina)
## mar_06 El ascenso               -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="mar_01", pj="mariela", label="ev_mar_01", lugar="oficina", slots=[0], dia_min=3)
    registrar_evento(id="mar_02", pj="mariela", label="ev_mar_02", lugar="oficina", slots=[3], principal=True, afecto=15, eventos=["mar_01"])
    registrar_evento(id="mar_03", pj="mariela", label="ev_mar_03", lugar="oficina", slots=[2], afecto=24, confianza=18, eventos=["mar_02"])
    registrar_evento(id="mar_04", pj="mariela", label="ev_mar_04", lugar="oficina", slots=[1], confianza=28, eventos=["mar_03"])
    registrar_evento(id="mar_05", pj="mariela", label="ev_mar_05", lugar="malecon", slots=[3], dias_semana=[5],
                     afecto=40, confianza=36, atraccion=30, eventos=["mar_04"])
    registrar_evento(id="mar_crisis", pj="mariela", label="ev_mar_crisis", lugar="oficina", estado=2, prioridad=20,
                     sin_flags=["mar_transfer"], cond=lambda: rumores["oficina"] >= 45)
    registrar_evento(id="mar_06", pj="mariela", label="ev_mar_06", lugar="oficina", slots=[2], estado=2,
                     afecto=70, confianza=58, citas=3, eventos=["mar_05"])
    registrar_evento(id="mar_06b", pj="mariela", label="ev_mar_06b", lugar="oficina", slots=[2], estado=2,
                     flags=["mar_pendiente"], eventos=["mar_06"], cond=lambda: dia >= R("mariela")["dia_estado"] + 5)


label ev_mar_01:
    "Sprint review. Sala de reuniones, proyector que parpadea, nueve personas y Mariela en la cabecera."
    ma "Tú. El nuevo. Estimaste el módulo de cuotas en tres días. ¿Por qué tres?"
    "Todos te miran. Piero se hunde en su silla."
    menu:
        "Explicar honestamente: tres días si nadie cambia los requerimientos":
            p "Tres días si el cliente no cambia la regla de los intereses moratorios. Si la cambia, cinco. Y la va a cambiar."
            "Silencio. Mariela anota algo."
            ma "Bien. Eso es una estimación. No un deseo. Gracias."
            $ cambiar("mariela", afecto=3, confianza=5)
            $ cambiar_desempeno(2, "buena estimación")
        "Prometer que lo tienes en dos":
            p "En realidad, creo que en dos lo saco."
            ma "Perfecto. Dos días. Lo anoto. Con tu nombre."
            "Piero te mira como quien mira a alguien que acaba de firmar su sentencia."
            $ cambiar("mariela", afecto=-1)
            $ cambiar_desempeno(-2)
        "Decir que depende de lo que entregue Piero":
            ma "Ajá. O sea que el problema es de otro. Qué novedad en esta empresa."
            "Piero no te habla el resto de la mañana."
            $ cambiar("mariela", confianza=-3)
    return


label ev_mar_02:
    "Jueves, nueve de la noche. El piso nueve está vacío, salvo por una luz en la sala de reuniones."
    "Mariela está ahí, con los zapatos al lado de la silla y tres hojas de Excel abiertas."
    ma "¿Qué haces aquí todavía? Ve a tu casa."
    p "¿Y tú?"
    ma "Yo soy la jefa. Los jefes no tenemos casa. Tenemos reportes."
    "Te sirves un café de la máquina, que esta vez funciona. Le sirves otro a ella sin preguntar."
    ma "...Gracias. Benavides quiere que el Chasqui salga en treinta días. El directorio de la cooperativa lo presiona a él, él me presiona a mí, y yo..."
    ma "Yo no presiono a nadie. Me lo como yo. Así funciona."
    menu:
        "Ofrecerte a ayudarla con el reporte":
            "Te quedas una hora más. Arreglas las fórmulas de su Excel, que tenían referencias rotas desde 2021."
            ma "No le digas a nadie que me ayudaste. Me arruinas la reputación de bruja."
            $ cambiar("mariela", afecto=4, confianza=4)
            $ cambiar_desempeno(2)
        "Decirle que no tiene que cargar todo sola":
            ma "Qué fácil se dice. ...Pero gracias. Hace tiempo nadie me decía eso."
            $ cambiar("mariela", afecto=3, confianza=6)
    $ trasnoche = True
    return


label ev_mar_03:
    "A las seis y media, en el estacionamiento del sótano, alguien le da con furia al volante de un carro gris."
    ma "¡No arranca! ¡Hoy no! Luana sale de su clase de natación a las siete y media."
    menu:
        "Revisar el carro":
            "Abres el capó con la seguridad de quien ha visto muchos videos de YouTube. Es el borne de la batería, flojo y sulfatado."
            "Lo limpias con una servilleta y un poco de Coca-Cola del Tambo. El carro arranca."
            ma "¿Eres ingeniero de sistemas o mecánico?"
            p "Ingeniero de sistemas que tuvo un Tico en la universidad."
            $ cambiar("mariela", afecto=5, confianza=4, atraccion=3)
        "Pedir una grúa por la app del seguro y acompañarla mientras llega":
            "Esperan cuarenta minutos sentados en la vereda. Ella llama a su ex para que recoja a Luana. Él no contesta. Llama a su mamá."
            ma "Gracias por quedarte. No tenías que."
            $ cambiar("mariela", afecto=4, confianza=6)
    ma "Te llevo. Vives en Lince, ¿no? Me queda de paso. Bueno, no me queda de paso, pero sube."
    "En el carro suena una lista de canciones de Juan Luis Guerra. Ella canta bajito sin darse cuenta. Tú no dices nada para no romper el momento."
    $ trabajo_hoy[2] = True
    $ ubicacion = "casa"
    $ avanzar()
    if R("mariela")["estado"] < 1:
        $ poner_estado("mariela", 1)
    return


label ev_mar_04:
    "Mariela pasa por tu escritorio y deja un post-it: 'Almuerzo. Surquillo. 1 p.m. No es una reunión.'"
    scene expression Solid("#2b2618")
    "La cevichería está en una calle sin nombre de Surquillo y tiene cola de taxistas, que es la mejor señal posible."
    ma "Aquí venía con mi papá cuando era chica. Él era taxista. Por eso conozco estos huecos."
    "Piden un ceviche de pescado y un arroz con mariscos para compartir. Ella come con hambre de verdad, sin la pose de la oficina."
    ma "Me divorcié hace dos años. Tengo una hija de ocho, Luana. Los fines de semana está con su papá. Esos fines de semana no sé qué hacer con mi vida."
    ma "Te lo cuento porque... no sé por qué te lo cuento. Esto que estamos hablando no sale de aquí."
    menu:
        "Contarle algo tuyo a cambio":
            p "Yo me fui a Arequipa cuando mi papá se enfermó. Y me quedé cuando se murió. Volví porque allá todo me recordaba a él."
            ma "...Gracias por decírmelo. Ahora estamos a mano."
            $ cambiar("mariela", afecto=4, confianza=7)
        "Preguntarle por Luana":
            ma "Luana dibuja edificios. Dice que va a ser arquitecta 'para hacer oficinas donde las mamás salgan temprano'."
            "Se le quiebra la voz un segundo. Después toma limonada y se recompone."
            $ cambiar("mariela", afecto=5, confianza=5)
    "Vuelven a la oficina por separado, con diez minutos de diferencia. Idea de ella."
    $ avanzar()
    return


label ev_mar_05:
    scene expression Solid("#1a2433")
    "Sábado en la noche. El malecón de Miraflores está lleno de parejas y de vendedores de algodón de azúcar."
    "En una banca, sola, con un vestido negro y los tacos en la mano, está Mariela."
    ma "No te rías. Tuve una cita de aplicación. Llegó tarde, habló cuarenta minutos de criptomonedas y me pidió que pagara a medias el vino que pidió él."
    "Te sientas a su lado. El mar suena abajo, en la oscuridad."
    ma "¿Sabes qué es lo peor? Que me arreglé. Me pinté. Le pedí a mi mamá que se quedara con la idea de que salía con amigas."
    p "Te ves increíble. El de las criptomonedas se lo perdió."
    "Ella te mira. Largo. Como si estuviera estimando un proyecto muy riesgoso."
    ma "Esto es una pésima idea. Soy tu jefa. Tengo treinta y cuatro años, una hija y un divorcio. Y tú tienes cara de que todavía crees en las cosas."
    ma "...Y quiero hacerla igual. ¿Puedo besarte?"
    menu:
        "Decirle que sí":
            "Se besan en la banca, con el mar de fondo y los tacos de ella en el suelo."
            ma "Lunes en la oficina, nada. Ni una mirada. ¿Entendido?"
            p "Entendido, jefa."
            ma "No me digas jefa. Ahora no."
            $ R("mariela")["beso"] = True
            $ poner_estado("mariela", 2)
            $ poner_flag("mar_secreto")
            $ cambiar("mariela", afecto=6, confianza=4, atraccion=8)
        "Decirle que mejor no, por el trabajo":
            ma "...Tienes razón. Claro que tienes razón. Qué vergüenza."
            "Se pone los tacos y se va caminando hacia el Parque Kennedy. No mira atrás."
            $ cambiar("mariela", afecto=-5, confianza=4)
    return


label ev_mar_crisis:
    "Mariela te llama a la sala de reuniones pequeña. Cierra la puerta. Baja la persiana."
    ma "Jimena me preguntó, 'de manera informal', si tengo algo que declarar sobre un miembro de mi equipo."
    ma "Se está hablando de nosotros. Y si esto sale mal, la que pierde soy yo. Siempre es la mujer, y siempre es la jefa."
    menu:
        "Pedir el traslado a otro equipo y declarar la relación":
            p "Voy a hablar con Jimena. Pido el traslado al equipo de pagos y declaramos lo nuestro. Así nadie puede decir nada."
            ma "¿Harías eso? ¿Dejar el Chasqui?"
            p "El Chasqui no me abraza los sábados."
            ma "...Idiota. Ya. Hazlo."
            "Jimena los recibe con una ceja levantada y un formulario de 'declaración de vínculo'. Lo firman. El chisme pierde gracia cuando es oficial."
            $ poner_flag("mar_transfer")
            $ subir_rumor("oficina", -25)
            $ cambiar_desempeno(-3)
            $ cambiar("mariela", afecto=6, confianza=10)
        "Seguir en secreto, con más cuidado":
            ma "Más cuidado significa cero. Cero almuerzos, cero cafés, cero mensajes en horario de trabajo."
            $ subir_rumor("oficina", -10)
            $ cambiar("mariela", confianza=-5)
        "Terminar por ahora":
            ma "...Sí. Es lo más sensato. Lo sensato siempre duele, ¿no?"
            $ poner_estado("mariela", 1)
            $ cambiar("mariela", afecto=-8)
            $ subir_rumor("oficina", -15)
    return


label ev_mar_06:
    "El Sr. Benavides te llama a su oficina. Tiene los dos celulares sobre el escritorio, boca abajo, lo que significa que es serio."
    be "Joven, le tengo una propuesta. Tech lead del Chasqui. Más sueldo, más responsabilidad. Reportaría directamente a la señora Cornejo."
    "Sales de la oficina de Benavides con el corazón en la garganta. Mariela te espera en la escalera de emergencia."
    ma "Ya sé lo que te ofreció. Yo lo recomendé antes de... antes de nosotros. Y ahora no sé qué hacer."
    ma "No puedo ser tu jefa y tu pareja. Una de las dos cosas sobra."
    menu:
        "Rechazar el ascenso, pedir traslado y declarar la relación":
            call mar_final
        "Aceptar el ascenso y seguir en secreto":
            ma "No. Eso no. Ya viví una relación donde uno de los dos tenía que callarse. No otra vez."
            ma "Piénsalo. Te doy unos días."
            $ poner_flag("mar_pendiente")
            $ cambiar("mariela", confianza=-8)
    return


label ev_mar_06b:
    ma "¿Lo pensaste?"
    menu:
        "Rechazar el ascenso, pedir traslado y declarar la relación":
            $ quitar_flag("mar_pendiente")
            call mar_final
        "Decirle que no puedes renunciar al ascenso":
            ma "Entonces ya está. Felicitaciones, tech lead. Lo digo en serio. Pero lo nuestro se queda aquí."
            $ quitar_flag("mar_pendiente")
            $ poner_estado("mariela", 1)
            $ cambiar("mariela", afecto=-15, confianza=-10)
            $ cambiar_desempeno(8, "ascenso")
    return


label mar_final:
    p "Le digo a Benavides que no. Que me pasen al equipo de pagos. Y que tú y yo lo declaramos con Jimena."
    ma "¿Vas a rechazar un ascenso... por mí?"
    p "Por nosotros. Los ascensos vuelven. Esto no sé si vuelve."
    "Mariela se quita los lentes, se frota los ojos y se ríe. Una risa que nunca le habías escuchado: sin filtro, sin cuidado."
    ma "Luana va a preguntar quién eres. Le voy a decir que eres el que arregla carros con Coca-Cola."
    if not flag("mar_transfer"):
        $ poner_flag("mar_transfer")
        $ subir_rumor("oficina", -25)
    $ poner_estado("mariela", 3)
    $ cambiar("mariela", afecto=10, confianza=10, atraccion=4)
    centered "{b}Ruta de Mariela completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "mariela"
    $ escena_lugar = "oficina"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("mariela", "evento", "mar_06")
    if esc_mod:
        call expression esc_mod
    return
