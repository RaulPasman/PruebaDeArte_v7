@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==============================================
echo   Prueba de Arte - descarga de imagenes (v7)
echo ==============================================
echo.
py -c "import PIL" 2>nul || (echo Instalando Pillow... & py -m pip install --quiet pillow)
py tools\fetch_images.py %*
if errorlevel 1 (
  echo.
  echo Quedaron obras sin imagen. Mira la lista de arriba.
  echo Podes volver a ejecutar este archivo: retoma donde quedo.
) else (
  echo.
  echo TODAS LAS IMAGENES ESTAN LISTAS.
)
if exist REVISAR_IMAGENES.html start "" REVISAR_IMAGENES.html
pause
