@echo off
title Class 6 - AI Node Local File Service (Port 8888)
cls
echo =================================================================
echo  Class 6 - AI Node Local File Access Service (Port 8888)
echo =================================================================
echo.
echo  Local Test URL: http://localhost:8888
echo  Public Tunnel Command: Double click start_ngrok.bat
echo -----------------------------------------------------------------
echo.

python app.py

echo.
echo [INFO] Python service ended.
pause
