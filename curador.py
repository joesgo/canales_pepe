import requests
import os
import re

print("="*60)
print("CURADOR DE CANALES - Version sin emojis")
print("="*60)

# Archivos
LISTA_PRINCIPAL = "lista_combo.m3u"
FUENTES = "fuentes.txt"
SALIDA = "lista_combo_nueva.m3u"

# 1. Leer lista principal
try:
    with open(LISTA_PRINCIPAL, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
except:
    print("ERROR: No se encuentra lista_combo.m3u")
    exit()

# Extraer nombres
nombres_originales = []
for linea in lineas:
    if linea.startswith("#EXTINF:"):
        nombre = linea.strip().split(",")[-1]
        nombres_originales.append(nombre)

print(f"\nCanales que quieres: {len(nombres_originales)}")

# 2. Leer fuentes
try:
    with open(FUENTES, 'r', encoding='utf-8') as f:
        urls = [linea.strip() for linea in f if linea.strip()]
    print(f"Fuentes: {len(urls)}")
except:
    print("ERROR: No se encuentra fuentes.txt")
    exit()

# 3. Función para limpiar nombres
def limpiar_nombre(nombre):
    nombre = nombre.lower()
    nombre = re.sub(r'\bes:?\s*|\bhd\b|\bfhd\b|\bsd\b|\b1080p\b|\b720p\b|\([^)]*\)', '', nombre)
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    return nombre

# 4. Buscar coincidencias
print("\nBuscando coincidencias...")
encontrados = 0
no_encontrados = []

with open(SALIDA, 'w', encoding='utf-8') as out:
    out.write("#EXTM3U\n")
    
    for idx, nombre in enumerate(nombres_originales, 1):
        nombre_limpio = limpiar_nombre(nombre)
        print(f"\n  [{idx}/{len(nombres_originales)}] {nombre[:40]}")
        print(f"     Buscando: '{nombre_limpio}'")
        
        hallado = False
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    continue
                lineas_fuente = r.text.splitlines()
                
                for i, linea in enumerate(lineas_fuente):
                    if linea.startswith("#EXTINF:"):
                        if nombre_limpio in linea.lower():
                            out.write(linea + "\n")
                            if i+1 < len(lineas_fuente):
                                out.write(lineas_fuente[i+1] + "\n")
                            hallado = True
                            encontrados += 1
                            print(f"     ENCONTRADO en: {url}")
                            break
                if hallado:
                    break
            except:
                continue
        
        if not hallado:
            no_encontrados.append(nombre)
            print(f"     NO ENCONTRADO")

# 5. Reemplazar lista antigua
os.replace(SALIDA, LISTA_PRINCIPAL)

# 6. Resumen
print("\n" + "="*60)
print("RESUMEN")
print("="*60)
print(f"Canales encontrados: {encontrados}")
print(f"Canales no encontrados: {len(no_encontrados)}")
if no_encontrados:
    print("\nCanales no encontrados (primeros 10):")
    for n in no_encontrados[:10]:
        print(f"   - {n}")
print("="*60)
input("\nPresiona ENTER para salir...")