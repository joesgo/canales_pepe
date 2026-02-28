import requests
import os
import time
from datetime import datetime

print("="*50)
print("VALIDADOR DE CANALES - VERSIÓN ESPAÑOL")
print("="*50)

# Lista de archivos fuente (TUS LISTAS)
fuentes = ["jose1.m3u", "jose2.m3u", "jose3.m3u", "lista_buena.m3u"]
archivo_salida = "lista_combo.m3u"

# Crear carpeta logs si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Iniciar log
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/validacion_{timestamp}.txt"

def validar_url(url):
    """Verifica si una URL responde correctamente"""
    try:
        response = requests.get(url, timeout=5, stream=True)
        return response.status_code == 200
    except:
        return False

print(f"\n📂 Leyendo archivos fuente: {', '.join(fuentes)}")
print("⏳ Esto puede tardar unos minutos...\n")

total_canales = 0
canales_validos = 0

with open(log_file, "w", encoding="utf-8") as log:
    log.write(f"VALIDACIÓN - {datetime.now()}\n")
    log.write("="*50 + "\n\n")
    
    with open(archivo_salida, "w", encoding="utf-8") as salida:
        
        for fuente in fuentes:
            if not os.path.exists(fuente):
                print(f"⚠️  Archivo no encontrado: {fuente}")
                continue
                
            print(f"Procesando: {fuente}")
            with open(fuente, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                
            i = 0
            while i < len(lineas):
                linea = lineas[i].strip()
                
                # Si es línea de información del canal
                if linea.startswith("#EXTINF:"):
                    info_canal = linea
                    i += 1
                    if i < len(lineas):
                        url = lineas[i].strip()
                        
                        # Validar la URL
                        total_canales += 1
                        if validar_url(url):
                            canales_validos += 1
                            # Guardar canal válido
                            salida.write(info_canal + "\n")
                            salida.write(url + "\n")
                            log.write(f"✅ VÁLIDO: {info_canal}\n")
                            log.write(f"   URL: {url}\n\n")
                            print(f"  ✅ Canal válido encontrado")
                        else:
                            log.write(f"❌ FALLÓ: {info_canal}\n")
                            log.write(f"   URL: {url}\n\n")
                            print(f"  ❌ Canal falló")
                else:
                    i += 1

print("\n" + "="*50)
print(f"✅ PROCESO COMPLETADO")
print("="*50)
print(f"📊 Total canales procesados: {total_canales}")
print(f"✅ Canales válidos encontrados: {canales_validos}")
print(f"❌ Canales fallidos: {total_canales - canales_validos}")
print(f"📁 Nueva lista guardada en: {archivo_salida}")
print(f"📝 Log guardado en: {log_file}")
print("="*50)