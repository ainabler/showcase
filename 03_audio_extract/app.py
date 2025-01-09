import streamlit as st
import google.generativeai as genai
from typing import List, Optional
import logging
import os
from pydub import AudioSegment
import tempfile
import shutil

def validate_api_key(api_key: str) -> bool:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
        return True
    except Exception as e:
        logging.error(f"API key validation failed: {str(e)}")
        return False

def convert_aac_to_mp3(input_path: str) -> str:
    try:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "converted_audio.mp3")
        audio = AudioSegment.from_file(input_path, format="aac")
        audio.export(output_path, format="mp3", bitrate="192k")
        logging.info(f"Successfully converted {input_path} to MP3")
        return output_path
    except Exception as e:
        logging.error(f"Error converting AAC to MP3: {str(e)}")
        raise

def upload_to_gemini(file_path: str, api_key: str, mime_type: str = "audio/mp3"):
    try:
        # Ensure API key is configured before upload
        genai.configure(api_key=api_key)
        file = genai.upload_file(file_path, mime_type=mime_type)
        logging.info(f"Successfully uploaded file to Gemini: {file_path}")
        return file
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return None

def initialize_gemini(api_key: str) -> genai.GenerativeModel:
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

def process_audio_with_gemini(
    file_path: str,
    api_key: str,
    prompt: str,
) -> Optional[str]:
    try:
        if not api_key:
            raise ValueError("API key is required")

        # Convert if needed
        temp_file = None
        processing_path = file_path
        if file_path.lower().endswith('.aac'):
            processing_path = convert_aac_to_mp3(file_path)
            temp_file = processing_path

        try:
            # Upload and process
            uploaded_file = upload_to_gemini(processing_path, api_key)
            if not uploaded_file:
                raise Exception("Failed to upload file to Gemini")

            model = initialize_gemini(api_key)
            chat_session = model.start_chat(
                history=[{"role": "user", "parts": [uploaded_file]}]
            )
            response = chat_session.send_message(prompt)
            return response.text

        finally:
            # Cleanup temp file if it was created
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
                logging.info(f"Cleaned up temporary file: {temp_file}")

    except Exception as e:
        logging.error(f"Error processing audio: {str(e)}")
        return None

def generate_notulen(file_path: str, api_key: str) -> Optional[str]:
    prompt = """Buatkan notulen rapat yang lengkap dan terstruktur dari rekaman audio ini. 
    Harap sertakan:
    1. Tanggal dan waktu rapat (jika disebutkan)
    2. Peserta rapat (jika disebutkan)
    3. Agenda/topik yang dibahas
    4. Poin-poin penting dari setiap pembahasan
    5. Keputusan yang diambil
    6. Tindak lanjut atau tugas yang diberikan
    
    Format notulen dalam bentuk yang formal dan profesional."""
    
    return process_audio_with_gemini(file_path, api_key, prompt)

def generate_transcript(file_path: str, api_key: str) -> Optional[str]:
    prompt = """Buatkan transkrip lengkap dari audio ini dengan format berikut:
    1. Identifikasi pembicara jika ada multiple speaker (Contoh: Speaker 1:, Speaker 2:)
    2. Tambahkan timestamp setiap 1-2 menit
    3. Sertakan semua detail percakapan termasuk jeda, tawa, atau interupsi dalam tanda kurung
    4. Perbaiki tata bahasa dan pengucapan tanpa mengubah konteks
    
    Harap pertahankan akurasi dan konteks asli percakapan."""
    
    return process_audio_with_gemini(file_path, api_key, prompt)

def generate_action_plan(file_path: str, api_key: str) -> Optional[str]:
    prompt = """Analisis rekaman audio ini dan buatkan action plan yang terstruktur dengan:
    1. Daftar semua tugas dan tindak lanjut yang disebutkan
    2. Prioritas untuk setiap tugas (High/Medium/Low)
    3. Target waktu penyelesaian (jika disebutkan)
    4. Penanggung jawab untuk setiap tugas (jika disebutkan)
    5. Dependencies atau ketergantungan antar tugas
    6. Catatan atau rekomendasi khusus
    
    Format dalam bentuk yang mudah difollow up dan actionable."""
    
    return process_audio_with_gemini(file_path, api_key, prompt)

def generate_summary(file_path: str, api_key: str) -> Optional[str]:
    prompt = """Buatkan ringkasan komprehensif dari audio ini dengan format berikut:

    KONTEKS
    - Jenis konten (podcast/rapat/video/dll)
    - Durasi (jika terdeteksi)
    - Jumlah pembicara
    - Bahasa yang digunakan
    
    RINGKASAN UTAMA
    - Berikan ringkasan singkat namun lengkap tentang inti pembahasan
    - Highlight 3-5 poin penting yang dibahas
    - Kutip pernyataan-pernyataan kunci (jika ada)
    
    DETAIL PENTING
    - Nama atau istilah penting yang disebutkan
    - Angka atau statistik yang disebutkan
    - Referensi atau sumber yang dikutip
    - Informasi teknis yang relevan
    
    KESIMPULAN & INSIGHT
    - Kesimpulan utama dari pembahasan
    - Insight atau pembelajaran penting
    - Tindak lanjut atau rekomendasi (jika ada)
    
    Format output dalam bentuk yang mudah dibaca dengan pemisahan section yang jelas.
    Fokus pada informasi yang benar-benar penting dan relevan.
    Hindari informasi yang terlalu detail atau tidak signifikan."""
    
    return process_audio_with_gemini(file_path, api_key, prompt)

def main():
    st.set_page_config("Audio Processing", layout="wide", page_icon=":loud_sound:")
    
    # Initialize session state
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "current_result" not in st.session_state:
        st.session_state.current_result = None
    
    # Sidebar
    with st.sidebar:
        st.title("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter your Google API key:",
            type="password",
            help="Get API key from https://aistudio.google.com/app/apikey"
        )
        
        if st.button("Save API Key"):
            st.session_state.api_key = api_key.strip()
            if st.session_state.api_key != "":
                st.success("Successfully saved Gemini API key")
            else:
                st.warning("API Key not saved")
        
        # File path input
        file_path = st.text_input(
            "Audio File Path:",
            help="Enter the full path to your audio file (supports .mp3, .aac, .ogg, .wav)"
        )
        
        st.markdown("---")
        
        # Processing buttons
        def check_inputs() -> bool:
            if not st.session_state.api_key:
                st.error("Please save your API key first")
                return False
            if not file_path:
                st.error("Please provide the audio file path")
                return False
            if not os.path.exists(file_path):
                st.error("File not found at specified path")
                return False
            return True

        if st.button("Generate Summary", use_container_width=True):
            if check_inputs():
                with st.spinner("Generating summary..."):
                    result = generate_summary(file_path, st.session_state.api_key)
                    if result:
                        st.session_state.current_result = ("Summary", result)
                    else:
                        st.error("Failed to generate summary")

        if st.button("Generate Notulen", use_container_width=True):
            if check_inputs():
                with st.spinner("Generating notulen..."):
                    result = generate_notulen(file_path, st.session_state.api_key)
                    if result:
                        st.session_state.current_result = ("Notulen", result)
                    else:
                        st.error("Failed to generate notulen")
        
        if st.button("Generate Transcript", use_container_width=True):
            if check_inputs():
                with st.spinner("Generating transcript..."):
                    result = generate_transcript(file_path, st.session_state.api_key)
                    if result:
                        st.session_state.current_result = ("Transcript", result)
                    else:
                        st.error("Failed to generate transcript")
        
        if st.button("Generate Action Plan", use_container_width=True):
            if check_inputs():
                with st.spinner("Generating action plan..."):
                    result = generate_action_plan(file_path, st.session_state.api_key)
                    if result:
                        st.session_state.current_result = ("Action Plan", result)
                    else:
                        st.error("Failed to generate action plan")
    
    # Main content
    st.title("Audio Processing with Gemini AI")
    
    if st.session_state.current_result:
        title, content = st.session_state.current_result
        st.header(title)
        st.markdown(content)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()