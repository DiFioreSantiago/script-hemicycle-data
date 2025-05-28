
# Generador de Resultados de Votaciones Legislativas

Este script en Python procesa archivos de votaciones de diputados y senadores de Argentina para generar archivos JSON estructurados. Estos archivos se utilizan en el proyecto de visualización interactiva de votaciones en formato de hemiciclo:  
🔗 [Visualización de Votaciones - Frontend](https://github.com/tu-usuario/repositorio-frontend)

---

## 🧩 ¿Qué hace este script?

A partir de dos archivos de entrada:

- `Votacion_Diputados.csv` exportado desde la pagina oficial de [Votaciones de la Camara de Diputados](https://votaciones.hcdn.gob.ar/)
- `Votacion_Senadores.xlsx` exportado desde la pagina oficial de [Votaciones de la Camara de Senadores](https://www.senado.gob.ar/votaciones/actas)

El script genera automáticamente:

- `votacionDiputados.json` → detalle voto por voto de diputados.
- `votacionSenadores.json` → detalle voto por voto de senadores.
- `mockResults.json` → resumen por tipo de voto y por bloque.

Los datos se enriquecen con nombres estandarizados, colores por partido o tipo de voto, y rutas a imágenes de cada legislador/a.

---

## 🛠️ Requisitos

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) (para procesar archivos .xlsx)

Instalación de dependencias recomendada:

```bash
pip install pandas openpyxl
```

---

## 🚀 Cómo usar

1. De las paginas oficiales de [Votaciones de la Camara de Diputados](https://votaciones.hcdn.gob.ar/) y [Votaciones de la Camara de Senadores](https://www.senado.gob.ar/votaciones/actas) descargar los archivos para un proyecto de ley deseado. Por lo general el titulo para buscar el proyecto coincicide tanto en el sitio Diputados como en el de Senadores. Una vez descargados (para Diputados sera un archivo .csv y para Senadores un .xlsx) se deberan renombrar como `Votacion_Diputados.csv` y `Votacion_Senadores.xlsx` correspondientemente.

2. Colocá en la raíz del proyecto los archivos:

   - `Votacion_Diputados.csv`
   - `Votacion_Senadores.xlsx`

3. Ejecutá el script:

```bash
python generate_mock_results.py
```

4. Se generarán automáticamente los archivos de salida en el mismo directorio:

- `votacionDiputados.json`
- `votacionSenadores.json`
- `mockResults.json`

5. Una vez generados los archivos los mismos pueden ser colocados en el repositorio para los [Datos y API](https://github.com/DiFioreSantiago/api-hemicycle-widget)

---

## 📁 Estructura esperada de los archivos

### `Votacion_Diputados.csv`

Debe contener las siguientes columnas:

- `DIPUTADO`
- `BLOQUE`
- `PROVINCIA`
- `¿CÓMO VOTÓ?`

### `Votacion_Senadores.xlsx`

- La hoja debe comenzar en la fila 6 (el script salta las primeras 5).
- Columnas esperadas:
  - `Senador`
  - `Bloque`
  - `Provincia`
  - `¿Cómo votó?`

---

## 📦 Archivos generados

### `votacionDiputados.json` y `votacionSenadores.json`

Cada objeto incluye:

```json
{
  "DIPUTADO": "Nombre Apellido",
  "BLOQUE": "Nombre del Bloque",
  "PROVINCIA": "Provincia",
  "VOTO": "AFIRMATIVO | NEGATIVO | ABSTENCION | AUSENTE",
  "FOTO": "/fotosDiputados/nombre_apellido.jpg"
}
```

(Para senadores, la clave principal es `SENADOR` y la carpeta de fotos cambia).

### `mockResults.json`

Resumen por cámara:

```json
{
  "diputados": {
    "votos": { "AFIRMATIVO": {...}, "NEGATIVO": {...}, ... },
    "partidos": { "Pro": {...}, "Union Por La Patria": {...}, ... }
  },
  "senadores": { ... }
}
```

Incluye colores y totales por categoría.

---

## 📎 Notas adicionales

- Las fotos se enlazan automáticamente a partir del nombre del legislador.
- Los nombres de partidos se normalizan para evitar duplicados con diferentes formas de escritura.
- Este script es parte del pipeline de datos del proyecto principal de visualización de votaciones.

---

## 🛡️ Licencia

Este script está bajo la Licencia MIT.
