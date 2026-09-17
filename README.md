# AREM S2 — Modelado y Decisión

Material de la **Sesión 2** del curso *Arquitectura Empresarial* (AREM), Unidad 2:
**Modelado Empresarial y Arquitectura de Integración**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

La unidad va de representar formalmente una arquitectura a **decidir entre dos caminos
defendibles y declarar qué se sacrifica**. Marco de referencia: **TOGAF® Standard,
10th Edition**. Lenguaje de modelado: **ArchiMate® 3.2**.

Las actividades de la unidad, tal como están en la plataforma:

- **Actividad 2.1 — Presentación del reto** · individual · formativa, sin calificación.
  - **Antes de la sesión:** instalen Archi y lean la
    [especificación de ArchiMate 3.2](https://www.opengroup.org/sites/default/files/docs/downloads/n221p.pdf)
    (capítulos 1 a 3) y la descripción de ATAM en Lankhorst (2017), capítulo 6.
  - **Entregable:** mapa mental o esquema visual de 1 página que relacione las capas de
    ArchiMate con las cuatro capas arquitectónicas del curso. La retroalimentación se da con
    el **F-19**.
- **Actividad 2.2 — Modelado arquitectónico y evaluación de trade-offs** · grupal, de **3 a 4
  integrantes** · 30 % · 20 horas.
  - **Entregable:** lo que la actividad llama «repositorio de arquitectura» son dos cosas que se
    suben a la plataforma: **(a)** los diagramas ArchiMate exportados como imagen (PNG o PDF) y
    **(b)** un informe de evaluación arquitectónica en PDF de **máximo 20 páginas**, en **norma
    APA 7**. No es un repositorio de GitHub.
  - Se califica con la rúbrica de la actividad, de cuatro criterios: vistas ArchiMate (2,0),
    evaluación ATAM y trade-offs (1,5), estrategia de integración y deuda (1,0) y calidad
    documental (0,5).
  - **Los formatos F-13 a F-20 no se suben:** son el borrador de las secciones del informe.

---

## Empiecen aquí

1. **Lean el [mapa de la Actividad 2.2](documentos/1_actividad_2_2/AREM_S2_Mapa_Actividad_2_2.pdf).** Tres páginas: qué pide la actividad, con
   qué criterio se califica, en qué sección del informe va cada cosa y qué formato la prepara.
2. **Miren el [informe de ejemplo](documentos/1_actividad_2_2/AREM_S2_Informe_Ejemplo_Actividad_2_2.pdf).** Así se ve la 2.2 terminada, con Red Salud
   Andina. Cada sección abre con un recuadro que explica qué hay que hacer en ella.
3. **Instalen Archi.** Descárguenlo de [archimatetool.com](https://www.archimatetool.com) →
   *Downloads*. Es gratuito y de código abierto.
4. **Abran el caso resuelto.** En Archi, **`File → Open`** →
   [`modelo/AREM_S2_Modelo_Red_Salud_Andina.archimate`](modelo/AREM_S2_Modelo_Red_Salud_Andina.archimate).
   Despliegan **Views** en el árbol de la izquierda y tienen las cuatro vistas del informe de
   ejemplo.

Para trabajar sin conexión, descarguen el repositorio (botón verde **`Code` → `Download ZIP`**),
descomprímanlo y hagan doble clic en `index.html`: la portada abre todos los documentos y
herramientas. El caso completo está en el [dossier de Red Salud Andina](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf).

---

## Paso a paso de la unidad

Los pasos siguen el orden en que conviene trabajar, no el orden del informe; por eso cada paso
dice en qué sección del informe termina. El orden importa: **primero se decide qué se va a
mostrar, después se dibuja**. Quien abre Archi antes de llenar el F-13 dibuja dos veces: una
para descubrir qué quería mostrar y otra para mostrarlo.

Los formatos están en los [Instrumentos F-13 a F-20](documentos/3_como_se_hace/AREM_S2_Instrumentos.pdf); cómo llenarlos campo por campo,
en la [guía de formatos](documentos/3_como_se_hace/AREM_S2_Guia_Visuales_e_Instrumentos.pdf); y cada herramienta recorrida con el caso, en los
[recorridos resueltos](documentos/3_como_se_hace/AREM_S2_Recorridos_Resueltos.pdf).

### Paso 1 · Decidir qué vistas van

- **Cuándo:** en clase, en la **Actividad 2.2 · Parte 1**, antes de abrir Archi. Qué se hace
  en la parte 1 está en el [enunciado](documentos/1_actividad_2_2/AREM_S2_Enunciado_Actividad_2_2.pdf).
- **Con qué:** [las cuatro vistas de Red Salud Andina](interactivos/vistas_archimate_red_salud.html)
  (resueltas, con tres contraejemplos) y el modelo de ejemplo.
- **Produce:** **F-13** — catálogo de vistas. Una ficha por vista, con su *stakeholder*, su
  *concern*, su punto de vista, su fase del ADM y la decisión que habilita.
- **Va al informe en:** sección 2, la tabla debajo de cada vista.
- **Se califica en:** *Vistas ArchiMate* (2,0).

### Paso 2 · Modelar las cuatro vistas en Archi

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** la [guía de Archi paso a paso](documentos/3_como_se_hace/AREM_S2_Guia_Archi_PasoAPaso.pdf) abierta y
  [ArchiMate 3.2 interactivo](interactivos/archimate_interactivo.html) al lado, como diccionario
  de elementos y relaciones.
- **Produce:** las cuatro vistas —motivación y estrategia; negocio; aplicación y tecnología;
  implementación y migración—, cada una con **mínimo 5 elementos**, sus relaciones y las
  decisiones de diseño que representa, exportadas como imagen (PNG o PDF).
- **Va al informe en:** sección 2, una figura por vista, y como diagramas sueltos en la entrega.
- **Se califica en:** *Vistas ArchiMate* (2,0). La rúbrica premia que las vistas estén
  **relacionadas y sean coherentes entre sí**, no solo que existan.

### Paso 3 · Escenarios de calidad, árbol de utilidad y alternativas

- **Cuándo:** en clase, en la **Actividad 2.2 · Parte 2** (F-14 y F-16); el F-15, fuera de clase
  y en grupo. Qué se hace en la parte 2 está en el [enunciado](documentos/1_actividad_2_2/AREM_S2_Enunciado_Actividad_2_2.pdf).
- **Con qué:** [Escenarios ATAM](interactivos/atam_escenarios_interactivo.html). No deja
  registrar un escenario sin medida ni cerrar la decisión sin la renuncia, y genera el texto
  para pegar en el informe.
- **Produce:**
  - **F-14** — al menos **tres escenarios de calidad**, con medida de respuesta y cómo se
    verifica: **disponibilidad, rendimiento y evolubilidad (mantenibilidad)**, los tres que pide
    la actividad. Los de costo de operación y componente de IA son **opcionales**: agréguenlos
    solo si su caso los necesita.
  - **F-15** — árbol de utilidad completo, con la doble valoración.
  - **F-16** — las dos alternativas y, para **cada una**, qué se gana y qué se sacrifica, sus
    **riesgos** y sus **puntos de sensibilidad**. La rúbrica exige el análisis de riesgos para
    la nota máxima.
- **Va al informe en:** sección 3 — las alternativas en 3.1, los escenarios del F-14 en 3.2, el
  árbol del F-15 en 3.3 y la comparación, los riesgos, los trade-offs y la decisión del F-16 en
  3.4 a 3.7.
- **Se califica en:** *Evaluación ATAM y trade-offs* (1,5).
- **Si las alternativas difieren sobre todo en costo,** pueden complementar ATAM con **CBAM**
  (Cost-Benefit Analysis Method; Bass, Clements y Kazman, 2003), que pone valor esperado y
  costo a cada alternativa.

### Paso 4 · Elegir la costura de integración

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [C4 Model](interactivos/c4_model_interactivo.html) (en qué nivel de zoom vive la
  decisión), [Costura de integración](interactivos/costura_integracion_interactivo.html) (las
  cuatro formas de resolverla) y [Wardley Map](interactivos/wardley_map_interactivo.html) (qué se
  construye y qué se consume).
- **Produce:** **F-17** — ficha de la costura de integración. La estrategia elegida (APIs,
  arquitectura orientada a eventos o mensajería) tiene que quedar **dibujada en la vista
  ArchiMate de aplicación** y justificada frente a las alternativas.
- **Tengan presente el dilema de la unidad:** reescribir el sistema heredado de una vez o
  **estrangularlo gradualmente** detrás de una fachada (patrón *Strangler Fig*; Fowler, 2004).
  La costura que elijan decide cuál de los dos caminos es posible.
- **Va al informe en:** sección 4.
- **Se califica en:** *Estrategia de integración y deuda* (1,0).

### Paso 5 · Registrar la deuda arquitectónica

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [Deuda arquitectónica](interactivos/deuda_arquitectonica_interactivo.html). Cada
  partida con principal, interés mensual con cifra, vencimiento y estrategia.
- **Produce:** **F-18** — registro de deuda arquitectónica. La cartera tiene que usar **al
  menos dos estrategias de gestión distintas**: pagar, refinanciar o declarar.
- **Va al informe en:** sección 5.
- **Se califica en:** *Estrategia de integración y deuda* (1,0).

### Paso 6 · Armar el informe

- **Cuándo:** fuera de clase, en grupo, cuando los pasos 1 a 5 estén listos.
- **Con qué:** el [informe de ejemplo](documentos/1_actividad_2_2/AREM_S2_Informe_Ejemplo_Actividad_2_2.pdf) como guía de estructura.
- **Produce:** el informe completo. Además de pasar los formatos a las secciones 2 a 5, se
  escriben dos secciones que no salen de ningún formato:
  - **Sección 1 · Contexto, alcance y método:** la brecha que priorizaron en la Unidad 1, qué
    cubre el informe y qué no, el método y la tabla de supuestos.
  - **Sección 6 · Conclusiones:** lo que el informe demuestra, sin análisis nuevo.
  - **Referencias** en APA 7, citadas en el texto.
- **Se califica en:** *Calidad documental* (0,5): narrativa integrada con los diagramas y APA 7.

### Paso 7 · Verificar antes de entregar

- **Cuándo:** antes de subir los diagramas y el informe.
- **Con qué:** la lista del **F-20**, condición por condición.
- **Se califica en:** *Calidad documental* (0,5).
- El **F-19** no lo llenan ustedes: es la rúbrica con la que el docente da la retroalimentación
  de la Actividad 2.1.

**No copien el caso: cópienle la estructura.** El ejemplo es de una IPS de salud; su
organización es otra.

---

## Qué hay en el repositorio

```text
AREM-S2_Modelado_y_Decision/
├── index.html      ← portada: desde aquí se abre todo lo demás
├── README.md
├── LICENSE
├── documentos/                 ← PDF, en el orden en que se usan
│   ├── 1_actividad_2_2/        ← qué se entrega y cómo se ve: mapa, informe de ejemplo, enunciado
│   ├── 2_caso/                 ← dossier de Red Salud Andina
│   ├── 3_como_se_hace/         ← instrumentos F-13 a F-20 y guías
│   └── 4_clase/                ← deck de la sesión
├── interactivos/               ← las siete herramientas HTML
└── modelo/                     ← el caso Red Salud Andina en Archi (.archimate y Open Exchange .xml)
```

### `documentos/` — PDF

Las carpetas están numeradas en el orden en que conviene abrirlas.

**`1_actividad_2_2/` — qué se entrega y cómo se ve.** Es la primera carpeta que se abre.

| Archivo | Descripción |
|---|---|
| [`AREM_S2_Mapa_Actividad_2_2.pdf`](documentos/1_actividad_2_2/AREM_S2_Mapa_Actividad_2_2.pdf) | Lo que pide la Actividad 2.2 en la plataforma, su rúbrica y, para cada requisito, la sección del informe, el formato que la prepara, cuándo se trabaja y dónde ver su ejemplo. |
| [`AREM_S2_Informe_Ejemplo_Actividad_2_2.pdf`](documentos/1_actividad_2_2/AREM_S2_Informe_Ejemplo_Actividad_2_2.pdf) | Un informe de la 2.2 terminado, sobre Red Salud Andina, con un recuadro por sección que explica qué hacer en ella, en qué criterio se califica y con qué formato se prepara. |
| [`AREM_S2_Enunciado_Actividad_2_2.pdf`](documentos/1_actividad_2_2/AREM_S2_Enunciado_Actividad_2_2.pdf) | El enunciado de las partes 1 y 2 que se trabajan en la sesión: objetivo, qué se produce, reparto del tiempo, ejemplos resueltos, qué las invalida y los conceptos que usan. |

**`2_caso/` — el caso de ejemplo.** El modelo en Archi está en [`modelo/`](#modelo--el-caso-en-archi).

| Archivo | Descripción |
|---|---|
| [`AREM_Caso_Red_Salud_Andina.pdf`](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf) | El dossier de la organización simulada de respaldo: identidad, sistemas, cifras, episodios, restricciones y las dos alternativas de la Unidad 2. |

**`3_como_se_hace/` — formatos y guías.** Los formatos se llenan; las guías se consultan.

| Archivo | Descripción |
|---|---|
| [`AREM_S2_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S2_Instrumentos.pdf) | Los ocho formatos F-13 a F-20, con el orden de llenado, la regla que invalida cada campo y la sección del informe a la que va. |
| [`AREM_S2_Guia_Visuales_e_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S2_Guia_Visuales_e_Instrumentos.pdf) | Cómo leer cada herramienta y cómo diligenciar cada formato, campo por campo. |
| [`AREM_S2_Guia_Archi_PasoAPaso.pdf`](documentos/3_como_se_hace/AREM_S2_Guia_Archi_PasoAPaso.pdf) | Archi, de la instalación a la exportación de imágenes, con las cuatro vistas paso a paso. |
| [`AREM_S2_Recorridos_Resueltos.pdf`](documentos/3_como_se_hace/AREM_S2_Recorridos_Resueltos.pdf) | Las siete herramientas recorridas paso a paso con Red Salud Andina, con lo que cada una deja en los formatos, y una ficha de Banco Colombia Digital. |

**`4_clase/` — la sesión.**

| Archivo | Descripción |
|---|---|
| [`AREM_S2_Deck_Reto_U2.pdf`](documentos/4_clase/AREM_S2_Deck_Reto_U2.pdf) | Las 20 diapositivas del encuentro sincrónico: tres conceptos, cada uno con su ejemplo en Red Salud Andina, el formato diligenciado y la comparación «cómo y por qué». |

### `interactivos/` — herramientas HTML

Son **autocontenidas**: todo el HTML, CSS y JavaScript va dentro de un solo archivo. No
requieren instalación, ni servidor, ni conexión a internet.

| Archivo | Para qué sirve | Paso |
|---|---|---|
| [`vistas_archimate_red_salud.html`](interactivos/vistas_archimate_red_salud.html) | Las cuatro vistas resueltas del caso Red Salud Andina, cada una con su *stakeholder*, su *concern* y la decisión que habilita, y tres contraejemplos diagnosticados. | 1 |
| [`archimate_interactivo.html`](interactivos/archimate_interactivo.html) | Capas, elementos y relaciones de ArchiMate 3.2, con ejemplos del caso bancario o de Red Salud Andina. El diccionario que se consulta mientras se modela. | 2 |
| [`atam_escenarios_interactivo.html`](interactivos/atam_escenarios_interactivo.html) | Constructor de escenarios de calidad (F-14), árbol de utilidad (F-15) y comparador de alternativas (F-16). | 3 |
| [`c4_model_interactivo.html`](interactivos/c4_model_interactivo.html) | Los cuatro niveles del C4 Model: las decisiones se toman en el nivel de contenedor y se pagan en el de componente. | 4 |
| [`costura_integracion_interactivo.html`](interactivos/costura_integracion_interactivo.html) | Las cuatro formas de resolver la costura de integración, comparadas campo por campo, con su acoplamiento real. | 4 |
| [`wardley_map_interactivo.html`](interactivos/wardley_map_interactivo.html) | Posición evolutiva de cada componente y la decisión de construir o consumir. | 4 |
| [`deuda_arquitectonica_interactivo.html`](interactivos/deuda_arquitectonica_interactivo.html) | Principal, interés mensual y la gráfica del mes en que el interés alcanza al principal. | 5 |

**Dos casos.** ArchiMate, C4 y Wardley abren con **Banco Colombia Digital**, el caso
transversal del curso, y traen arriba un selector **«Caso del ejemplo»** para cambiar a **Red
Salud Andina**. Para abrirlas directamente en Red Salud Andina, agreguen `?caso=red-salud` al
final de la dirección; por ejemplo,
`https://cesaravegaf312.github.io/AREM-S2_Modelado_y_Decision/interactivos/c4_model_interactivo.html?caso=red-salud`.
Las otras cuatro herramientas trabajan con Red Salud Andina desde el inicio.

### `modelo/` — el caso en Archi

El mismo modelo en dos formatos. **Cada uno se abre por un menú distinto:**

| Archivo | Formato | Menú en Archi |
|---|---|---|
| [`AREM_S2_Modelo_Red_Salud_Andina.archimate`](modelo/AREM_S2_Modelo_Red_Salud_Andina.archimate) | Nativo de Archi | `File → Open` |
| [`AREM_S2_Modelo_Red_Salud_Andina_OpenExchange.xml`](modelo/AREM_S2_Modelo_Red_Salud_Andina_OpenExchange.xml) | Estándar de The Open Group, validado contra su esquema. También lo abren otras herramientas ArchiMate. | `File → Import → Model From Open Exchange File…` |

Contiene 41 elementos, 39 relaciones y las cuatro vistas armadas y **encadenadas**: cada vista comparte al menos un elemento con otra. Hagan clic en un elemento y
miren **Properties → Documentation**: la mayoría explica por qué ese elemento está en el
modelo, y la documentación de **cada vista** trae su *stakeholder*, su *concern*, su punto de
vista, su fase del ADM y la decisión que habilita.

> El modelo está en **ArchiMate 3.2**, que es la versión que implementa Archi y en la que se
> entrega la Actividad 2.2. El estándar publicado es ArchiMate 4; esa diferencia se discute en
> la sesión y es, ella misma, un ejemplo de deuda arquitectónica declarada.

> La Sesión 1 —marcos de referencia y capacidades— está en su propio repositorio:
> [AREM-S1_Marcos_y_Capacidades](https://github.com/CesarAVegaF312/AREM-S1_Marcos_y_Capacidades-repositorio).
> Allí está el **TOGAF ADM interactivo**, que se reutiliza en esta sesión para ubicar las
> fases B a E.

---

## Problemas frecuentes

**Archi muestra «Error Importing cvc-elt.1.a: No se ha encontrado la declaración del elemento
'archimate:model'».**
Se usó `File → Import` con el archivo `.archimate`. Ese menú solo acepta el `.xml` de Open
Exchange. Cancelen y abran el `.archimate` con `File → Open`.

**Al hacer clic en un `.html` dentro de GitHub se ve código, no la herramienta.**
GitHub muestra el código fuente, no lo ejecuta. Descarguen el repositorio y ábranlo desde su
computador, o usen el enlace publicado que comparte el docente.

**El doble clic sobre un `.html` abre un editor de texto.**
Clic derecho → **Abrir con** → Chrome, Edge o Firefox.

**Solo necesito una herramienta.**
En GitHub, abran el archivo `.html`, entren a la vista **Raw** y guarden la página con
`Ctrl + S` (`Cmd + S` en Mac). Luego ábranla con doble clic.

---

## Requisitos

- Cualquier navegador moderno: Chrome, Edge, Firefox o Safari, en versiones recientes. No se
  requiere internet una vez descargados los archivos.
- Para el modelo, **Archi 5.x**, gratuito.

---

## Para el docente: publicar con GitHub Pages

Con GitHub Pages las herramientas se abren con un enlace, sin descargar nada. Se activa una
sola vez:

1. En el repositorio, pestaña **`Settings`** → menú lateral **`Pages`** (sección
   *Code and automation*).
2. En **Build and deployment → Source**, elegir **`Deploy from a branch`**.
3. En **Branch**, seleccionar **`main`** y carpeta **`/ (root)`**. Pulsar **`Save`**.
4. Esperar 1–2 minutos. La misma página muestra el aviso *"Your site is live at …"*.

Basta un solo enlace para los estudiantes, porque el repositorio trae portada:

- **Portada:** `https://cesaravegaf312.github.io/AREM-S2_Modelado_y_Decision/`
- **Una herramienta suelta:** `…/interactivos/<nombre_del_archivo>.html`

> - El repositorio debe ser **público** para usar Pages con una cuenta gratuita.
> - Si aparece **404**, revisar que el despliegue haya terminado y que el nombre del archivo
>   esté escrito exactamente igual, con la carpeta `interactivos/` y respetando mayúsculas.
> - Cada `git push` a `main` vuelve a desplegar el sitio.

---

## Referencias

- Bass, L., Clements, P., & Kazman, R. (2003). *Software architecture in practice* (2.ª ed.).
  Addison-Wesley.
- Fowler, M. (2004). *Strangler fig application*. martinfowler.com.
  <https://martinfowler.com/bliki/StranglerFigApplication.html>
- Hohpe, G., & Woolf, B. (2003). *Enterprise integration patterns: Designing, building, and
  deploying messaging solutions*. Addison-Wesley.
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and
  analysis* (4.ª ed.). Springer. <https://doi.org/10.1007/978-3-662-53933-0>
- Newman, S. (2021). *Building microservices: Designing fine-grained systems* (2.ª ed.).
  O'Reilly Media.
- The Open Group. (2022). *ArchiMate® 3.2 specification*. The Open Group.
  <https://www.opengroup.org/sites/default/files/docs/downloads/n221p.pdf>

---

## Licencia

Publicado bajo la **Licencia MIT** — ver [`LICENSE`](LICENSE).

Pueden usar, adaptar y redistribuir este material, incluido el código de los interactivos,
conservando el aviso de copyright y la atribución.

*Nota: TOGAF® y ArchiMate® son marcas registradas de The Open Group. Este repositorio contiene
material docente que los explica; la licencia MIT aplica a estos materiales, no a los marcos
originales. Los casos —Banco Colombia Digital y Red Salud Andina— son organizaciones simuladas
con fines pedagógicos.*
