# Aplikasi Ekstraksi Informasi Audio

Aplikasi Streamlit untuk mengekstrak informasi dari file audio menggunakan model Google Gemini 2.0 Flash. Pengguna dapat mengunggah file audio dan memberikan prompt khusus untuk menganalisis konten sesuai kebutuhan mereka.

## Fitur

- Unggah dan proses file audio MP4 (durasi maksimal 20 menit)
- Ekstraksi informasi berbasis prompt kustom
- Menggunakan model Google Gemini 2.0 Flash (kapasitas ~1 juta token)
- Pemrosesan audio dan ekstraksi informasi secara real-time
- Antarmuka Streamlit yang mudah digunakan

## Prasyarat

1. Python 3.8 atau lebih tinggi terinstal di sistem Anda
2. API key Google dari https://aistudio.google.com/app/prompts/new_chat
3. FFmpeg terinstal di sistem Anda

## Instalasi

1. Clone repositori ini:
```bash
git clone https://github.com/ainabler/showcase.git
cd showcase/03_audio_extract
```

2. Buat dan aktifkan virtual environment (direkomendasikan):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install paket yang diperlukan:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:

**Windows:**
- Unduh dari https://ffmpeg.org/download.html
- Tambahkan ke system PATH

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## Penggunaan

1. Jalankan aplikasi Streamlit:
```bash
run_app.bat
```

2. Buka browser web Anda dan akses URL lokal yang diberikan (biasanya http://localhost:8501)

3. Masukkan API key Google Anda di field password
   - Dapatkan API key dari: https://aistudio.google.com/app/prompts/new_chat
   - Jaga keamanan API key Anda dan jangan bagikan

4. Unggah file audio MP4 (durasi maksimal 20 menit)

5. Masukkan prompt yang menjelaskan informasi apa yang ingin Anda ekstrak dari audio

6. Klik "Process Audio" dan tunggu hasilnya

## Contoh Prompt

- "Buatkan kesimpulan dari rekaman tersebut"
- "Ekstrak poin-poin penting dari audio ini"
- "Identifikasi pembicara dan topik utama dalam rekaman"
- "Buat transkrip dari audio tersebut"

## Batasan

- Durasi audio maksimal: 20 menit
- Format file yang didukung: MP4
- Membutuhkan koneksi internet yang stabil
- API key harus memiliki akses ke model Gemini 2.0 Flash

## Penyelesaian Masalah

1. **Masalah API Key:**
   - Pastikan Anda memiliki API key yang valid dari Google AI Studio
   - Periksa apakah API key Anda memiliki izin yang tepat
   - Verifikasi koneksi internet Anda

2. **Masalah Upload File:**
   - Periksa apakah file dalam format MP4
   - Pastikan durasi file di bawah 20 menit
   - Verifikasi file tidak rusak

3. **Error FFmpeg:**
   - Verifikasi FFmpeg terinstal dengan benar
   - Periksa apakah FFmpeg sudah ditambahkan ke system PATH
   - Coba instal ulang FFmpeg

