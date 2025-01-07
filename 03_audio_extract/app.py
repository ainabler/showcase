import streamlit as st
import google.generativeai as genai
from typing import List, Optional
import logging
import os
from pydub import AudioSegment
import tempfile
import shutil
import subprocess

def validate_api_key(api_key: str) -> bool:
    """
    Validate the Google API key by attempting a simple configuration.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if API key is valid, False otherwise
    """
    try:
        genai.configure(api_key=st.session_state.api_key)
        # Try to access a simple model configuration to test the key
        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
        return True
    except Exception as e:
        logging.error(f"API key validation failed: {str(e)}")
        return False

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def convert_aac_to_mp3(input_path: str) -> str:
    """
    Convert AAC file to MP3 format.
    
    Args:
        input_path (str): Path to the input AAC file
    
    Returns:
        str: Path to the converted MP3 file
    """
    try:
        # Create temporary directory for conversion
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "converted_audio.mp3")
        
        # Load the AAC file
        audio = AudioSegment.from_file(input_path, format="aac")
        
        # Export as MP3
        audio.export(output_path, format="mp3", bitrate="192k")
        
        logging.info(f"Successfully converted {input_path} to MP3")
        return output_path
        
    except Exception as e:
        logging.error(f"Error converting AAC to MP3: {str(e)}")
        raise

def upload_to_gemini(file_path: str, mime_type: str = "audio/mp3"):
    """
    Uploads a file to Gemini AI.
    
    Args:
        file_path (str): Path to the file to upload
        mime_type (str): MIME type of the file (default: "audio/mp3")
    
    Returns:
        FileData: Uploaded file object or None if upload fails
    """
    try:
        file = genai.upload_file(file_path, mime_type=mime_type)
        logging.info(f"Successfully uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return None

def initialize_gemini(api_key: str) -> genai.GenerativeModel:
    """
    Initialize the Gemini AI model with specified configuration.
    
    Args:
        api_key (str): Google API key for authentication
    
    Returns:
        GenerativeModel: Configured Gemini model instance
    """
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

def process_audio_with_gemini(
    files: List[str],
    api_key: str,
    prompt: str,
    source: str
) -> Optional[str]:
    """
    Process audio files using Gemini AI.
    
    Args:
        files (List[str]): List of file paths to process
        api_key (str): Google API key
        prompt (str): Input prompt for the model
        source (str): Source identifier
    
    Returns:
        str: Generated response text or None if processing fails
    """
    try:
        # Upload files
        uploaded_files = []
        for file_path in files:
            uploaded_file = upload_to_gemini(file_path)
            if uploaded_file:
                uploaded_files.append(uploaded_file)
            else:
                raise Exception(f"Failed to upload file: {file_path}")

        # Initialize model
        model = initialize_gemini(api_key)

        # Start chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": uploaded_files
                }
            ]
        )

        # Send prompt and get response
        response = chat_session.send_message(prompt)
        return response.text

    except Exception as e:
        logging.error(f"Error processing audio: {str(e)}")
        return None

def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return os.path.splitext(filename)[1].lower()

def main():
    """Main Streamlit application"""

    st.set_page_config("Audio processing",layout="wide",page_icon=":loud_sound:")
    st.title("Audio Processing with Gemini AI")

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    
    # API key handling
    api_key = st.text_input("Enter your Google API key:", type="password", help="Dapatkan api key dari https://aistudio.google.com/app/apikey")
    if st.button("simpan"):
        st.session_state.api_key=api_key
        if st.session_state.api_key is not "":
            st.success("Sukses simpan Gemini api key")
        else:
            st.warning("API Key belum tersimpan")
    
    # File upload
    uploaded_file = st.file_uploader("Upload audio file", type=["aac", "mp3", "ogg", "wav"])
    
    # Prompt input
    prompt = st.text_area("Enter your prompt:")
    
    if st.button("Process Audio"):
        if not api_key:
            st.error("Please enter your Google API key")
            return
            
        # Validate API key before proceeding
        with st.spinner("Validating API key..."):
            if not validate_api_key(api_key):
                st.error("""
                Invalid or unauthorized API key. Please ensure:
                1. You have entered the correct API key
                2. The API key has access to Gemini API
                3. The API key is active and not restricted
                
                You can get an API key from: https://makersuite.google.com/app/apikey
                """)
                return
            
        if not uploaded_file:
            st.error("Please upload an audio file")
            return
            
        if not prompt:
            st.error("Please enter a prompt")
            return
            
        try:
            with st.spinner("Processing audio..."):
                # Explicitly configure API key before processing
                genai.configure(api_key=st.session_state.api_key)
                
                # Create temporary directory
                temp_dir = tempfile.mkdtemp()
                logging.info(f"Created temporary directory: {temp_dir}")
                
                # Save uploaded file
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                temp_input_path = os.path.join(temp_dir, f"input_audio{file_extension}")
                
                with open(temp_input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Convert if needed and process
                if file_extension == '.aac':
                    st.info("Converting AAC to MP3...")
                    processing_path = convert_aac_to_mp3(temp_input_path)
                else:
                    processing_path = temp_input_path
                
                # Process with Gemini
                result = process_audio_with_gemini(
                    files=[processing_path],
                    api_key=api_key,
                    prompt=prompt,
                    source="streamlit_app"
                )
                
                if result:
                    st.success("Processing complete!")
                    st.markdown(result)
                    #st.text_area("Result:", value=result, height=300)
                else:
                    st.error("Failed to process audio")
                
                # Cleanup
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    logging.warning(f"Error cleaning up temporary files: {str(e)}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    main()