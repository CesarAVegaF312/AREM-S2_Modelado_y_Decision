"""AGENDA-WEB: el portal donde el paciente agenda su cita.

El mismo codigo corre de dos maneras, segun la variable MODO:

  sincrono   Llama al API de HIS-CORE y espera la respuesta antes de contestar
             al paciente. Es la costura que existe hoy en el caso.
  asincrono  Publica la cita en una cola de RabbitMQ y contesta de inmediato.
             El adaptador-his la lleva a HIS-CORE despues.

POST /agendar  {"paciente": "...", "sede": "...", "fecha": "..."}
"""
import json
import threading
import time
import urllib.error
import urllib.request
import uuid

from comun import entero, env, log, servir

MODO = env("MODO", "sincrono")
HIS_CORE_URL = env("HIS_CORE_URL", "http://his-core:8081")
TIMEOUT_S = float(env("TIMEOUT_S", "15"))
RABBIT_HOST = env("RABBIT_HOST", "rabbitmq")
COLA = env("COLA", "citas")
NOMBRE = f"agenda-{MODO}"


class Publicador:
    """Una conexion compartida. pika no es seguro entre hilos: se serializa."""

    def __init__(self):
        self.candado = threading.Lock()
        self.canal = None

    def _conectar(self):
        import pika  # solo hace falta en modo asincrono
        conexion = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBIT_HOST, heartbeat=30, blocked_connection_timeout=10))
        canal = conexion.channel()
        canal.queue_declare(queue=COLA, durable=True)
        canal.confirm_delivery()  # el broker confirma que guardo el mensaje
        return canal

    def publicar(self, mensaje):
        import pika
        with self.candado:
            for intento in (1, 2):
                try:
                    if self.canal is None or self.canal.is_closed:
                        self.canal = self._conectar()
                    self.canal.basic_publish(
                        exchange="", routing_key=COLA, body=json.dumps(mensaje),
                        properties=pika.BasicProperties(delivery_mode=2),  # persistente
                        mandatory=True)
                    return
                except Exception:
                    self.canal = None
                    if intento == 2:
                        raise


PUBLICADOR = Publicador()


def agendar(h, cuerpo, query):
    cita = {
        "id_cita": str(uuid.uuid4()),
        "paciente": cuerpo.get("paciente", "anonimo"),
        "sede": cuerpo.get("sede", "sin sede"),
        "fecha": cuerpo.get("fecha", ""),
        "creada_en": time.time(),
        "canal": MODO,
    }
    if MODO == "asincrono":
        try:
            PUBLICADOR.publicar(cita)
        except Exception as e:
            return h.responder(503, {"error": f"No se pudo encolar la cita: {e}"})
        return h.responder(202, {
            "id_cita": cita["id_cita"],
            "estado": "recibida; se confirma en HIS-CORE cuando este disponible",
        })

    peticion = urllib.request.Request(
        f"{HIS_CORE_URL}/citas", data=json.dumps(cita).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT_S) as r:
            return h.responder(201, {"id_cita": cita["id_cita"], "estado": "confirmada en HIS-CORE",
                                     "his_core": json.loads(r.read())})
    except urllib.error.HTTPError as e:
        return h.responder(502, {"error": f"HIS-CORE respondio {e.code}"})
    except (TimeoutError, urllib.error.URLError) as e:
        return h.responder(504, {"error": f"HIS-CORE no respondio: {e}"})


def salud(h, cuerpo, query):
    h.responder(200, {"servicio": NOMBRE})


if __name__ == "__main__":
    log(NOMBRE, f"modo {MODO}")
    servir(NOMBRE, {
        ("POST", "/agendar"): agendar,
        ("GET", "/salud"): salud,
    }, entero(env("PUERTO", "8080"), 8080))
