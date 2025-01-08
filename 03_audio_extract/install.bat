@echo off
setlocal EnableDelayedExpansion

echo Memeriksa instalasi Python...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python tidak ditemukan. Mengunduh dan menginstal Python...
    
    :: Unduh Python installer
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
    
    :: Install Python dengan menambahkan ke PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Hapus installer
    del python_installer.exe
    
    :: Refresh PATH
    call refreshenv.cmd
    
    echo Python telah terinstal.
) else (
    echo Python sudah terinstal.
)

:: Cek git dan clone repositori
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Git tidak ditemukan. Silakan install Git terlebih dahulu di link berikut
    echo Windows: https://git-scm.com/download/win
    echo macOS: https://git-scm.com/download/mac
    echo Linux: https://git-scm.com/download/linux
    exit /b 1
)

:: Cek apakah folder sudah ada
if exist "showcase" (
    echo Updating repository...
    cd showcase
    git pull
) else (
    echo Cloning repository...
    git clone https://github.com/ainabler/showcase.git
    cd showcase
)

:: Masuk ke folder proyek
cd 03_audio_extract

:: Setup virtual environment dan install requirements
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Cek FFMPEG
where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PERINGATAN: FFmpeg tidak ditemukan. 
    echo Silakan download dan install FFmpeg dari https://ffmpeg.org/download.html
    echo dan tambahkan ke system PATH
)

:: Jalankan aplikasi
echo Starting application...
streamlit run app.py

endlocal