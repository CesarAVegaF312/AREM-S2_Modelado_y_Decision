"""Generador de carga y tablero de estado del laboratorio.

  python carga.py agendar --destino sincrono --peticiones 200 --concurrencia 20
  python carga.py agendar --destino asincrono --peticiones 200 --concurrencia 20
  python carga.py estado
  python carga.py configurar --latencia-ms 4000
  python carga.py reiniciar

Cada corrida de 'agendar' imprime el resumen y lo guarda en resultados/ como
JSON, con la configuracion de HIS-CORE de ese momento. Ese archivo es la
evidencia que va al informe.
"""
import argparse
import base64
import json
import os
import socket
import statistics
import threading
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

DESTINOS = {
    "sincrono": os.environ.get("AGENDA_SINCRONA_URL", "http://agenda-sincrona:8080"),
    "asincrono": os.environ.get("AGENDA_ASINCRONA_URL", "http://agenda-asincrona:8080"),
}
HIS_CORE_URL = os.environ.get("HIS_CORE_URL", "http://his-core:8081")
ADAPTADOR_HOST = os.environ.get("ADAPTADOR_HOST", "adaptador-his")
ADAPTADOR_PUERTO = 8082
RABBIT_API = os.environ.get("RABBIT_API", "http://rabbitmq:15672/api/queues/%2F/citas")
OBJETIVO_S = float(os.environ.get("OBJETIVO_S", "3"))  # objetivo interno del caso
RESULTADOS = os.environ.get("RESULTADOS", "/resultados")
SEDES = ["Sede Centro", "Sede Norte 1", "Clinica Andina", "Sede Sur", "Sede Norte 4"]


def leer_json(url, usuario=None):
    peticion = urllib.request.Request(url)
    if usuario:
        peticion.add_header("Authorization", "Basic " + base64.b64encode(usuario.encode()).decode())
    try:
        with urllib.request.urlopen(peticion, timeout=5) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404 and url == RABBIT_API:
            return {"error": "La cola aun no existe: se crea con la primera cita."}
        return {"error": f"Respondio {e.code}"}
    except Exception as e:
        return {"error": f"Todavia no responde ({e.__class__.__name__}). Si acaba de levantar el "
                         "laboratorio, esperen unos segundos y repitan."}


def adaptadores():
    """URL de cada instancia del adaptador: con --scale hay varias detras del mismo nombre."""
    try:
        ips = sorted({info[4][0] for info in socket.getaddrinfo(ADAPTADOR_HOST, ADAPTADOR_PUERTO)})
    except socket.gaierror:
        return []
    return [f"http://{ip}:{ADAPTADOR_PUERTO}" for ip in ips]


def una_cita(url, i):
    datos = json.dumps({"paciente": f"Paciente {i:04d}", "sede": SEDES[i % len(SEDES)],
                        "fecha": "2026-11-15T08:00"}).encode("utf-8")
    peticion = urllib.request.Request(f"{url}/agendar", data=datos,
                                      headers={"Content-Type": "application/json"}, method="POST")
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(peticion, timeout=60) as r:
            r.read()
            codigo = r.status
    except urllib.error.HTTPError as e:
        codigo = e.code
    except Exception:
        codigo = "sin respuesta"
    return codigo, time.perf_counter() - inicio


def percentil(valores, p):
    if len(valores) < 2:
        return valores[0] if valores else 0.0
    return statistics.quantiles(valores, n=100, method="inclusive")[p - 1]


def agendar(args):
    url = DESTINOS[args.destino]
    his = leer_json(f"{HIS_CORE_URL}/admin")
    print(f"Destino: AGENDA-WEB {args.destino} ({url})")
    print(f"HIS-CORE: {his}")
    print(f"{args.peticiones} citas con {args.concurrencia} pacientes a la vez...\n")

    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrencia) as hilos:
        resultados = list(hilos.map(lambda i: una_cita(url, i), range(args.peticiones)))
    duracion = time.perf_counter() - inicio

    codigos = Counter(str(c) for c, _ in resultados)
    exitosas = [t for c, t in resultados if c in (200, 201, 202)]
    todas = sorted(t for _, t in resultados)
    resumen = {
        "destino": args.destino,
        "etiqueta": args.etiqueta,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "his_core": his,
        "peticiones": args.peticiones,
        "concurrencia": args.concurrencia,
        "duracion_s": round(duracion, 2),
        "throughput_citas_por_s": round(args.peticiones / duracion, 1),
        "codigos": dict(codigos),
        "exito_pct": round(100 * len(exitosas) / args.peticiones, 1),
        "tiempo_respuesta_s": {
            "p50": round(percentil(todas, 50), 3),
            "p95": round(percentil(todas, 95), 3),
            "max": round(todas[-1], 3),
        },
        "cumple_objetivo_3s_pct": round(100 * sum(t <= OBJETIVO_S for t in exitosas) / args.peticiones, 1),
    }

    t = resumen["tiempo_respuesta_s"]
    print(f"  Respuestas por codigo       {dict(codigos)}")
    print(f"  Exito                       {resumen['exito_pct']} %")
    print(f"  Tiempo de respuesta p50     {t['p50']} s")
    print(f"  Tiempo de respuesta p95     {t['p95']} s")
    print(f"  Tiempo de respuesta max     {t['max']} s")
    print(f"  {'Exitosas en <= %g s' % OBJETIVO_S:<28}{resumen['cumple_objetivo_3s_pct']} %")
    print(f"  Throughput                  {resumen['throughput_citas_por_s']} citas/s")
    if args.destino == "asincrono":
        print("\n  Ojo: en asincrono, 'exito' significa 'encolada', no 'registrada en HIS-CORE'.")
        print("  Para saber cuantas llegaron y con cuanto retraso: python carga.py estado")

    os.makedirs(RESULTADOS, exist_ok=True)
    nombre = time.strftime("%Y%m%d-%H%M%S") + f"-{args.destino}" + (f"-{args.etiqueta}" if args.etiqueta else "")
    ruta = os.path.join(RESULTADOS, nombre + ".json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print(f"\n  Guardado en resultados/{nombre}.json")


def estado(args):
    his = leer_json(f"{HIS_CORE_URL}/citas")
    cola = leer_json(RABBIT_API, usuario="guest:guest")
    instancias = [leer_json(f"{u}/admin") for u in adaptadores()]
    print("HIS-CORE")
    if "error" in his:
        print(f"  {his['error']}")
    else:
        print(f"  Configuracion          {his['estado']}")
        if not his["por_canal"]:
            print("  Sin citas registradas")
        for canal, c in his["por_canal"].items():
            r = c["retraso_registro_s"]
            print(f"  Canal {canal}")
            print(f"    Registros            {c['registros']}")
            print(f"    Citas unicas         {c['citas_unicas']}")
            print(f"    Duplicadas           {c['duplicadas']}")
            print(f"    Retraso de registro  p50 {r['p50']} s · p95 {r['p95']} s · max {r['max']} s")
    print("Cola 'citas' en RabbitMQ (la consola actualiza cada 5 s)")
    if "error" in cola:
        print(f"  {cola['error']}")
    else:
        print(f"  Esperando              {cola.get('messages_ready', 0)}")
        print(f"  En proceso (sin ack)   {cola.get('messages_unacknowledged', 0)}")
    print(f"Adaptador de HIS-CORE ({len(instancias)} instancia(s))")
    for i, a in enumerate(instancias, 1):
        if "error" in a:
            print(f"  [{i}] {a['error']}")
        else:
            print(f"  [{i}] " + " · ".join(f"{k} {v}" for k, v in a.items()))


def enviar(url, metodo="POST", usuario=None):
    peticion = urllib.request.Request(url, method=metodo)
    if usuario:
        peticion.add_header("Authorization", "Basic " + base64.b64encode(usuario.encode()).decode())
    try:
        with urllib.request.urlopen(peticion, timeout=5) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return e.__class__.__name__


def configurar_adaptadores(prob_fallo):
    return [enviar(f"{u}/admin?prob_fallo={prob_fallo}") for u in adaptadores()]


def configurar(args):
    cambios = {}
    if args.latencia_ms is not None:
        cambios["latencia_ms"] = args.latencia_ms
    if args.caido is not None:
        cambios["caido"] = args.caido
    if args.idempotente is not None:
        cambios["idempotente"] = args.idempotente
    if cambios:
        query = "&".join(f"{k}={v}" for k, v in cambios.items())
        print(f"  HIS-CORE {str(cambios):<40} {enviar(f'{HIS_CORE_URL}/admin?{query}')}")
    if args.prob_fallo is not None:
        print(f"  {'Adaptador prob_fallo=%g' % args.prob_fallo:<49} {configurar_adaptadores(args.prob_fallo)}")
    if not cambios and args.prob_fallo is None:
        print("  Nada que configurar. Vea: python carga.py configurar --help")


def reiniciar(args):
    """Deja todo como al levantar el laboratorio, para empezar un experimento limpio."""
    pasos = [
        ("HIS-CORE disponible, 50 ms, sin idempotencia",
         enviar(f"{HIS_CORE_URL}/admin?latencia_ms=50&caido=0&idempotente=0")),
        ("Citas de HIS-CORE borradas", enviar(f"{HIS_CORE_URL}/citas", "DELETE")),
        ("Adaptadores sin fallos simulados y en cero",
         [enviar(f"{u}/admin?prob_fallo=0&reiniciar=1") for u in adaptadores()]),
        ("Cola 'citas' vaciada",
         vaciar if (vaciar := enviar(RABBIT_API + "/contents", "DELETE", usuario="guest:guest")) != 404
         else "aun no existe; nada que vaciar"),
    ]
    for descripcion, resultado in pasos:
        print(f"  {descripcion:<48} {resultado}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Carga y estado del laboratorio de la costura")
    sub = p.add_subparsers(dest="comando", required=True)
    a = sub.add_parser("agendar", help="genera citas contra AGENDA-WEB")
    a.add_argument("--destino", choices=DESTINOS, required=True)
    a.add_argument("--peticiones", type=int, default=200)
    a.add_argument("--concurrencia", type=int, default=20)
    a.add_argument("--etiqueta", default="", help="nombre corto del experimento, p. ej. e2-lento")
    a.set_defaults(funcion=agendar)
    e = sub.add_parser("estado", help="muestra HIS-CORE, la cola y el adaptador")
    e.set_defaults(funcion=estado)
    c = sub.add_parser("configurar", help="cambia HIS-CORE y el adaptador en caliente")
    c.add_argument("--latencia-ms", type=int, help="latencia de HIS-CORE por cita")
    c.add_argument("--caido", type=int, choices=[0, 1], help="1 = HIS-CORE fuera de servicio")
    c.add_argument("--idempotente", type=int, choices=[0, 1], help="1 = HIS-CORE ignora citas repetidas")
    c.add_argument("--prob-fallo", type=float, help="probabilidad de fallo del adaptador antes del ack")
    c.set_defaults(funcion=configurar)
    r = sub.add_parser("reiniciar", help="vuelve a la configuracion inicial y borra los datos")
    r.set_defaults(funcion=reiniciar)
    args = p.parse_args()
    args.funcion(args)
