@echo off
title ACTUALIZADOR COMPLETO DE CANALES
color 0A
cd /d "C:\Users\peper\Downloads\canales-pepe"

echo ========================================
echo    PROCESO COMPLETO DE ACTUALIZACION
echo ========================================
echo.

:: PASO 1: Ejecutar el curador (limpia canales malos)
echo [1/3] Limpiando canales malos y buscando reemplazos...
echo (Esto puede tardar varios minutos...)
echo.
python curador.py

:: PASO 2: Verificar que se genero la nueva lista
echo.
echo [2/3] Verificando nueva lista...
if exist "lista_combo.m3u" (
    echo ✅ Nueva lista_combo.m3u generada correctamente
) else (
    echo ❌ ERROR: No se genero la lista
    pause
    exit
)
echo.

:: PASO 3: Subir a GitHub
echo [3/3] Subiendo cambios a GitHub...
git add lista_combo.m3u
git commit -m "Actualizacion automatica %date% - %time%"
git push

echo.
echo ========================================
echo   ¡PROCESO COMPLETADO CON EXITO!
echo ========================================
echo.
echo ✅ Canales malos eliminados
echo ✅ Canales repetidos unificados
echo ✅ Lista subida a GitHub
echo.
echo 📁 Revisa la carpeta /logs para mas detalles@echo off
cd /d "C:\Users\peper\Downloads\canales-pepe"
python curador.py
git add .
git commit -m "Actualizacion automatica"
git push
echo Listo!
pause
echo.
pause