# AREM S2 — Laboratorio: la costura de integración

Laboratorio de la **Sesión 2** del curso *Arquitectura Empresarial* (AREM), Unidad 2:
**Modelado Empresarial y Arquitectura de Integración**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

En la Actividad 2.2 hay que comparar dos alternativas de integración y declarar qué se sacrifica.
Normalmente esa comparación se argumenta. En este laboratorio **se mide**: las dos alternativas
corren en su computador, se les aplica el mismo estímulo y se registra cómo responde cada una. Los
números que salen de aquí son la evidencia de los escenarios de calidad (**F-14**) y del comparador
de alternativas (**F-16**) de su informe.

No hay que programar. El código ya está escrito; el trabajo es diseñar el experimento, leer los
resultados y decidir.

---

## El escenario

Es la costura **AGENDA-WEB → HIS-CORE** del caso Red Salud Andina (dossier, secciones 7 y 8):

- Es el **único punto del inventario con un API real**, y no tiene control de versiones del contrato.
- HIS-CORE tiene una **ventana de mantenimiento de 2 horas cada domingo** y acumuló **31 horas de
  caídas no planeadas** en el último año.
- El portal de agendamiento tarda **más de 12 s en hora pico**; el objetivo interno es **3 s**.

Hoy la costura es **síncrona**: el portal llama a HIS-CORE y espera la respuesta antes de
contestarle al paciente. La alternativa es **asíncrona**: el portal deja la cita en una cola y
contesta de inmediato; un adaptador la lleva a HIS-CORE cuando puede.

| | Alternativa síncrona (hoy) | Alternativa asíncrona |
|---|---|---|
| Qué hace el portal | Llama a HIS-CORE y espera | Publica la cita en una cola y contesta |
| Qué recibe el paciente | «Cita confirmada» o un error | «Cita recibida»; la confirmación llega después |
| Piezas nuevas | Ninguna | Una cola (RabbitMQ) y un adaptador |

Ninguna de las dos es la respuesta correcta. El laboratorio sirve para que su decisión diga **qué
gana y qué paga** cada una, con cifras.

---

## Requisitos

- **Docker Desktop** (Windows o Mac) o Docker Engine con el plugin Compose (Linux). Verifiquen con
  `docker compose version`.
- Unos **3 GB libres** de disco para las imágenes, y los puertos 8080, 8081, 8090, 8200 y 15672 libres.
- **Sin Docker en su equipo:** abran el repositorio en **GitHub Codespaces** (botón verde
  **`Code` → `Codespaces`**) y elijan la configuración **«AREM S2 · Laboratorio de la costura»**.
  El ambiente ya viene configurado en `.devcontainer/laboratorio/`. En la terminal, entren a la
  carpeta con `cd laboratorio`.

La primera vez se descargan las imágenes y tarda unos minutos. Después arranca en segundos.

---

## Levantar el laboratorio

```bash
git clone https://github.com/CesarAVegaF312/AREM-S2_Modelado_y_Decision.git
cd AREM-S2_Modelado_y_Decision/laboratorio
docker compose up -d --build
docker compose run --rm carga estado
```

Todos los comandos de esta guía se ejecutan dentro de la carpeta `laboratorio/`.

Si el último comando muestra HIS-CORE, la cola y el adaptador sin errores, el laboratorio está listo.

| Servicio | Qué es | Dónde |
|---|---|---|
| `agenda-sincrona` | AGENDA-WEB, alternativa síncrona | <http://localhost:8080> |
| `agenda-asincrona` | AGENDA-WEB, alternativa asíncrona | <http://localhost:8090> |
| `his-core` | Simulador de HIS-CORE: se puede poner lento, caer o volver idempotente | <http://localhost:8081> |
| `rabbitmq` | La cola de citas. Consola web con usuario y clave `guest` | <http://localhost:15672> |
| `adaptador-his` | Lleva las citas de la cola a HIS-CORE y reintenta si no responde | — |
| `carga` | La herramienta del laboratorio: genera citas, cambia la configuración y muestra el estado | — |

Los cuatro comandos que se usan en todo el laboratorio:

```bash
docker compose run --rm carga reiniciar                     # todo como al principio, sin datos
docker compose run --rm carga configurar --latencia-ms 4000 # cambia HIS-CORE o el adaptador
docker compose run --rm carga agendar --destino sincrono    # genera citas y mide
docker compose run --rm carga estado                        # qué llegó a HIS-CORE y qué hay en la cola
```

Cada corrida de `agendar` guarda su resumen en `resultados/` como JSON, con la configuración de
HIS-CORE de ese momento. Usen `--etiqueta` para reconocerlas después.

---

## Experimentos

Hagan los cinco en orden y **empiecen cada uno con `reiniciar`**. Antes de correrlo, escriban qué
esperan que pase: la diferencia entre lo que esperaban y lo que midieron es lo más útil del
laboratorio. Tiempo estimado: dos horas.

En `agendar`, `--peticiones` es cuántas citas se piden y `--concurrencia` cuántos pacientes las piden
al mismo tiempo. Si cambian esos valores, usen los mismos en las dos alternativas: si no, la
comparación no vale.

### Experimento 1 — Línea base

HIS-CORE responde en unos 50 ms, como en un día tranquilo.

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga agendar --destino sincrono  --peticiones 100 --concurrencia 10 --etiqueta e1
docker compose run --rm carga agendar --destino asincrono --peticiones 100 --concurrencia 10 --etiqueta e1
docker compose run --rm carga estado
```

**Registren:** tiempo de respuesta p50 y p95 de cada alternativa, y el retraso de registro en
HIS-CORE del canal asíncrono.

**Para pensar:** si las dos cumplen el objetivo de 3 s, ¿qué argumento queda para cambiar la costura?

### Experimento 2 — Hora pico: HIS-CORE lento

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --latencia-ms 4000
docker compose run --rm carga agendar --destino sincrono  --peticiones 60 --concurrencia 20 --etiqueta e2
docker compose run --rm carga agendar --destino asincrono --peticiones 60 --concurrencia 20 --etiqueta e2
docker compose run --rm carga estado
```

Repitan `estado` cada 30 s hasta que la cola quede vacía.

**Registren:** el porcentaje de citas que cumplen los 3 s en cada alternativa, cuántas citas hay en la
cola y cuánto tarda en vaciarse.

**Para pensar:** en la alternativa asíncrona el paciente recibe respuesta rápido. ¿Cuándo queda la
cita en HIS-CORE? ¿Qué pasa si el paciente llega a la sede antes de eso?

### Experimento 3 — Ventana de mantenimiento: HIS-CORE caído

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --caido 1
docker compose run --rm carga agendar --destino sincrono  --peticiones 50 --concurrencia 10 --etiqueta e3
docker compose run --rm carga agendar --destino asincrono --peticiones 50 --concurrencia 10 --etiqueta e3
docker compose run --rm carga estado
```

Esperen un minuto: es su «ventana de mantenimiento». Luego devuelvan el servicio y miren cómo se
pone al día:

```bash
docker compose run --rm carga configurar --caido 0
docker compose run --rm carga estado
```

**Registren:** el porcentaje de éxito de cada alternativa mientras HIS-CORE está caído, los
reintentos del adaptador y el retraso máximo de registro cuando HIS-CORE vuelve.

**Para pensar:** hoy, durante la ventana dominical, Urgencias opera en papel. ¿Qué cambiaría para el
agendamiento? ¿Qué no cambiaría?

### Experimento 4 — El costo que no sale en el diagrama: duplicados

El adaptador puede fallar justo después de registrar la cita en HIS-CORE y antes de avisarle a la
cola que terminó. La cola no sabe que la cita ya quedó registrada y la entrega otra vez.

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --prob-fallo 0.2
docker compose run --rm carga agendar --destino asincrono --peticiones 100 --concurrencia 10 --etiqueta e4-sin-idempotencia
docker compose run --rm carga estado
```

Repítanlo haciendo que HIS-CORE ignore las citas que ya tiene:

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --prob-fallo 0.2 --idempotente 1
docker compose run --rm carga agendar --destino asincrono --peticiones 100 --concurrencia 10 --etiqueta e4-con-idempotencia
docker compose run --rm carga estado
```

**Registren:** las citas duplicadas en cada corrida.

**Para pensar:** «HIS-CORE idempotente» es una línea en este laboratorio. En el caso real, HIS-CORE
es un producto de un proveedor que nadie modifica sin riesgo. ¿Dónde se resuelve entonces la
idempotencia, y quién la mantiene? Eso también es deuda.

### Experimento 5 — Escalar el adaptador

Con HIS-CORE lento, un solo adaptador vacía la cola de a una cita a la vez.

```bash
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --latencia-ms 1000
docker compose run --rm carga agendar --destino asincrono --peticiones 40 --concurrencia 10 --etiqueta e5-1
```

Esperen a que la cola se vacíe (`estado`) y anoten el retraso máximo. Luego, con cuatro adaptadores:

```bash
docker compose up -d --scale adaptador-his=4
docker compose run --rm carga reiniciar
docker compose run --rm carga configurar --latencia-ms 1000
docker compose run --rm carga agendar --destino asincrono --peticiones 40 --concurrencia 10 --etiqueta e5-4
```

Al terminar, vuelvan a uno: `docker compose up -d --scale adaptador-his=1`.

**Para pensar:** cuatro adaptadores mandan cuatro veces más carga a un HIS-CORE que ya está lento.
¿Lo resiste el sistema real? ¿Quién decide cuántos adaptadores corren?

---

## Del laboratorio al informe

Un escenario de calidad del **F-14** tiene fuente, estímulo, artefacto, entorno, respuesta y medida.
El laboratorio les da la **medida**, que es la parte que casi siempre queda inventada. Por ejemplo,
con la estructura del F-14:

| Fuente | Estímulo | Entorno | Respuesta esperada | Medida (síncrona) | Medida (asíncrona) |
|---|---|---|---|---|---|
| Paciente | Agenda una cita | HIS-CORE en ventana de mantenimiento | El paciente recibe respuesta y la cita no se pierde | *% de éxito del experimento 3* | *% de éxito y retraso máximo del experimento 3* |

Lleven al informe **la tabla de mediciones**, no capturas de la consola, y digan con qué
configuración se obtuvo cada cifra: está en cada archivo de `resultados/`.

Dos advertencias para el análisis:

- **Este es un modelo, no el sistema real.** Las cifras sirven para comparar las alternativas entre sí
  bajo el mismo estímulo, no para predecir tiempos de producción. Díganlo en el informe.
- **Lo que no se mide aquí también cuenta.** El costo de operar RabbitMQ, quién monitorea la cola o el
  contrato con el proveedor de AGENDA-WEB van en el análisis de trade-offs aunque el laboratorio no
  los cuantifique.

---

## El modelo C4

`modelo/workspace.dsl` describe la costura en **Structurizr DSL**: un diagrama de contexto y una
vista de contenedores por cada alternativa. Los diagramas se generan a partir del texto: se cambia
el modelo, no el dibujo.

```bash
docker compose --profile modelo up -d structurizr
```

Ábranlo en <http://localhost:8200>. Si editan `workspace.dsl`, recarguen la página para ver el
cambio. Pueden usar este modelo como base para la vista de integración de su propio caso.

---

## Apagar

```bash
docker compose --profile modelo down
```

Los datos del laboratorio viven en memoria: al apagarlo se pierden, pero los archivos de
`resultados/` se conservan.

---

## Problemas frecuentes

**`docker: command not found` o «Cannot connect to the Docker daemon».**
Docker Desktop no está instalado o no está abierto. Ábranlo y esperen a que diga que está corriendo.

**«port is already allocated».**
Otro programa usa ese puerto. Ciérrenlo, o cambien el número de la izquierda en `docker-compose.yml`
(por ejemplo `"18080:8080"`).

**`estado` muestra la cola con cero mensajes justo después de `agendar`.**
La consola de RabbitMQ actualiza sus contadores cada 5 s. Esperen un momento y repitan.

**Structurizr dice «Data directory /usr/local/structurizr is not writable» (Linux).**
Den permiso de escritura a la carpeta del modelo: `chmod a+w modelo`. En Windows, Mac y Codespaces
no hace falta.

**Una corrida sale muy distinta de la anterior.**
¿Empezaron con `reiniciar`? Si quedaron citas en la cola de un experimento anterior, se mezclan con
las nuevas.

---

## Licencia

Este laboratorio es parte del repositorio de la Sesión 2 y se distribuye con su misma licencia,
[Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es),
incluido el código del laboratorio.

*Nota: Red Salud Andina es una organización simulada con fines pedagógicos. RabbitMQ es marca de
Broadcom; Structurizr, de Structurizr Limited.*
