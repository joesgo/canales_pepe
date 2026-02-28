@echo off
title SUPER ACTUALIZADOR DE CANALES
color 0A
cd /d "C:\Users\peper\Downloads\canales-pepe"

echo ========================================
echo    SUPER ACTUALIZADOR DE CANALES
echo ========================================
echo.

:: PASO 1: Ejecutar el validador de Python
echo [1/3] Validando canales de todas tus listas...
echo (Esto puede tardar unos minutos...)
python validador_canales.py

:: PASO 2: Subir a GitHub
echo.
echo [2/3] Subiendo cambios a GitHub...
git add .
git commit -m "Actualizacion automatica %date% - %time%"
git push

:: PASO 3: Mostrar resumen
echo.
echo [3/3] Proceso completado!
echo.
echo ========================================
echo   ¡LISTA COMBO ACTUALIZADA CON EXITO!
echo ========================================
echo.
echo ✅ Tu lista_combo.m3u tiene SOLO canales validos
echo ✅ Todos tus dispositivos se actualizaran
echo ✅ Revisa la carpeta /logs para mas detalles
echo.
pause