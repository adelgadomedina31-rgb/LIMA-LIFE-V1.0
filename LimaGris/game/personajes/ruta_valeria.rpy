## =============================================================================
## RUTA DE VALERIA QUISPE (QA, Andina Data)
## =============================================================================
## val_01 El commit del console.log   -> val_02 El táper de los lunes
## val_03 Cardio con incidencias      -> amiga
## val_04 La tesis que no converge    -> val_05 Café de la Arequipa -> saliendo
## val_rumor La oficina habla          (si hay rumores mientras salen)
## val_06 La sustentación             -> pareja (fin de ruta)
## =============================================================================

init python:
    registrar_evento(id="val_01", pj="valeria", label="ev_val_01", lugar="oficina", slots=[0, 2], dia_min=2)
    registrar_evento(id="val_02", pj="valeria", label="ev_val_02", lugar="oficina", slots=[1], afecto=10, eventos=["val_01"])
    registrar_evento(id="val_03", pj="valeria", label="ev_val_03", lugar="gimnasio", slots=[3], afecto=20, eventos=["val_02"])
    registrar_evento(id="val_04", pj="valeria", label="ev_val_04", lugar="oficina", slots=[2], afecto=30, confianza=25, eventos=["val_03"])
    registrar_evento(id="val_05", pj="valeria", label="ev_val_05", lugar="tiendas", slots=[2], dias_semana=[5], afecto=35, atraccion=28, flags=["val_ayuda"])
    registrar_evento(id="val_rumor", pj="valeria", label="ev_val_rumor", lugar="oficina", estado=2,
                     cond=lambda: rumores["oficina"] >= 40, prioridad=20)
    registrar_evento(id="val_06", pj="valeria", label="ev_val_06", lugar="oficina", slots=[2], dias_semana=[4],
                     estado=2, afecto=70, confianza=60, citas=3, eventos=["val_05"])


label ev_val_01:
    "Abres el repositorio y ves una notificación roja: tu primer pull request fue rechazado."
    "Comentario de Valeria Quispe: 'Rompe 3 pruebas. Tiene un console.log. Y el nombre de la variable \"cosa2\" es un crimen'."
    "Te das la vuelta. Ella está a dos escritorios, con los audífonos puestos, fingiendo que no te ve."
    menu:
        "Ir a defender tu código":
            p "Las pruebas que fallan ya fallaban antes. No es mi culpa."
            va "Puede ser. Pero las tocaste y no las arreglaste. Eso sí es tu culpa."
            "Lo peor es que tiene razón."
            $ cambiar("valeria", afecto=1, confianza=2)
        "Aceptar el comentario y arreglarlo":
            "Arreglas las tres pruebas, borras el console.log y renombras 'cosa2' a 'saldoPendiente'. Vuelves a mandar el PR."
            "A los diez minutos: 'Aprobado. Así sí, ingeniero'. Y un emoji de pulgar arriba. Uno solo. Pero arriba."
            $ cambiar("valeria", afecto=4, confianza=2)
            $ cambiar_desempeno(1)
        "Hacerle una broma":
            p "¿'cosa2' es un crimen? Deberías ver 'cosa1'."
            va "...No me hagas reír, que estoy en modo profesional."
            "Pero se ríe. Bajito, tapándose la boca con la manga del polerón."
            $ cambiar("valeria", afecto=3, atraccion=2)
    return


label ev_val_02:
    "Al mediodía, el comedor de Andina Data huele a microondas. Valeria está sola en una esquina, con un táper enorme."
    va "Ven, siéntate. Mi mamá me manda comida para tres. Cree que en San Isidro no hay comida."
    "Son tallarines verdes con papa a la huancaína. Son, probablemente, los mejores tallarines verdes de tu vida."
    va "Ella vende emoliente en Comas. Desde hace veinte años, en la misma esquina. Todo el barrio la conoce como 'la señora Rosa del emoliente'."
    p "¿Y tú la ayudabas?"
    va "Desde los ocho años. Yo contaba el sencillo. Por eso soy QA: no se me escapa ni un céntimo."
    menu:
        "Preguntarle por su papá":
            va "Mi papá manejaba combi. Comas-Centro. Él quería que yo fuera ingeniera, como tú."
            va "...Ya no está. Pero se hubiera reído de ver que terminé corrigiendo a los ingenieros."
            $ cambiar("valeria", afecto=3, confianza=4)
        "Contarle de tu familia en Arequipa":
            p "Mi mamá vive en Arequipa con mi hermana. Mi papá murió hace dos años. Por eso me fui allá un tiempo."
            va "...Lo siento. No sabía."
            "Se queda callada un momento. Después te sirve más tallarines sin preguntar."
            $ cambiar("valeria", afecto=4, confianza=3)
        "Pedirle la receta para tu tía":
            va "La receta es secreta. Mi mamá me la va a dejar en el testamento. Literal."
            $ cambiar("valeria", afecto=3, atraccion=1)
    return


label ev_val_03:
    "En el gimnasio, entre reguetón y pesas, ves a alguien peleando con una caminadora como si le debiera plata."
    "Es Valeria. Roja, sudada, con los audífonos gigantes y una cara de odio puro."
    va "No. Me. Mires."
    p "No te estoy mirando."
    va "Me estás mirando. Estoy haciéndole QA a mi cardio y está fallando todas las pruebas."
    "Se baja de la máquina, toma agua y se ríe de sí misma."
    va "Mi doctora me dijo que tengo que hacer ejercicio. Que tanto estrés me va a matar a los cuarenta. Así que aquí estoy. Muriendo a los veintinueve."
    menu:
        "Ofrecerte a entrenar con ella los martes y jueves":
            va "¿En serio? ...Ya. Pero si me ves llorar en la bicicleta, no dices nada."
            $ cambiar("valeria", afecto=4, confianza=3, atraccion=2)
        "Decirle que se ve bien igual":
            va "...Gracias. Creo. Ya, cállate, me vas a hacer perder el ritmo."
            $ cambiar("valeria", afecto=2, atraccion=4)
        "Retarla a una carrera en las caminadoras":
            "Le ganas por poco. Ella exige revancha. Pierdes la revancha a propósito y ella lo sabe."
            va "Me dejaste ganar. Te voy a reportar por fraude."
            $ cambiar("valeria", afecto=4, atraccion=2)
    if R("valeria")["estado"] < 1:
        $ poner_estado("valeria", 1)
    return


label ev_val_04:
    "A las cinco de la tarde, Valeria tiene la cabeza apoyada en el teclado. En su pantalla hay un gráfico que parece un electrocardiograma de alguien muy enfermo."
    p "¿Todo bien?"
    va "Mi modelo de la tesis no converge. Llevo dos semanas. Mi asesor me dijo que 'revise los hiperparámetros'. Gracias, maestro, qué aporte."
    va "Es un modelo para predecir qué socios de la cooperativa van a dejar de pagar. Si funciona, la cooperativa podría ayudarlos antes, en vez de embargarlos."
    "La miras. Por primera vez la ves cansada de verdad."
    menu:
        "Ofrecerte a revisarlo con ella el sábado":
            va "¿Harías eso? ...Los sábados en la tarde trabajo en el café de la Av. Arequipa, al lado de la librería. Llevo mi laptop."
            va "Pero no es una cita, ¿ah? Es una sesión de debugging."
            p "Obvio. Debugging."
            $ poner_flag("val_ayuda")
            $ cambiar("valeria", afecto=4, confianza=5)
        "Darle una idea rápida ahí mismo":
            p "¿Normalizaste las variables? Los montos de los préstamos van de cien a cien mil soles."
            "Se queda mirando la pantalla. Escribe dos líneas. El gráfico se calma un poco."
            va "...Te odio. Bueno, no. Pero un poquito. ¿Me ayudas el sábado? Estoy en el café de la Arequipa en la tarde."
            $ poner_flag("val_ayuda")
            $ cambiar("valeria", afecto=3, confianza=4, atraccion=2)
    return


label ev_val_05:
    scene expression Solid("#2a2219")
    "El café de la Arequipa huele a pan de plátano. Valeria está en la mesa del fondo, con lentes, el pelo amarrado con un lapicero y tres tazas vacías."
    va "Llegaste. Pensé que te ibas a corretear."
    "Durante dos horas revisan su código. Encuentras un error en la división de los datos de entrenamiento. Ella encuentra tres en tu forma de explicar."
    "A las seis, el modelo converge. La curva baja limpia, como una pista de aterrizaje."
    va "¡Funciona! ¡FUNCIONA!"
    "Se para de golpe y te abraza. Después se da cuenta de que te está abrazando. No te suelta."
    va "...Oye."
    p "Dime."
    va "Me gustas. Ya. Lo dije. No me mires así, que tengo cero preparación para esto."
    va "Pero me da miedo. En mi chamba anterior salí con alguien de la oficina y terminé renunciando. No quiero ser 'la flaca del ingeniero nuevo'."
    menu:
        "Proponerle salir, con calma y sin que se entere nadie en la oficina":
            p "Entonces lo hacemos a nuestra manera. Despacio. Y en la oficina somos 'muy profesionales'."
            va "...¿Me lo prometes?"
            p "Te lo prometo."
            "Te pregunta con la mirada. Asientes. Se besan entre tazas vacías y un modelo que por fin funciona."
            $ poner_estado("valeria", 2)
            $ R("valeria")["beso"] = True
            $ cambiar("valeria", afecto=6, confianza=6, atraccion=5)
        "Decirle que tú también, pero que vayan paso a paso":
            p "A mí también me gustas. Y no tengo apuro. Vamos viendo."
            va "Vamos viendo. Me gusta. Suena a sprint sin fecha de entrega."
            "Ella misma te da un beso rápido en la mejilla y se pone roja hasta las orejas."
            $ poner_estado("valeria", 2)
            $ cambiar("valeria", afecto=5, confianza=7, atraccion=3)
    $ escena_personaje = "valeria"
    $ escena_lugar = "cafe"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("valeria", "evento", "val_05")
    if esc_mod:
        call expression esc_mod
    $ avanzar()
    return


label ev_val_rumor:
    "Valeria pasa a tu lado sin mirarte. Cinco minutos después te llega un mensaje: 'Escalera de emergencia. Ahora.'"
    va "Kathy me preguntó, delante de todos, si tú y yo 'ya oficializamos'. Brenda se rió. Hasta Piero puso cara."
    va "Te lo dije. Te dije que esto me daba miedo."
    menu:
        "Hablar tú con Kathy para que pare el chisme":
            "Le pides a Kathy, con la mejor cara que tienes, que por favor deje el tema. Ella levanta las manos: 'Yo no dije nada'. Pero entiende."
            $ subir_rumor("oficina", -20)
            $ cambiar("valeria", confianza=4)
            $ cambiar("kathy", afecto=-2)
            va "...Gracias. Eso no lo hubiera hecho cualquiera."
        "Proponerle contarlo abiertamente":
            if R("valeria")["confianza"] >= 60:
                va "...¿Sabes qué? Ya. Que hablen. Pero que hablen con información correcta."
                "Al día siguiente almuerzan juntos en el comedor, a la vista de todos. Kathy aplaude. Valeria le tira una servilleta."
                $ poner_flag("val_publico")
                $ subir_rumor("oficina", -30)
                $ cambiar("valeria", afecto=5, confianza=5)
            else:
                va "Todavía no. No estoy lista. Lo siento."
                $ cambiar("valeria", confianza=-3)
        "Tomar más distancia en la oficina":
            p "Tienes razón. En la oficina, distancia total."
            va "Gracias. Aunque me va a costar no mirarte en las dailies."
            $ subir_rumor("oficina", -15)
            $ cambiar("valeria", afecto=-2, confianza=3)
    return


label ev_val_06:
    "Es viernes. Valeria aparece en tu escritorio con un blazer prestado y la cara blanca como una hoja de requerimientos."
    va "Hoy sustento la tesis. A las seis. En San Marcos. Tengo ganas de vomitar."
    va "No tienes que venir. O sea... sí tienes que venir. Si quieres."
    "Terminas tu ticket a toda velocidad, le avisas a Mariela y tomas un taxi a la Ciudad Universitaria."
    $ trabajo_hoy[2] = True
    scene expression Solid("#1d1d2a")
    "El auditorio es viejo y huele a madera. En la primera fila está una señora bajita con una chompa tejida: la señora Rosa, la del emoliente. Tiene un ramo de girasoles en las manos."
    "Valeria habla cuarenta minutos sin mirar sus notas. Cuando el jurado pregunta algo difícil, ella sonríe. Esa sonrisa la conoces: es la de 'encontré el bug'."
    "Aprobada. Con mención."
    "La señora Rosa llora. Valeria llora. Tú también, un poco, aunque dices que es la alergia."
    va "Mamá, él es... él es [nombre]."
    "Señora Rosa" "Ah, el ingeniero. Mi hija me habla de usted. Bueno, no me habla, pero se le nota. Venga, que le invito un emoliente."
    "Después, en la puerta del auditorio, Valeria te jala de la mano."
    va "Oye. Ya no quiero 'ir viendo'. Ya vi. Quiero que seamos algo de verdad. Con nombre y todo."
    menu:
        "Decirle que sí, que quieres ser su pareja":
            p "Sí. Con nombre y todo."
            va "Ya. Entonces... mi enamorado. Qué raro suena. Me gusta."
            $ poner_estado("valeria", 3)
            $ cambiar("valeria", afecto=10, confianza=10, atraccion=5)
            $ subir_rumor("oficina", -10)
    centered "{b}Ruta de Valeria completada{/b}\n\nLa historia sigue: Lima no se detiene."
    $ escena_personaje = "valeria"
    $ escena_lugar = "universidad"
    $ escena_punto = "evento"
    $ esc_mod = modulo_buscar_escena("valeria", "evento", "val_06")
    if esc_mod:
        call expression esc_mod
    $ ubicacion = "casa"
    $ slot = 3
    "Celebran con pollo a la brasa en Pueblo Libre: ella, su mamá, su roomie Dayana y tú. Llegas a Lince de noche, con olor a papas fritas y una sonrisa idiota."
    if puede_intimidad("valeria"):
        va "Oye... ¿y si la noche no termina todavía?"
        call intimidad("valeria", "cita")
        if _return:
            return
    $ necesita_dormir = True
    return
