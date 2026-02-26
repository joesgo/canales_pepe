@echo off
title GESTOR DE LISTAS CANALES PEPE
color 0A

cd /d "C:\peper\canales_pepe"

:menu
cls
echo ========================================
echo    GESTOR DE LISTAS DE CANALES
echo ========================================
echo.
echo 1. Ver listas disponibles
echo 2. Editar lista_combo.m3u (PRINCIPAL)
echo 3. Subir cambios a GitHub
echo 4. Salir
echo.
set /p opcion="Selecciona una opcion: "

if "%opcion%"=="1" goto ver_listas
if "%opcion%"=="2" goto editar
if "%opcion%"=="3" goto subir
if "%opcion%"=="4" exit
goto menu

:ver_listas
cls
echo ===== LISTAS DISPONIBLES =====
echo.
dir *.m3u /b
echo.
pause
goto menu

:editar
cls
echo EDITANDO lista_combo.m3u
echo (Se abrira el bloc de notas)
pause
notepad lista_combo.m3u
goto menu

:subir
cls
echo ===== SUBIENDO CAMBIOS A GITHUB =====
echo.

:: Verificar cambios
git status

:: Añadir todos los archivos .m3u
git add *.m3u
git add actualizar.bat

:: Hacer commit con fecha
set fecha=%DATE%
set hora=%TIME%
git commit -m "Actualizacion listas %fecha% - %hora%"

:: Subir a GitHub
git push

echo.
echo ¡LISTAS ACTUALIZADAS EN GITHUB!
echo.
pause
goto menu