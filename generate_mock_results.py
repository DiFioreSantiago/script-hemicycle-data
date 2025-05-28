
import json
import pandas as pd
from collections import defaultdict
import re

# Archivos de entrada
DIPUTADOS_CSV_PATH = 'Votacion_Diputados.csv'
SENADORES_XLSX_PATH = 'Votacion_Senadores.xlsx'

# Archivos intermedios
DIPUTADOS_PATH = 'votacionDiputados.json'
SENADORES_PATH = 'votacionSenadores.json'

# Archivo final
OUTPUT_PATH = 'mockResults.json'

# Funciones de utilidad
def format_name_for_photo(name, tipo):
    base = re.sub(r"[^\w\s]", "", name.lower())
    base = "_".join(base.split())
    ext = ".jpg" if tipo == "diputado" else ".gif"
    folder = "fotosDiputados" if tipo == "diputado" else "fotosSenadores"
    return f"/{folder}/{base}{ext}"

def to_camel_case(text):
    return " ".join(word.capitalize() for word in text.lower().split())

# Colores por tipo de voto
VOTO_COLOURS = {
    'AFIRMATIVO': '#008000',
    'NEGATIVO': '#B71C1C',
    'ABSTENCION': '#FFD600',
    'AUSENTE': '#607D8B'
}

# Colores por partido - Diputados
PARTIDO_COLOURS_DIPUTADOS = {
    'Union Por La Patria': '#118CEF',
    'Pro': '#F9A825',
    'Frente De Izquierda Unidad': '#E53935',
    'La Libertad Avanza': '#8E24AA',
    'Otros': '#9E9E9E'
}

# Colores por partido - Senadores
PARTIDO_COLOURS_SENADORES = {
    'La Libertad Avanza': '#8E24AA',
    'Frente Nacional Y Popular': '#1976D2',
    'Unidad Ciudadana': '#1976D2',
    'Frente Pro': '#F9A825',
    'Unión Cívica Radical': '#FC4B08',
    'Otros': '#B0BEC5'
}

# Reemplazos para unificar nombres de bloques en Diputados
PARTY_REPLACEMENTS_DIPUTADOS = {
    'Pts-frente De Izquierda Unidad': 'Frente De Izquierda Unidad',
    'Partido Obrero -frente De Izquierda Y De Trabajadores -unidad': 'Frente De Izquierda Unidad',
    'Izquierda Socialista Fit-unidad': 'Frente De Izquierda Unidad'
}

# 1. Procesar diputados
diputados_df = pd.read_csv(DIPUTADOS_CSV_PATH)
diputados_data = []
for _, row in diputados_df.iterrows():
    nombre = row['DIPUTADO']
    bloque = PARTY_REPLACEMENTS_DIPUTADOS.get(row['BLOQUE'], row['BLOQUE'])
    diputados_data.append({
        "DIPUTADO": nombre,
        "BLOQUE": bloque,
        "PROVINCIA": row["PROVINCIA"],
        "VOTO": row["¿CÓMO VOTÓ?"],
        "FOTO": format_name_for_photo(nombre, "diputado")
    })

with open(DIPUTADOS_PATH, 'w', encoding='utf-8') as f:
    json.dump(diputados_data, f, indent=4, ensure_ascii=False)

# 2. Procesar senadores
senadores_df = pd.read_excel(SENADORES_XLSX_PATH, skiprows=5)
senadores_data = []
for _, row in senadores_df.iterrows():
    if pd.notna(row.get("Senador")):
        nombre = row["Senador"]
        bloque = to_camel_case(row["Bloque"])
        senadores_data.append({
            "SENADOR": nombre,
            "BLOQUE": bloque,
            "PROVINCIA": row["Provincia"],
            "VOTO": row["¿Cómo votó?"],
            "FOTO": format_name_for_photo(nombre, "senador")
        })

with open(SENADORES_PATH, 'w', encoding='utf-8') as f:
    json.dump(senadores_data, f, indent=4, ensure_ascii=False)

# 3. Función para calcular totales
def generar_totales(data, key_bloque, partidos_colores, main_parties):
    votos_totales = defaultdict(int)
    partidos_totales = defaultdict(lambda: defaultdict(int))
    for item in data:
        voto = item['VOTO']
        partido = item[key_bloque]
        if partido not in main_parties:
            partido = 'Otros'
        votos_totales[voto] += 1
        partidos_totales[partido][voto] += 1

    votos = {
        voto: {
            'name': voto,
            'seats': count,
            'colour': VOTO_COLOURS.get(voto, '#000000')
        } for voto, count in votos_totales.items()
    }
    partidos = {
        partido: {
            'name': partido,
            'seats': sum(vs.values()),
            'colour': partidos_colores.get(partido, partidos_colores.get('Otros', '#9E9E9E'))
        } for partido, vs in partidos_totales.items()
    }
    return {"votos": votos, "partidos": partidos}

# 4. Generar mockResults.json
mock_results = {
    "diputados": generar_totales(diputados_data, 'BLOQUE', PARTIDO_COLOURS_DIPUTADOS, set(PARTIDO_COLOURS_DIPUTADOS) - {'Otros'}),
    "senadores": generar_totales(senadores_data, 'BLOQUE', PARTIDO_COLOURS_SENADORES, set(PARTIDO_COLOURS_SENADORES) - {'Otros'})
}

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(mock_results, f, indent=4, ensure_ascii=False)

print("Archivo generado exitosamente: votacionDiputados.json, votacionSenadores.json y mockResults.json")
