@echo off
cd /d "%~dp0"
echo ==============================================
echo   TestDeArte - verificacion de imagenes
 echo ==============================================
py tools\validate_images.py
pause
