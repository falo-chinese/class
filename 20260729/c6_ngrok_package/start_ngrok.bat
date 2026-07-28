@echo off
title ngrok Port 8888 Tunnel
cls
echo =================================================================
echo  Starting ngrok http 127.0.0.1:8888 Tunnel...
echo =================================================================
echo.

if exist "%~dp0ngrok.exe" goto RUN_LOCAL
goto RUN_PATH

:RUN_LOCAL
"%~dp0ngrok.exe" http 127.0.0.1:8888
goto END

:RUN_PATH
ngrok http 127.0.0.1:8888
goto END

:END
echo.
echo [INFO] ngrok session ended.
pause
