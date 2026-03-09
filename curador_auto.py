# Script curador
import requests
import os

print("🚀 Iniciando curador automático...")

# 1. Leer fuentes
try:
    with open("fuentes.txt", "r") as f:
        fuentes = [linea.strip() for linea in f if linea.strip()]
    print(f"📚 Usando {len(fuentes)} fuentes.")
except FileNotFoundError:
    print("❌ Error: No se encuentra fuentes.txt")
    exit(1)

# 2. Leer lista actual
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
        nombre_canal = linea.strip().split(",")[-1]
        canales_a_buscar.append(nombre_canal)

print(f"🔍 Se buscarán {len(canales_a_buscar)} canales...")

# 4. Buscar reemplazos (simulado)
print("⏳ Simulando búsqueda de reemplazos...")
canales_encontrados = 0
with open("lista_combo_nueva.m3u", "w") as salida:
    for i, canal in enumerate(canales_a_buscar):
        if i % 10 != 0:
            salida.write(f"#EXTINF:-1,{canal}\n")
            salida.write(f"http://url-ejemplo.com/{canal}\n")
            canales_encontrados += 1

print(f"✅ Simulación completa. {canales_encontrados} canales 'encontrados'.")

# 5. Reemplazar la lista antigua
os.replace("lista_combo_nueva.m3u", "lista_combo.m3u")
print("🎉 Nueva lista_combo.m3u generada.")