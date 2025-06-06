@echo off
REM Windows batch file to stop the key generator service

echo Stopping key generator service...

REM Find and kill the Python process running key_generator_service.py
for /f "tokens=1" %%p in ('wmic process where "commandline like '%%key_generator_service.py%%'" get processid ^| findstr /r "[0-9]"') do (
    echo Found process with PID %%p
    taskkill /F /PID %%p
    echo Service stopped.
    goto :end
)

echo No running key generator service found.

:end
pause 