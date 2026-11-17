## =============================================================================
## LIMA GRIS - Funciones del núcleo
## =============================================================================
## Tiempo, dinero, relaciones, horarios, eventos, rumores, citas e intimidad.
## Los textos de historia están en personajes/ y en nucleo/5x-8x.
## =============================================================================

init -15 python:

    ## Registro de eventos (cada archivo de personaje agrega los suyos)
    EVENTOS = []

    def registrar_evento(**kw):
        kw.setdefault("prioridad", 50)
        EVENTOS.append(kw)
        EVENTOS.sort(key=lambda e: e["prioridad"])

    ## Ayuda para escribir horarios.
    ## lv = lunes a viernes, sab = sábado, dom = domingo.
    ## También se puede pasar un día puntual: d0=[...] (lunes) ... d6=[...]
    def H(lv=None, sab=None, dom=None, **dias):
        vacio = [None, None, None, None]
        h = {}
        for d in range(5):
            h[d] = list(lv or vacio)
        h[5] = list(sab or vacio)
        h[6] = list(dom or vacio)
        for k, v in dias.items():
            h[int(k[1:])] = list(v)
        return h


init -10 python:

    import time as _time

    ## ------------------------------------------------------------ Avisos
    AVISOS = []

    def aviso(msg):
        AVISOS.append([msg, _time.time()])
        del AVISOS[:-5]
        renpy.restart_interaction()

    def limpiar_avisos():
        ahora = _time.time()
        cambio = False
        while AVISOS and ahora - AVISOS[0][1] > 4.5:
            AVISOS.pop(0)
            cambio = True
        if cambio:
            renpy.restart_interaction()

    ## ------------------------------------------------------------ Tiempo
    def fecha(d=None):
        if d is None:
            d = store.dia
        offset = DIA_MES_INICIO - 1 + (d - 1)
        m = MES_INICIO
        while offset >= MESES[m][1]:
            offset -= MESES[m][1]
            m = (m + 1) % 12
        return offset + 1, m

    def dia_mes(d=None):
        return fecha(d)[0]

    def es_fin_de_mes(d=None):
        dm, m = fecha(d)
        return dm == MESES[m][1]

    def dow(d=None):
        if d is None:
            d = store.dia
        return (d - 1) % 7

    def texto_fecha(d=None):
        if d is None:
            d = store.dia
        dm, m = fecha(d)
        return "%s %d de %s" % (DIAS_SEMANA[dow(d)], dm, MESES[m][0])

    def texto_fecha_corta(d, s=None):
        dm, m = fecha(d)
        t = "%s %d/%02d" % (DIAS_SEMANA[dow(d)][:3], dm, m + 1)
        if s is not None:
            t += " · " + SLOTS[s].lower()
        return t

    def es_laborable(d=None):
        return dow(d) < 5

    def oficina_de_noche(d=None):
        if d is None:
            d = store.dia
        return dow(d) == 3 or ("oficina_noche_%d" % d) in store.flags

    def lugar_abierto(lid, s=None, d=None):
        if s is None:
            s = store.slot
        if d is None:
            d = store.dia
        L = LUGARES[lid]
        w = dow(d)
        if lid == "oficina":
            if w < 5 and s in (0, 1, 2):
                return True
            return s == 3 and oficina_de_noche(d)
        if lid == "gimnasio" and w == 6:
            return s == 0
        return (w in L["dias"]) and (s in L["abierto"])

    def es_horario_laboral(s=None, d=None):
        if s is None:
            s = store.slot
        return es_laborable(d) and s in (0, 2)

    def texto_hora():
        return "%s · %s" % (SLOTS[store.slot], SLOT_HORA[store.slot])

    ## ------------------------------------------------------------ Dinero
    def soles(x):
        signo = "-" if x < 0 else ""
        return "%sS/ %s" % (signo, "{:,.2f}".format(abs(x)))

    def gastar(monto, motivo="", silencioso=False):
        store.dinero = round(store.dinero - monto, 2)
        store.historial_gastos.append((store.dia, -monto, motivo))
        del store.historial_gastos[:-40]
        if not silencioso and monto:
            aviso("%s  %s" % (soles(-monto), motivo))

    def ganar(monto, motivo="", silencioso=False):
        store.dinero = round(store.dinero + monto, 2)
        store.historial_gastos.append((store.dia, monto, motivo))
        del store.historial_gastos[:-40]
        if not silencioso and monto:
            aviso("+%s  %s" % (soles(monto), motivo))

    def puede_pagar(monto):
        return store.dinero >= monto

    def costo_viaje(destino, s=None):
        if s is None:
            s = store.slot
        z1 = LUGARES[store.ubicacion]["zona"]
        z2 = LUGARES[destino]["zona"] if destino in LUGARES else destino
        if z1 == z2:
            return 0.0
        lejos = z2 if z2 != "Lince" else z1
        modo = "taxi" if s == 3 else "micro"
        return ZONAS[lejos][modo]

    def costo_zona(zona, s=None):
        if s is None:
            s = store.slot
        z1 = LUGARES[store.ubicacion]["zona"]
        if z1 == zona:
            return 0.0
        lejos = zona if zona != "Lince" else z1
        info = ZONAS.get(lejos, {"micro": 3.0, "taxi": 18.0})
        return info["taxi" if s == 3 else "micro"]

    def cambiar_energia(n):
        store.energia = max(0, min(100, store.energia + n))

    def cambiar_desempeno(n, motivo=""):
        store.desempeno = max(0, min(100, store.desempeno + n))
        if motivo:
            aviso("Desempeño %+d  %s" % (n, motivo))

    def cambiar_forma(n):
        store.forma = max(0, min(100, store.forma + n))

    ## ---------------------------------------------------------- Flags
    def flag(f):
        return f in store.flags

    def poner_flag(f):
        if f not in store.flags:
            store.flags.append(f)

    def quitar_flag(f):
        while f in store.flags:
            store.flags.remove(f)

    def visto(ev_id):
        return ev_id in store.eventos_vistos

    ## ------------------------------------------------------- Relaciones
    def nuevo_rel(pj):
        datos = PJ[pj]
        return dict(
            afecto=datos.get("inicio", {}).get("afecto", 0),
            confianza=datos.get("inicio", {}).get("confianza", 0),
            atraccion=datos.get("inicio", {}).get("atraccion", 0),
            estado=0,
            tipo=datos.get("tipo", "secundario"),
            conocida=False,
            visitas=0, ult_visita=-1,
            ult_charla=-1, ult_coqueteo=-1, ult_regalo=-1, ult_confidencia=-1,
            confidencias=0, charla_idx=0,
            citas=0, noches=0, ult_noche=-1, beso=False,
            numero=False, horario=False,
            gustos_vistos=[], chisme_idx=0, dia_estado=0,
            flags=[],
        )

    def asegurar_rel():
        for pj in PJ:
            if pj not in store.rel:
                store.rel[pj] = nuevo_rel(pj)
            else:
                base = nuevo_rel(pj)
                for k, v in base.items():
                    if k not in store.rel[pj]:
                        store.rel[pj][k] = v

    def R(pj):
        if pj not in store.rel:
            store.rel[pj] = nuevo_rel(pj)
        return store.rel[pj]

    def nom(pj):
        return PJ[pj]["nombre"]

    def ch(pj):
        return getattr(store, PJ[pj]["var"])

    def es_romance(pj):
        return PJ[pj].get("tipo") != "npc"

    def cambiar(pj, afecto=0, confianza=0, atraccion=0, aviso_=True):
        r = R(pj)
        partes = []
        for k, v, etiqueta in (("afecto", afecto, "afecto"), ("confianza", confianza, "confianza"), ("atraccion", atraccion, "atracción")):
            if v:
                r[k] = max(0, min(100, r[k] + v))
                partes.append("%s %+d" % (etiqueta, v))
        if aviso_ and partes and es_romance(pj):
            aviso("%s: %s" % (PJ[pj]["corto"], ", ".join(partes)))
        revisar_progreso(pj)

    def poner_estado(pj, e, aviso_=True):
        r = R(pj)
        if r["estado"] == e:
            return
        sube = e > r["estado"]
        r["estado"] = e
        r["dia_estado"] = store.dia
        if e >= 2:
            r["chisme_idx"] = len(store.chismes)
        if aviso_:
            if sube:
                textos = {1: "%s ahora te considera su amigo.", 2: "Estás saliendo con %s.", 3: "%s y tú son pareja."}
                aviso(textos.get(e, "%s") % nom(pj))
            else:
                aviso("Tu relación con %s se enfrió (%s)." % (nom(pj), ESTADOS[e]))

    def revisar_progreso(pj):
        r = R(pj)
        if not es_romance(pj):
            return
        if not r["numero"] and r["confianza"] >= UMBRAL_NUMERO:
            r["numero"] = True
            aviso("Ahora tienes el WhatsApp de %s." % nom(pj))
        if r["estado"] == 0:
            ruta = PJ[pj].get("ruta", False)
            if (not ruta and r["afecto"] >= 30 and r["confianza"] >= 25) or (r["afecto"] >= 40 and r["confianza"] >= 35):
                poner_estado(pj, 1)

    def registrar_visita(pj):
        r = R(pj)
        if r["ult_visita"] != store.dia:
            r["visitas"] += 1
            r["ult_visita"] = store.dia
        if r["visitas"] >= UMBRAL_HORARIO and not r["horario"]:
            r["horario"] = True
        promover(pj)

    def promover(pj, forzar=False):
        r = R(pj)
        if r["tipo"] != "secundario":
            return False
        if forzar or (r["visitas"] >= UMBRAL_PRINCIPAL_VISITAS and r["afecto"] >= UMBRAL_PRINCIPAL_AFECTO):
            r["tipo"] = "principal"
            aviso("%s ahora es parte importante de tu historia." % nom(pj))
            return True
        return False

    def es_principal(pj):
        return R(pj)["tipo"] == "principal"

    def puede_invitar(pj):
        r = R(pj)
        return es_romance(pj) and es_principal(pj) and r["afecto"] >= 25 and r["confianza"] >= 15 and not cita_con(pj)

    def puede_intimidad(pj):
        r = R(pj)
        return (es_romance(pj) and r["estado"] >= 2 and r["afecto"] >= 55 and r["confianza"] >= 45
                and r["atraccion"] >= 55 and r["ult_noche"] != store.dia)

    def corazones(pj):
        a = R(pj)["afecto"]
        llenos = int(a / 20)
        return "♥" * llenos + "♡" * (5 - llenos)

    ## --------------------------------------------------------- Horarios
    def ubic_pj(pj, d=None, s=None):
        if d is None:
            d = store.dia
        if s is None:
            s = store.slot
        clave = "%d-%d-%s" % (d, s, pj)
        if clave in store.presencias:
            return store.presencias[clave]
        datos = PJ[pj]
        if d < datos.get("aparece_dia", 1):
            return None
        if ("fuera_" + pj) in store.flags:
            return None
        f = datos.get("horario_func")
        if f:
            fila = f(d)
        else:
            fila = datos["horario"].get(dow(d))
        if not fila:
            return None
        loc = fila[s]
        if loc and loc in LUGARES and not lugar_abierto(loc, s, d):
            return None
        return loc

    def gente_aqui(lugar=None, d=None, s=None):
        if lugar is None:
            lugar = store.ubicacion
        return [pj for pj in ORDEN_PJ if ubic_pj(pj, d, s) == lugar]

    def texto_horario(pj):
        """Devuelve una lista de líneas con el horario conocido del personaje."""
        datos = PJ[pj]
        lineas = []
        for w in range(7):
            d = w + 1  ## semana 1 de ejemplo
            partes = []
            for s in range(4):
                if datos.get("horario_func"):
                    fila = datos["horario_func"](d)
                else:
                    fila = datos["horario"].get(w)
                loc = fila[s] if fila else None
                if loc and loc in LUGARES:
                    partes.append("%s: %s" % (SLOTS[s], LUGARES[loc]["nombre"]))
            lineas.append("%s — %s" % (DIAS_SEMANA[w], "; ".join(partes) if partes else "no se le ve por tu zona"))
        return lineas

    ## ----------------------------------------------------------- Eventos
    def evento_por_id(eid):
        for ev in EVENTOS:
            if ev["id"] == eid:
                return ev
        return None

    def evento_cumple(ev):
        if ev["id"] in store.eventos_vistos and not ev.get("repetible"):
            return False
        lug = ev.get("lugar")
        if lug:
            if isinstance(lug, str):
                lug = [lug]
            if store.ubicacion not in lug:
                return False
        if "slots" in ev and store.slot not in ev["slots"]:
            return False
        if "dias_semana" in ev and dow() not in ev["dias_semana"]:
            return False
        if "dia" in ev and store.dia != ev["dia"]:
            return False
        if store.dia < ev.get("dia_min", 1):
            return False
        pj = ev.get("pj")
        if pj:
            if ev.get("presente", True) and ubic_pj(pj) != store.ubicacion:
                return False
            r = R(pj)
            if ev.get("principal") and r["tipo"] != "principal":
                return False
            for k in ("afecto", "confianza", "atraccion", "citas"):
                if r[k] < ev.get(k, 0):
                    return False
            if r["estado"] < ev.get("estado", 0):
                return False
            if r["estado"] > ev.get("estado_max", 9):
                return False
        for e in ev.get("eventos", []):
            if e not in store.eventos_vistos:
                return False
        for f in ev.get("flags", []):
            if f not in store.flags:
                return False
        for f in ev.get("sin_flags", []):
            if f in store.flags:
                return False
        cond = ev.get("cond")
        if cond is not None and not cond():
            return False
        return True

    def buscar_evento():
        marca = (store.dia, store.slot, store.ubicacion)
        if store.ev_marca == marca:
            return None
        for ev in EVENTOS:
            if evento_cumple(ev):
                return ev["id"]
        return None

    def marcar_evento(eid):
        if eid not in store.eventos_vistos:
            store.eventos_vistos.append(eid)
        ev = evento_por_id(eid)
        if ev and ev.get("pj"):
            R(ev["pj"])["conocida"] = True
            if ev.get("presente", True):
                registrar_visita(ev["pj"])
        if not (ev and ev.get("no_cuenta")):
            store.ev_marca = (store.dia, store.slot, store.ubicacion)

    ## ------------------------------------------------- Rumores y chismes
    def subir_rumor(circulo, n):
        if not circulo:
            return
        store.rumores[circulo] = max(0, min(100, store.rumores.get(circulo, 0) + n))

    def agregar_chisme(pj, circulo, testigo=None, n=10):
        store.chismes.append(dict(pj=pj, circulo=circulo, testigo=testigo, dia=store.dia))
        subir_rumor(circulo, n)

    def chisme_para(pj):
        """Un chisme sobre otra persona que molestaría a 'pj' (si están saliendo)."""
        r = R(pj)
        if r["estado"] < 2:
            return None
        circ = PJ[pj].get("circulo")
        for i in range(r["chisme_idx"], len(store.chismes)):
            c = store.chismes[i]
            if c["pj"] == pj:
                continue
            if c["circulo"] == circ or c.get("testigo") == pj:
                return i
        return None

    def testigos_en(lugar, s, excluir):
        """Personas que conoces que estarían en ese lugar a esa hora."""
        res = []
        if lugar == "cevicheria":
            if R("lucia")["conocida"] and "lucia" != excluir and dow() != 6:
                res.append("lucia")
            return res
        if not lugar:
            return res
        for pj in gente_aqui(lugar, store.dia, s):
            if pj != excluir and R(pj)["conocida"]:
                res.append(pj)
        return res

    ## ----------------------------------------------------- Citas agendadas
    def cita_con(pj):
        for c in store.citas_agendadas:
            if c["pj"] == pj:
                return c
        return None

    def cita_ahora():
        for c in store.citas_agendadas:
            if c["dia"] == store.dia and c["slot"] == store.slot:
                return c
        return None

    def disponible_cita(pj, d, s):
        datos = PJ[pj]
        if es_horario_laboral(s, d):
            return False
        if (dow(d), s) in datos.get("bloqueado", []):
            return False
        loc = ubic_pj(pj, d, s)
        if loc in datos.get("ocupado", []):
            return False
        for c in store.citas_agendadas:
            if c["dia"] == d and c["slot"] == s:
                return False
        return True

    def opciones_agenda(pj, lugar_cita, maximo=5):
        res = []
        info = CITAS[lugar_cita]
        d, s = store.dia, store.slot + 1
        while len(res) < maximo and d < store.dia + 8:
            if s > 3:
                d += 1
                s = 0
                continue
            if s in info["slots"] and disponible_cita(pj, d, s):
                res.append((d, s))
            s += 1
        return res

    def agendar_cita(pj, lugar_cita, d, s):
        store.citas_agendadas.append(dict(pj=pj, lugar=lugar_cita, dia=d, slot=s))
        aviso("Cita con %s: %s" % (nom(pj), texto_fecha_corta(d, s)))

    def quitar_cita(c):
        if c in store.citas_agendadas:
            store.citas_agendadas.remove(c)

    ## ------------------------------------------------------- Inventario
    def tiene_item(i):
        return store.inventario.get(i, 0) > 0

    def agregar_item(i, n=1):
        store.inventario[i] = store.inventario.get(i, 0) + n

    def quitar_item(i, n=1):
        store.inventario[i] = store.inventario.get(i, 0) - n
        if store.inventario[i] <= 0:
            del store.inventario[i]

    def comprar(i):
        it = ITEMS[i]
        if not puede_pagar(it["precio"]):
            aviso("No te alcanza la plata.")
            return
        gastar(it["precio"], it["nombre"])
        agregar_item(i)

    def usar_item(i):
        it = ITEMS[i]
        if it.get("energia"):
            cambiar_energia(it["energia"])
            aviso("Energía +%d" % it["energia"])
        quitar_item(i)

    def regalos_en_mochila():
        return [i for i in sorted(store.inventario) if ITEMS[i]["cat"] in CATEGORIAS_REGALO]

    def items_tienda(lugar):
        return [i for i in ITEMS if lugar in ITEMS[i]["tiendas"]]

    ## -------------------------------------------------------- Freelance
    def generar_ofertas():
        if store.freelance_ofertas_dia == store.dia:
            return store.freelance_ofertas
        rnd = random.Random(store.dia * 7919 + 17)
        idx = rnd.sample(range(len(FREELANCE_OFERTAS)), 3)
        res = []
        for i in idx:
            t, ses, pago = FREELANCE_OFERTAS[i]
            pago = pago * (1.0 + 0.05 * min(store.rep_freelance, 6))
            res.append(dict(titulo=t, sesiones=ses, pago=round(pago), plazo=store.dia + ses * 2 + 2))
        store.freelance_ofertas = res
        store.freelance_ofertas_dia = store.dia
        return res

    ## --------------------------------------------------------- Módulo
    def modulo_stats_de(pj):
        ms = getattr(store, "modulo_stats", None) or {}
        return ms.get(pj, {})

    def stat_modulo(pj, stat, cantidad=1):
        f = getattr(store, "sumar_stat", None)
        if f:
            f(pj, stat, cantidad)

    def _cumple_valor(req, clave, valor):
        if clave not in req:
            return True
        esperado = req[clave]
        if isinstance(esperado, (list, tuple)):
            return valor in esperado
        return valor == esperado

    def modulo_req_ok(req, pj, punto, lugar):
        r = R(pj) if pj in PJ else None
        if req.get("punto", "intimidad") != punto:
            return False
        if not _cumple_valor(req, "lugar", lugar):
            return False
        if r:
            for k in ("afecto", "confianza", "atraccion"):
                if r[k] < req.get(k, 0):
                    return False
            if "estado" in req:
                est = req["estado"]
                if isinstance(est, str):
                    est = [e.lower() for e in ESTADOS].index(est.lower())
                if r["estado"] < est:
                    return False
            if r["noches"] < req.get("veces_min", 0):
                return False
            if r["noches"] > req.get("veces_max", 9999):
                return False
            if r["citas"] < req.get("citas_min", 0):
                return False
        if store.dia < req.get("dia_min", 1):
            return False
        if not _cumple_valor(req, "slot", store.slot):
            return False
        f = req.get("flag")
        if f and f not in store.flags:
            return False
        ev = req.get("evento")
        if ev and ev not in store.eventos_vistos:
            return False
        ms = req.get("stats")
        if ms:
            mis = modulo_stats_de(pj)
            for k, v in ms.items():
                if mis.get(k, 0) < v:
                    return False
        return True

    def modulo_buscar_escena(pj, punto="intimidad", lugar=None):
        conns = getattr(store, "modulo_conexiones", None) or []
        for c in conns:
            quien = c.get("personaje")
            if quien not in (pj, "*", "todas", None):
                continue
            if not modulo_req_ok(c.get("requisitos", {}) or {}, pj, punto, lugar):
                continue
            lbl = c.get("escena")
            if lbl and renpy.has_label(lbl):
                return lbl
        return None

    ## -------------------------------------------------------- Intimidad
    NOMBRE_LUGAR_INTIMO = {
        "depa_tuyo": "tu depa",
        "depa_ella": "su depa",
        "hostal": "un hostal en Lince",
        "hotel": "un hotel en Miraflores",
        "oficina": "la oficina",
        "azotea": "la azotea del edificio",
        "callejon": "un callejón oscuro",
        "carro": "su carro",
        "almacen": "el almacén del Tambo",
        "vestidor": "los vestidores del gimnasio",
        "trastienda": "la trastienda de la bodega",
    }

    PREFERENCIA_LUGAR_BASE = {
        "depa_tuyo": 1, "depa_ella": 1, "hostal": 1, "hotel": 1,
        "oficina": -1, "azotea": 0, "callejon": -1, "carro": 0,
        "almacen": -1, "vestidor": -1, "trastienda": -1,
    }

    def pref_lugar(pj, lid):
        return PJ[pj].get("lugares", {}).get(lid, PREFERENCIA_LUGAR_BASE.get(lid, 0))

    def casa_ella_posible(pj):
        """(posible, motivo_si_no)"""
        tipo = PJ[pj].get("vivienda", "sola")
        w = dow()
        if tipo in ("familia", "padres"):
            return False, "familia"
        if tipo == "hermana" and w not in (1, 3):
            return False, "hermana"
        if tipo == "hija" and w not in (4, 5):
            return False, "hija"
        return True, None

    def opciones_lugar_intimo(pj):
        """Lista de (id, texto, costo) según dónde están y con quién."""
        u = store.ubicacion
        s = store.slot
        circ = PJ[pj].get("circulo")
        ops = []
        taxi_lince = costo_zona("Lince", 3)
        ops.append(("depa_tuyo", "Ir a tu depa en Lince", taxi_lince))
        if PJ[pj].get("vivienda") == "vecina":
            ops.append(("depa_ella", "Ir a su depa, en tu mismo edificio", costo_zona("Lince", 3)))
        else:
            z = PJ[pj].get("zona_casa", "Lince")
            ops.append(("depa_ella", "Ir a su casa (%s)" % z, costo_zona(z, 3)))
        ops.append(("hostal", "Un hostal discreto en Lince", 70.0 + taxi_lince))
        ops.append(("hotel", "Un hotel bonito en Miraflores", 220.0 + costo_zona("Miraflores", 3)))
        if u == "oficina" and circ == "oficina":
            ops.append(("oficina", "Quedarse en la oficina vacía", 0.0))
        if u in ("edificio", "casa") and circ == "edificio" and s == 3:
            ops.append(("azotea", "Subir a la azotea del edificio", 0.0))
        if u in ("barranco", "malecon") and s == 3:
            ops.append(("callejon", "Un callejón oscuro a la vuelta", 0.0))
        if PJ[pj].get("carro") and u not in ("casa", "edificio"):
            ops.append(("carro", "En su carro, estacionados en un lugar apartado", 0.0))
        if u == "tambo" and pj == "dani":
            ops.append(("almacen", "El almacén del Tambo, a la hora del cierre de caja", 0.0))
        if u == "gimnasio" and circ == "gimnasio" and s == 3:
            ops.append(("vestidor", "Los vestidores, a la hora de cierre", 0.0))
        if u == "bodega" and pj == "mery" and s == 3:
            ops.append(("trastienda", "La trastienda de la bodega, con la reja ya bajada", 0.0))
        return ops


init 5 python:
    ## Revisa partidas viejas al cargar: si se agregó un personaje nuevo, lo crea.
    def _al_cargar():
        asegurar_rel()
    config.after_load_callbacks.append(_al_cargar)
