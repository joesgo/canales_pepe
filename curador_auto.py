import requests
import os

print("🚀 Iniciando curador automático REAL...")

# 1. Leer fuentes
try:
    with open("fuentes.txt", "r") as f:
        fuentes = [linea.strip() for linea in f if linea.strip()]
    print(f"📚 Usando {len(fuentes)} fuentes.")
except FileNotFoundError:
    print("❌ Error: No se encuentra fuentes.txt")
    exit(1)

# 2. Leer lista actual para saber qué canales buscar
try:
    with open("lista_combo.m3u", "r") as f:
        lineas_actuales = f.readlines()
    print(f"📄 Lista actual leída con {len(lineas_actuales)} líneas.")
except FileNotFoundError:
    print("❌ Error: No se encuentra lista_combo.m3u")
    exit(1)

# 3. Extraer nombres de canales
canales_a_buscar = []
for linea in lineas_actuales:
    if linea.startswith("#EXTINF:"):
        # Extrae el nombre del canal (después de la última coma)
        nombre_canal = linea.strip().split(",")[-1]
        canales_a_buscar.append(nombre_canal)

print(f"🔍 Se buscarán {len(canales_a_buscar)} canales en las fuentes...")

# 4. BUSCAR CANALES REALES en las fuentes
canales_encontrados = 0
with open("lista_combo_nueva.m3u", "w", encoding='utf-8') as salida:
    
    for i, canal_buscado in enumerate(canales_a_buscar, 1):
        print(f"  [{i}/{len(canales_a_buscar)}] Buscando '{canal_buscado[:30]}...'", end=" ")
        encontrado = False
        
        # Buscar en cada fuente
        for url_fuente in fuentes:
            if encontrado:
                break
            try:
                # Descargar la lista fuente
                respuesta = requests.get(url_fuente, timeout=10)
                lineas_fuente = respuesta.text.splitlines()
                
                # Buscar el canal en esta fuente
                j = 0
                while j < len(lineas_fuente):
                    linea = lineas_fuente[j]
                    if linea.startswith("#EXTINF:") and canal_buscado in linea:
                        # Encontrado: guardar info y URL
                        salida.write(linea + "\n")
                        if j+1 < len(lineas_fuente):
                            salida.write(lineas_fuente[j+1] + "\n")
                        encontrado = True
                        canales_encontrados += 1
                        break
                    j += 1
            except Exception as e:
                continue  # Si falla una fuente, probar la siguiente
        
        if encontrado:
            print("✅")
        else:
            print("❌ No encontrado")

# 5. Reemplazar la lista antigua con la nueva
os.replace("lista_combo_nueva.m3u", "lista_combo.m3u")

print("\n" + "="*50)
print("✅ PROCESO COMPLETADO")
print("="*50)
print(f"📊 Canales procesados: {len(canales_a_buscar)}")
print(f"✅ Canales encontrados: {canales_encontrados}")
print(f"❌ Canales no encontrados: {len(canales_a_buscar) - canales_encontrados}")
print(f"📁 Nueva lista guardada en: lista_combo.m3u")