@echo off
cd /d "%~dp0"
start "servidor" /min py -m http.server 8000
timeout /t 2 >nul
start "" http://localhost:8000
echo La prueba esta corriendo en http://localhost:8000  (cerra la ventana minimizada "servidor" para detenerla)
pause
