@echo off
setlocal EnableDelayedExpansion

:: Cek apakah berada di folder yang benar
if not exist "app.py" (
    echo Error: app.py tidak ditemukan!
    echo Pastikan Anda menjalankan script ini dari folder 03_audio_extract
    exit /b 1
)

:: Cek virtual environment
if not exist "venv" (
    echo Error: Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu untuk instalasi
    exit /b 1
)

:: Aktifkan virtual environment
echo Mengaktifkan virtual environment...
call venv\Scripts\activate

:: Cek FFmpeg
where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PERINGATAN: FFmpeg tidak ditemukan!
    echo Aplikasi mungkin tidak berjalan dengan benar
    echo Silakan install FFmpeg dari https://ffmpeg.org/download.html
    echo.
)

:: Jalankan aplikasi
echo Menjalankan aplikasi...
echo.
echo Aplikasi akan terbuka di browser Anda...
echo Untuk menghentikan aplikasi, tekan Ctrl+C
echo.
streamlit run app.py

:: Deaktivasi virtual environment saat selesai
deactivate

endlocal