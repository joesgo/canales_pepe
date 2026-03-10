import requests
import re
import os
from datetime import datetime

# --- CONFIGURACION ---
ARCHIVO_FUENTES = "fuentes.txt"
ARCHIVO_SALIDA = "lista_combo.m3u"
URL_PRINCIPAL = "https://raw.githubusercontent.com/joesgo/canales_pepe/main/lista_combo.m3u"
# ---------------------

print("INICIANDO PROCESO DE CURADO AUTOMATICO...")
print("="*50)

# Crear carpeta logs si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Archivo de log con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/curador_{timestamp}.txt"

# 1. Descargar la lista principal
print("Descargando lista principal...")
try:
    respuesta_principal = requests.get(URL_PRINCIPAL, timeout=10)
    lineas_principales = respuesta_principal.text.splitlines()
    print(f"   OK - Descargada ({len(lineas_principales)} lineas)")
except Exception as e:
    print(f"ERROR al descargar: {e}")
    input("\nPresiona ENTER para salir...")
    exit()

# 2. Extraer nombres de canales
canales_a_buscar = []
for linea in lineas_principales:
    if linea.startswith("#EXTINF:"):
        partes = linea.split(",")
        if len(partes) > 1:
            canales_a_buscar.append(partes[-1].strip())

print(f"Buscando reemplazo para {len(canales_a_buscar)} canales")

# 3. Leer fuentes
try:
    with open(ARCHIVO_FUENTES, 'r') as f:
        urls_fuente = [linea.strip() for linea in f if linea.strip()]
    print(f"Usando {len(urls_fuente)} listas de repuesto:")
    for url in urls_fuente:
        print(f"   - {url}")
except FileNotFoundError:
    print(f"ERROR: No se encuentra el archivo {ARCHIVO_FUENTES}")
    input("\nPresiona ENTER para salir...")
    exit()

print()

# 4. Buscar reemplazos
canales_encontrados = 0
canales_no_encontrados = []

with open(log_file, 'w', encoding='utf-8') as log:
    log.write(f"CURADOR - {datetime.now()}\n")
    log.write("="*50 + "\n\n")
    
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as salida:
        
        for i, canal_buscado in enumerate(canales_a_buscar, 1):
            print(f"  [{i}/{len(canales_a_buscar)}] Buscando '{canal_buscado[:30]}...'", end=" ")
            encontrado = False
            
            for url_fuente in urls_fuente:
                if encontrado:
                    break
                try:
                    respuesta_fuente = requests.get(url_fuente, timeout=5)
                    lineas_fuente = respuesta_fuente.text.splitlines()
                    
                    j = 0
                    while j < len(lineas_fuente):
                        linea = lineas_fuente[j]
                        if linea.startswith("#EXTINF:") and canal_buscado in linea:
                            salida.write(linea + "\n")
                            if j+1 < len(lineas_fuente):
                                salida.write(lineas_fuente[j+1] + "\n")
                            encontrado = True
                            canales_encontrados += 1
                            log.write(f"OK Encontrado: {linea}\n")
                            log.write(f"   Fuente: {url_fuente}\n\n")
                            break
                        j += 1
                except Exception as e:
                    log.write(f"Error con {url_fuente}: {e}\n")
                    continue
            
            if encontrado:
                print("OK")
            else:
                print("NO ENCONTRADO")
                canales_no_encontrados.append(canal_buscado)
                log.write(f"NO Encontrado: {canal_buscado}\n\n")

# 5. Resumen final
print("\n" + "="*50)
print("PROCESO COMPLETADO")
print("="*50)
print(f"Canales procesados: {len(canales_a_buscar)}")
print(f"Canales encontrados: {canales_encontrados}")
print(f"Canales no encontrados: {len(canales_no_encontrados)}")
print(f"Nueva lista guardada en: {ARCHIVO_SALIDA}")
print(f"Log guardado en: {log_file}")
print("="*50)

if canales_no_encontrados:
    print("\nCanales que NO se encontraron (primeros 10):")
    for canal in canales_no_encontrados[:10]:
        print(f"   - {canal}")
    if len(canales_no_encontrados) > 10:
        print(f"   ... y {len(canales_no_encontrados)-10} mas")

input("\nPresiona ENTER para salir...")