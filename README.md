# AREM S2 — Modelado y Decisión

Material de la **Sesión 2** del curso *Arquitectura Empresarial* (AREM), Unidad 2:
**Modelado Empresarial y Arquitectura de Integración**.

La unidad va de representar formalmente una arquitectura a **decidir entre dos caminos
defendibles y declarar qué se sacrifica**. Marco de referencia: **TOGAF® Standard,
10.ª edición**. Lenguaje de modelado: **ArchiMate® 3.2**.

Incluye **siete recursos interactivos en HTML**, un **modelo de Archi** con el caso
resuelto, los formatos de la unidad y las guías de trabajo.

---

## Contenido

### Recursos interactivos

| Archivo | Descripción |
|---|---|
| [`archimate_interactivo.html`](archimate_interactivo.html) | Las capas, elementos y relaciones de **ArchiMate 3.2**, con ejemplos del caso bancario. Es el diccionario que se consulta mientras se modela. |
| [`vistas_archimate_red_salud.html`](vistas_archimate_red_salud.html) | **Las cuatro vistas resueltas** del caso Red Salud Andina, cada una con su *stakeholder*, su *concern* y la decisión que habilita. Incluye tres **contraejemplos** diagnosticados. |
| [`c4_model_interactivo.html`](c4_model_interactivo.html) | Los cuatro niveles del **C4 Model**. Muestra por qué la vista de aplicación no alcanza para decidir: las decisiones se toman en el nivel de contenedor y se pagan en el de componente. |
| [`atam_escenarios_interactivo.html`](atam_escenarios_interactivo.html) | Constructor de **escenarios de calidad (F-14)**, **árbol de utilidad (F-15)** y **comparador de alternativas (F-16)**. No deja registrar un escenario sin medida ni cerrar la decisión sin la renuncia. Genera el texto para pegar en el informe. |
| [`wardley_map_interactivo.html`](wardley_map_interactivo.html) | **Mapa de Wardley**: la posición evolutiva de cada componente y la decisión de construir o consumir. |
| [`costura_integracion_interactivo.html`](costura_integracion_interactivo.html) | Las **cuatro formas de resolver la costura de integración** comparadas campo por campo, con su consecuencia real de acoplamiento. |
| [`deuda_arquitectonica_interactivo.html`](deuda_arquitectonica_interactivo.html) | Registro de **deuda arquitectónica**: principal, interés mensual y la gráfica del mes en que el interés supera al principal. |

### Modelo y documentos

| Archivo | Tipo | Descripción |
|---|---|---|
| [`AREM_S2_Modelo_Red_Salud_Andina.archimate`](AREM_S2_Modelo_Red_Salud_Andina.archimate) | Modelo de Archi | El caso completo: 41 elementos, 38 relaciones y las cuatro vistas armadas. Cada elemento lleva documentación. |
| [`AREM_S2_Instrumentos.pdf`](AREM_S2_Instrumentos.pdf) | PDF · se llena | Los ocho formatos **F-13 a F-20**, con el orden de llenado y la regla que invalida cada campo. |
| [`AREM_S2_Guia_Archi_PasoAPaso.pdf`](AREM_S2_Guia_Archi_PasoAPaso.pdf) | PDF · guía | Archi, de la instalación a la exportación de imágenes, con las cuatro vistas paso a paso. |
| [`AREM_S2_Guia_Visuales_e_Instrumentos.pdf`](AREM_S2_Guia_Visuales_e_Instrumentos.pdf) | PDF · guía | Cómo leer cada herramienta y cómo diligenciar cada formato, campo por campo, con una fila resuelta. |
| [`AREM_S2_Deck_Reto_U2.pdf`](AREM_S2_Deck_Reto_U2.pdf) | PDF | Las 30 diapositivas del encuentro sincrónico. |

> La Sesión 1 —marcos de referencia y capacidades— está en su propio repositorio:
> [AREM-S1_Marcos_y_Capacidades](https://github.com/CesarAVegaF312/AREM-S1_Marcos_y_Capacidades-repositorio).
> Allí está el **TOGAF ADM interactivo**, que se reutiliza en esta sesión para abrir las
> fases C, D y E.

---

## Cómo abrir los interactivos

Los siete archivos `.html` son **autocontenidos**: todo el HTML, CSS y JavaScript va
dentro de un solo archivo. No requieren instalación, ni servidor, ni conexión a
internet, ni dependencias externas.

### Opción 1 — Desde el computador (recomendada)

1. Descarga el repositorio: botón verde **`Code` → `Download ZIP`**, y descomprímelo.
   (O clónalo: `git clone https://github.com/CesarAVegaF312/AREM-S2_Modelado_y_Decision-repositorio.git`)
2. Entra a la carpeta y haz **doble clic** sobre `index.html` para ver la portada con
   todo, o sobre cualquiera de los `.html` para abrirlo directamente.
3. Se abrirá en tu navegador por defecto. Listo.

> Si el doble clic abre otro programa (por ejemplo un editor de texto): clic derecho →
> **Abrir con** → Chrome / Edge / Firefox.

### Opción 2 — Descargar un solo archivo

En GitHub, abre el archivo `.html`, entra a la vista **Raw** y guarda la página con
`Ctrl + S` (`Cmd + S` en Mac). Luego ábrela con doble clic.

> ⚠️ Al hacer clic sobre un `.html` **dentro de GitHub no se ve el interactivo**:
> GitHub muestra el código fuente, no lo ejecuta. Hay que descargarlo o publicarlo
> con GitHub Pages (Opción 3).

### Opción 3 — En línea con GitHub Pages

Con **GitHub Pages** los interactivos se abren con un solo link, sin descargar nada.
Requiere activarlo una vez (lo hace el dueño del repositorio):

1. En el repositorio, entra a la pestaña **`Settings`** (arriba a la derecha).
2. En el menú lateral izquierdo, baja hasta **`Pages`** (sección *Code and automation*).
3. En **Build and deployment → Source**, elige **`Deploy from a branch`**.
4. En **Branch**, selecciona **`main`** y carpeta **`/ (root)`**. Pulsa **`Save`**.
5. Espera 1–2 minutos. Al terminar, la misma página de *Pages* muestra el enlace del
   sitio con un aviso verde: *"Your site is live at …"*.

Una vez activado, **basta un solo enlace para los estudiantes**, porque el repositorio
trae una portada:

- **Portada con todo:** https://cesaravegaf312.github.io/AREM-S2_Modelado_y_Decision-repositorio/

Y si quieres enlazar una herramienta suelta:

| Herramienta | Enlace |
|---|---|
| ArchiMate 3.2 | `…/archimate_interactivo.html` |
| Las cuatro vistas | `…/vistas_archimate_red_salud.html` |
| C4 Model | `…/c4_model_interactivo.html` |
| Escenarios ATAM | `…/atam_escenarios_interactivo.html` |
| Wardley Map | `…/wardley_map_interactivo.html` |
| Costura de integración | `…/costura_integracion_interactivo.html` |
| Deuda arquitectónica | `…/deuda_arquitectonica_interactivo.html` |

> **Notas**
> - El repositorio debe ser **público** para usar Pages con una cuenta gratuita.
> - Si obtienes **404**, revisa que el despliegue haya terminado y que el nombre del
>   archivo en el link esté escrito exactamente igual (distingue mayúsculas).
> - Cada `git push` a `main` vuelve a desplegar el sitio automáticamente.

---

## Cómo abrir el modelo de Archi

1. Descarga **Archi** de [archimatetool.com](https://www.archimatetool.com) → *Downloads*.
   Es gratuito y de código abierto.
2. Abre Archi y usa `File → Open`, y elige `AREM_S2_Modelo_Red_Salud_Andina.archimate`.
3. En el árbol de la izquierda, despliega **Views** y abre las cuatro vistas.

Haz clic en cualquier elemento y mira la pestaña **Properties → Documentation**: ahí está
escrito por qué ese elemento está en el modelo. La documentación de **cada vista** trae su
*stakeholder*, su *concern*, su punto de vista, su fase del ADM y la decisión que habilita.

> El modelo está en **ArchiMate 3.2**, que es la versión que implementa Archi. El estándar
> publicado es ArchiMate 4; esa diferencia se discute en la sesión y es, ella misma, un
> ejemplo de deuda arquitectónica declarada.

**No copies el caso: cópiale la estructura.** El modelo es de una IPS de salud; tu
organización es otra.

---

## Cómo usarlos durante la unidad

El orden importa, y es el contrario al que la mayoría intenta:

1. **Decide qué vistas van** y llena el **F-13** — fuera de Archi. Apóyate en
   `vistas_archimate_red_salud.html` y en el modelo de ejemplo.
2. **Modela las cuatro vistas** en Archi, con `archimate_interactivo.html` al lado y la
   guía paso a paso abierta.
3. **Construye los escenarios de calidad** con `atam_escenarios_interactivo.html`:
   llena el F-14, cuelga el árbol de utilidad (F-15) y compara las dos alternativas (F-16).
4. **Elige la costura de integración** con `costura_integracion_interactivo.html` y
   `c4_model_interactivo.html`, y llena el F-17 con `wardley_map_interactivo.html`.
5. **Registra la deuda** que queda viva con `deuda_arquitectonica_interactivo.html` (F-18).
6. **Verifica antes de entregar** con la lista del F-20.

Quien abre Archi antes de llenar el F-13 dibuja dos veces: una para descubrir qué quería
mostrar y otra para mostrarlo.

---

## Requisitos

Cualquier navegador moderno: Chrome, Edge, Firefox o Safari (versiones recientes).
No se requiere internet una vez descargados los archivos.
Para el modelo, **Archi 5.x** (gratuito).

---

## Licencia

Publicado bajo la **Licencia MIT** — ver [`LICENSE`](LICENSE).

Puedes usar, adaptar y redistribuir este material (incluido el código de los
interactivos) libremente, conservando el aviso de copyright y la atribución.

*Nota: TOGAF® y ArchiMate® son marcas registradas de The Open Group. Este repositorio
contiene material docente que los explica; la licencia MIT aplica a estos materiales, no
a los marcos originales. Los casos —Banco Colombia Digital y Red Salud Andina— son
organizaciones simuladas con fines pedagógicos.*
