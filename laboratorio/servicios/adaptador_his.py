"""Adaptador de HIS-CORE: consume la cola de citas y las registra en HIS-CORE.

Es la pieza que la alternativa asincrona agrega a la arquitectura, y donde
aparecen los costos que el diagrama no muestra:

  - Si HIS-CORE no esta, el mensaje vuelve a la cola y se reintenta.
  - Si el adaptador falla despues de registrar la cita y antes de confirmar
    el mensaje (ack), RabbitMQ lo entrega otra vez. Si HIS-CORE no es
    idempotente, la cita queda duplicada.

Control en caliente:
  POST /admin?prob_fallo=0.2   probabilidad de fallar entre el registro y el ack
  POST /admin?reiniciar=1      pone los contadores en cero
  GET  /admin                  configuracion y contadores
"""
import json
import random
import threading
import time
import urllib.error
import urllib.request

from comun import entero, env, log, servir

HIS_CORE_URL = env("HIS_CORE_URL", "http://his-core:8081")
RABBIT_HOST = env("RABBIT_HOST", "rabbitmq")
COLA = env("COLA", "citas")
ESPERA_REINTENTO_S = float(env("ESPERA_REINTENTO_S", "2"))

ESTADO = {"prob_fallo": float(env("PROB_FALLO", "0"))}
CONTADORES = {"registradas": 0, "reintentos": 0, "fallos_simulados": 0}


class FalloSimulado(Exception):
    pass


def registrar_en_his(cuerpo):
    peticion = urllib.request.Request(
        f"{HIS_CORE_URL}/citas", data=cuerpo,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(peticion, timeout=30) as r:
        return r.status


def procesar(canal, metodo, propiedades, cuerpo):
    try:
        registrar_en_his(cuerpo)
    except (urllib.error.URLError, TimeoutError):
        # HIS-CORE no disponible: devolver el mensaje a la cola y esperar.
        CONTADORES["reintentos"] += 1
        time.sleep(ESPERA_REINTENTO_S)
        canal.basic_nack(metodo.delivery_tag, requeue=True)
        return
    if random.random() < ESTADO["prob_fallo"]:
        # La cita YA quedo en HIS-CORE, pero el ack nunca llega al broker.
        CONTADORES["fallos_simulados"] += 1
        raise FalloSimulado(json.loads(cuerpo)["id_cita"])
    canal.basic_ack(metodo.delivery_tag)
    CONTADORES["registradas"] += 1


def consumir():
    import pika
    while True:
        try:
            conexion = pika.BlockingConnection(pika.ConnectionParameters(
                host=RABBIT_HOST, heartbeat=30))
            canal = conexion.channel()
            canal.queue_declare(queue=COLA, durable=True)
            canal.basic_qos(prefetch_count=1)
            log("adaptador-his", f"consumiendo la cola '{COLA}'")
            for metodo, propiedades, cuerpo in canal.consume(COLA):
                procesar(canal, metodo, propiedades, cuerpo)
        except FalloSimulado as e:
            # Se cierra la conexion sin ack: RabbitMQ reentrega el mensaje.
            log("adaptador-his", f"fallo simulado despues de registrar {e}; sin ack")
            try:
                conexion.close()
            except Exception:
                pass
        except Exception as e:
            log("adaptador-his", f"sin conexion con RabbitMQ ({e.__class__.__name__}); reintento en 3 s")
            time.sleep(3)


def admin(h, cuerpo, query):
    if query.get("reiniciar") == "1":
        for clave in CONTADORES:
            CONTADORES[clave] = 0
    if "prob_fallo" in query:
        ESTADO["prob_fallo"] = min(1.0, max(0.0, float(query["prob_fallo"])))
        log("adaptador-his", f"configuracion: {ESTADO}")
    h.responder(200, {**ESTADO, **CONTADORES})


if __name__ == "__main__":
    threading.Thread(target=consumir, daemon=True).start()
    servir("adaptador-his", {
        ("GET", "/admin"): admin,
        ("POST", "/admin"): admin,
    }, entero(env("PUERTO", "8082"), 8082))
