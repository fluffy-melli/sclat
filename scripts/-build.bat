@echo off
cd ../
where python3 >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    set NODE=python3
) ELSE (
    set NODE=python
)
echo "init venv..."
%NODE% -m venv sclat-venv
call sclat-venv\Scripts\activate
echo "install modules..."
pip install -r requirements.txt
echo "pyinstaller start..."
pyinstaller ./sclat.spec
pyinstaller ./update.spec
deactivate