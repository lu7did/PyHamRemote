PyHamRemote

Repositorio con utilitarios, scripts y pequeñas aplicaciones destinados a la automatización y análisis para estaciones de radioaficionado, con enfoque en concursos (contest), DX y visualización de condiciones de propagación.

Contenido y módulos principales

- CONDXmap/
  - Propósito: Procesado de datos PSK/FT8/ADIF y generación de mapas/visualizaciones de condiciones de propagación.
  - Archivos clave: condxmap.py (generación de mapas), adif2json.py (conversión ADIF→JSON), csv2json.py, csv2data.py, grid2geo.py.
  - Datos y salidas: CONDXmap/data (ficheros PSK/FT8/ADIF y CSV de ejemplo), CONDXmap/out (imágenes y GIFs generados).
  - Uso: ejecutar los scripts en este directorio sobre los ficheros en data para regenerar imágenes en out; revisar CONDXmap/README.md para ejemplos concretos.

- PyMeter/
  - Propósito: Pequeña aplicación de medidor/GUI para monitorizar niveles de señal y utilidades relacionadas.
  - Archivos clave: PyMeter/PyMeter.py (aplicación principal), PyMeter/scripts/PyMeter (lanzador), PyMeter/scripts/install.sh (instalador y dependencias), PyMeter/PyMeter.ini (configuración), recursos en PyMeter/misc.
  - Uso: ejecutar el script instalador y lanzar el binario/script apropiado para la plataforma; revisar PyMeter/README.md para instrucciones detalladas.

- dx_proxy/
  - Propósito: Proxy/servicio para el manejo y re-distribución de spots DX o datos relacionados con cat/servidores.
  - Archivos clave: dx_proxy/dx_proxy.py (implementación principal), dx_proxy/pyc.cmd.
  - Uso: revisar el código para adaptarlo al entorno de red/local; puede actuar como intermediario para sistemas que consumen información DX.

- pycat/
  - Propósito: Utilidad auxiliar ligera (similar a cat pero en Python) para tareas sencillas de inspección.
  - Archivos clave: pycat/pycat.py

Otros ficheros y documentación

- CONTEXT.md: información de contexto y notas del proyecto.
- LICENSE: licencia del proyecto.
- README.md en subdirectorios (CONDXmap/README.md, PyMeter/README.md): documentación específica por módulo.

Instalación general y ejecución rápida

1. Clonar el repositorio y moverse al directorio del proyecto.
2. Revisar los README.md dentro de los subdirectorios para dependencias específicas (por ejemplo, librerías gráficas para CONDXmap o requisitos de PyMeter).
3. Para PyMeter: ejecutar PyMeter/scripts/install.sh si se dispone de un entorno Unix compatible; luego lanzar PyMeter/scripts/PyMeter o PyMeter/PyMeter.py.
4. Para CONDXmap: ejecutar los scripts de procesamiento sobre los ficheros en CONDXmap/data para generar las imágenes en CONDXmap/out.

Contribuir

- Abrir issues para bugs o mejoras.
- Enviar pull requests con descripciones claras de los cambios y pruebas cuando sea posible.

Licencia

Ver fichero LICENSE en la raíz del proyecto.

Última actualización: 2025-12-10T18:14:42.327Z
