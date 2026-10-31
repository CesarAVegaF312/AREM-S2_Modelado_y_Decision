"""Simulador de HIS-CORE, el sistema de informacion hospitalaria del caso.

No es un HIS: solo reproduce lo que importa para la costura con AGENDA-WEB.
  - Puede ponerse lento (el dossier reporta mas de 12 s en hora pico).
  - Puede caerse (ventana dominical de 2 horas y 31 horas de caidas no
    planeadas en el ultimo ano).
  - Puede aceptar o no la misma cita dos veces (idempotencia).

Control en caliente, sin reiniciar:
  POST /admin?latencia_ms=4000     latencia de cada registro
  POST /admin?caido=1              1 = fuera de servicio, 0 = disponible
  POST /admin?idempotente=1        1 = ignora citas repetidas por id_cita
  GET  /citas                      por canal: registros, duplicadas y retraso
  DELETE /citas                    borra todo para empezar un experimento
"""
import random
import statistics
import threading
import time

from comun import entero, env, log, servir

ESTADO = {
    "latencia_ms": entero(env("LATENCIA_MS", "50"), 50),
    "caido": env("CAIDO", "0") == "1",
    "idempotente": env("IDEMPOTENTE", "0") == "1",
}
CITAS = []          # cada registro aceptado, incluidos los duplicados
IDS = set()
CANDADO = threading.Lock()


def registrar_cita(h, cuerpo, query):
    if ESTADO["caido"]:
        return h.responder(503, {"error": "HIS-CORE fuera de servicio"})
    # Latencia con algo de variacion: una latencia fija no se parece a nada real.
    base = ESTADO["latencia_ms"]
    time.sleep(max(0, random.gauss(base, base * 0.15)) / 1000)
    id_cita = cuerpo.get("id_cita")
    if not id_cita:
        return h.responder(400, {"error": "Falta id_cita"})
    ahora = time.time()
    with CANDADO:
        if id_cita in IDS and ESTADO["idempotente"]:
            return h.responder(200, {"id_cita": id_cita, "resultado": "ya registrada"})
        CITAS.append({
            "id_cita": id_cita,
            "canal": cuerpo.get("canal", "desconocido"),
            "creada_en": cuerpo.get("creada_en", ahora),
            "registrada_en": ahora,
        })
        IDS.add(id_cita)
    h.responder(201, {"id_cita": id_cita, "resultado": "registrada"})


def percentil(valores, p):
    if not valores:
        return None
    if len(valores) == 1:
        return valores[0]
    return statistics.quantiles(valores, n=100, method="inclusive")[p - 1]


def resumen(h, cuerpo, query):
    with CANDADO:
        copia = list(CITAS)
    canales = {}
    for canal in sorted({c["canal"] for c in copia}):
        propias = [c for c in copia if c["canal"] == canal]
        retrasos = sorted(c["registrada_en"] - c["creada_en"] for c in propias)
        unicas = len({c["id_cita"] for c in propias})
        canales[canal] = {
            "registros": len(propias),
            "citas_unicas": unicas,
            "duplicadas": len(propias) - unicas,
            "retraso_registro_s": {
                "p50": redondear(percentil(retrasos, 50)),
                "p95": redondear(percentil(retrasos, 95)),
                "max": redondear(retrasos[-1]),
            },
        }
    h.responder(200, {"estado": ESTADO, "por_canal": canales})


def redondear(valor):
    return None if valor is None else round(valor, 3)


def borrar(h, cuerpo, query):
    with CANDADO:
        CITAS.clear()
        IDS.clear()
    log("his-core", "citas borradas")
    h.responder(200, {"resultado": "citas borradas"})


def admin(h, cuerpo, query):
    if "latencia_ms" in query:
        ESTADO["latencia_ms"] = max(0, entero(query["latencia_ms"], ESTADO["latencia_ms"]))
    if "caido" in query:
        ESTADO["caido"] = query["caido"] == "1"
    if "idempotente" in query:
        ESTADO["idempotente"] = query["idempotente"] == "1"
    if query:
        log("his-core", f"configuracion: {ESTADO}")
    h.responder(200, ESTADO)


def salud(h, cuerpo, query):
    h.responder(503 if ESTADO["caido"] else 200, {"caido": ESTADO["caido"]})


if __name__ == "__main__":
    servir("his-core", {
        ("POST", "/citas"): registrar_cita,
        ("GET", "/citas"): resumen,
        ("DELETE", "/citas"): borrar,
        ("GET", "/admin"): admin,
        ("POST", "/admin"): admin,
        ("GET", "/salud"): salud,
    }, entero(env("PUERTO", "8081"), 8081))
