## =============================================================================
## EVENTOS DE LAS PERSONAS SECUNDARIAS
## =============================================================================
## Cada una tiene un evento propio cuando ya es "principal" (la visitaste seguido)
## y le tienes algo de afecto. Después siguen con el sistema general:
## charlas, confidencias, regalos, citas, "salir en serio" y "ser pareja".
## Para alargar una ruta, agrega más eventos con registrar_evento(...).
## =============================================================================

init python:
    registrar_evento(id="fio_01", pj="fiorella", label="ev_fio_01", lugar="barranco", slots=[3], principal=True, afecto=22)
    registrar_evento(id="jim_01", pj="jimena", label="ev_jim_01", lugar="gimnasio", slots=[0], principal=True, afecto=20)
    registrar_evento(id="bre_01", pj="brenda", label="ev_bre_01", lugar="oficina", slots=[1], principal=True, afecto=22)
    registrar_evento(id="and_01", pj="andrea", label="ev_and_01", lugar="edificio", slots=[2], principal=True, afecto=22)
    registrar_evento(id="luc_01", pj="lucia", label="ev_luc_01", lugar="edificio", slots=[3], principal=True, afecto=22)
    registrar_evento(id="mil_01", pj="mila", label="ev_mil_01", lugar="gimnasio", slots=[3], principal=True, afecto=20)
    registrar_evento(id="cam_01", pj="camila", label="ev_cam_01", lugar="malecon", slots=[0, 2], principal=True, afecto=20)
    registrar_evento(id="mer_01", pj="mery", label="ev_mer_01", lugar="bodega", slots=[3], principal=True, afecto=20)
    registrar_evento(id="sof_01", pj="sofia", label="ev_sof_01", lugar="tiendas", slots=[1, 2], principal=True, afecto=20)
    registrar_evento(id="car_01", pj="carla", label="ev_car_01", lugar="barranco", slots=[3], principal=True, afecto=20)
    registrar_evento(id="pao_01", pj="paola", label="ev_pao_01", lugar="malecon", slots=[0], afecto=25)


label ev_fio_01:
    "Es noche de micrófono abierto en La Garúa. Fiorella está en la lista. Cuando dicen su nombre, se pone pálida."
    "Sube al pequeño escenario con su cuaderno. Le tiemblan las manos. Lee un poema sobre una combi que cruza la Vía Expresa al amanecer, 'como un pez fuera del agua buscando el mar'."
    "Cuando termina, hay un segundo de silencio. Después, aplausos. Los tuyos, los primeros."
    fi "¿Viniste? ¿Por mí?"
    menu:
        "Decirle qué verso te gustó más":
            p "Lo del pez buscando el mar. Así me siento yo todos los días en el micro."
            fi "...Nadie me había dicho un verso de vuelta. Gracias."
            $ cambiar("fiorella", afecto=5, confianza=7, atraccion=3)
        "Invitarle un trago para celebrar":
            "Pides dos chilcanos. Ella brinda 'por los poemas que nadie entiende'."
            $ gastar(30, "chilcanos")
            $ cambiar("fiorella", afecto=6, atraccion=4)
    return


label ev_jim_01:
    "Sábado en la mañana. En un rincón del gimnasio, alguien le pega a un saco de boxeo con una técnica impecable. Es Jimena, de Recursos Humanos, con guantes rojos."
    ji "Ah. Usted. ...Tú. Fuera de la oficina se tutea, ¿ya?"
    ji "¿Quieres probar? Tranquilo, no te voy a pegar. Mucho."
    menu:
        "Ponerte los guantes":
            "Durante diez minutos, Jimena te enseña a tirar un jab. Te corrige la guardia con una paciencia que en la oficina no muestra."
            ji "Nada mal. Para ser de sistemas."
            $ cambiar("jimena", afecto=5, confianza=4, atraccion=3)
        "Mejor sostenerle el saco":
            "Le sostienes el saco. Cada golpe te mueve medio metro. Al final se ríe, sudada y feliz."
            ji "Esto es lo mejor de mi semana. No se lo cuentes a nadie de Andina."
            $ cambiar("jimena", afecto=5, confianza=5)
    $ avanzar()
    return


label ev_bre_01:
    "Brenda se sienta a tu lado en el comedor con el celular lleno de anuncios de departamentos."
    br "¡Ayuda! Todos los depas en Lince cuestan un riñón y el otro también. Y los que son baratos tienen fotos sospechosas."
    menu:
        "Ayudarla a revisar los anuncios con ojo de ingeniero":
            "Le haces una hoja de cálculo con precio, distancia a la oficina, ruido y 'nivel de sospecha'. Ella está fascinada."
            br "¡Esto es lo más romántico que alguien ha hecho por mí! O sea, como amigo. O sea... ya."
            $ cambiar("brenda", afecto=5, confianza=6)
        "Preguntarle a Doña Gladys si hay algo libre en Los Ficus":
            "Doña Gladys dice que el 103 se libera el próximo mes, 'pero solo para gente decente'. Brenda promete ser decentísima."
            $ cambiar("brenda", afecto=6, confianza=4)
            $ poner_flag("brenda_ficus")
    return


label ev_and_01:
    "En la azotea, Andrea camina de un lado a otro entre la ropa tendida, leyendo en voz alta. Te ve y te señala con su lapicero."
    an "¡Tú! Necesito un jurado. Mañana sustento un avance de tesis y necesito practicar con alguien que no sepa nada de Derecho."
    "Durante una hora escuchas sobre la desprotección laboral de los repartidores de aplicativos. Al final, le haces una pregunta de ingeniero: cómo se calcula el pago por pedido."
    an "...Esa pregunta no me la había hecho nadie. Y es la clave. Gracias, jurado."
    $ cambiar("andrea", afecto=5, confianza=6, atraccion=2)
    return


label ev_luc_01:
    "Lucía te intercepta en la escalera con un táper y una cuchara."
    lu "Prueba. Es un tiradito nuevo, con ají amarillo y un toque de maracuyá. Si no te gusta, me mientes. Si te gusta, también."
    "Está espectacular. Se lo dices. Ella se sienta en la escalera, contenta, y te habla de su esposo, de cómo él le traía el pescado más bonito de cada madrugada."
    lu "Hace cinco años que nadie me dice que algo mío está rico así, con esa cara. Gracias, mi rey."
    $ cambiar("lucia", afecto=6, confianza=5, atraccion=2)
    return


label ev_mil_01:
    "A la hora de cierre, el gimnasio está casi vacío. Mila está frente a una barra con más discos de los que has visto juntos."
    mi "Tómame el tiempo y cuenta. Si llego a cinco, me inscribo en la competencia. Si no, me olvido del tema."
    "Uno. Dos. Tres. En el cuarto le tiembla la rodilla. Ella aprieta los dientes. Cuatro. Cinco."
    "Suelta la barra y se queda mirando el techo. Después te abraza tan fuerte que te cruje la espalda."
    mi "Me inscribo. Y tú vas. En primera fila."
    $ cambiar("mila", afecto=6, confianza=6, atraccion=3)
    return


label ev_cam_01:
    "En el malecón, Camila pelea con un trípode que el viento insiste en tumbar."
    ca "¿Me grabas? Diez tomas. Bueno, veinte. Te pago con un café."
    "Grabas veintitrés tomas. Entre toma y toma, ella revisa en el celular un Excel impecable: costos de tela, márgenes, envíos a provincia."
    ca "La gente cree que esto es posar. Esto es contabilidad con buena luz."
    $ cambiar("camila", afecto=5, confianza=5, atraccion=3)
    $ avanzar()
    return


label ev_mer_01:
    "Mery sale corriendo de la bodega con Don Teo apoyado en su hombro. El señor está pálido."
    me "¡Le subió la presión! ¡Lo llevo a la posta! ¡Vecino, cuídame la bodega una hora, por lo que más quieras!"
    "Durante una hora atiendes la bodega. Vendes pan, tres recargas, una gaseosa y le fías a una señora que jura que es 'clienta de toda la vida'."
    "Cuando vuelven, Don Teo está mejor. Mery revisa el cuaderno de ventas y se ríe hasta llorar."
    me "Le fiaste a la señora Pocha. La señora Pocha nunca paga. Pero gracias, vecino. De verdad."
    te "Joven... gracias. Usted puede venir cuando quiera. Y no le fío. Pero puede venir."
    $ cambiar("mery", afecto=6, confianza=7)
    return


label ev_sof_01:
    "En la Librería El Zorro, Sofía está con el celular en altavoz, leyendo en voz baja un capítulo de 'Los ríos profundos'."
    "Al otro lado de la línea, un señor mayor escucha en silencio. Cuando termina, él dice: 'Gracias, hijita. Hasta el domingo'."
    so "Es mi papá. Ya casi no ve. Le leo por teléfono cuando puedo."
    so "Perdón, qué escena. Estás en una librería, no en un drama."
    p "Las librerías son para los dramas."
    so "...Ja. Te voy a regalar un libro por esa frase. No me discutas."
    $ agregar_item("novela", 1)
    $ cambiar("sofia", afecto=6, confianza=6, atraccion=2)
    return


label ev_car_01:
    "Son las tres de la mañana y La Garúa está cerrando. Carla te hace una seña para que te quedes."
    cr "Te voy a hacer algo que no está en la carta. Se llama 'La Última'. Así se va a llamar mi bar, algún día."
    "Es un chilcano con pisco mosto verde, hierbaluisa y un toque de ají limo. Raro y perfecto."
    cr "Tengo ahorrado el cuarenta por ciento del local. Me falta el sesenta y el valor."
    $ cambiar("carla", afecto=6, confianza=6, atraccion=3)
    $ trasnoche = True
    return


label ev_pao_01:
    "Paola te alcanza mientras corres (o finges correr) por el malecón. Se detiene y te pide que se sienten un rato."
    pa "Necesito decirte algo, para cerrar o para abrir, no sé. Cuando te fuiste a Arequipa no me preguntaste si quería ir. Decidiste solo."
    pa "Y yo me quedé esperando que preguntaras. Cuatro años."
    menu:
        "Pedirle perdón y proponerle ser amigos":
            pa "Amigos. Ya. Eso puedo hacerlo. Creo."
            $ poner_estado("paola", 1)
            $ cambiar("paola", afecto=4, confianza=8)
        "Proponerle intentarlo otra vez, despacio":
            pa "...No sé si es buena idea. Pero esta vez lo decidimos juntos, ¿ya? Juntos."
            $ promover("paola", forzar=True)
            $ poner_estado("paola", 1)
            $ cambiar("paola", afecto=6, confianza=6, atraccion=6)
        "Decirle que es mejor no verse más":
            pa "Ya. Entiendo. Cuídate mucho. De verdad."
            "Se pone los audífonos y se va corriendo hacia Barranco. No la vuelves a ver por el malecón."
            $ poner_flag("fuera_paola")
    return
