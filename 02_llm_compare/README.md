# Simple LLM Application

This project is a simple Streamlit-based web application that allows users to interact with multiple language models (LLMs) provided by Groq. Users can input a query and compare the responses from two different models side by side.

---

## Features
- **API Integration**: Input and save your Groq API key to access the LLM services.
- **Model Selection**: Choose from a list of available Groq LLM models for comparison.
- **Real-Time Responses**: Submit a query and view responses from two selected models in parallel.
- **Streaming Responses**: Responses are streamed chunk-by-chunk for a real-time user experience.

---

## Usage

## Prerequisites
Before running the project, ensure the following:

1. 🐍 **Python Installed:** This project requires Python 3.8 or newer. If not installed, download it from [python.org](https://www.python.org/downloads/).
2. 🔑 **Groq API Key:** Obtain an API key from Groq and keep it handy.
3. 🌐 **Internet Connection:** The application requires a stable internet connection to communicate with the Groq API.

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**
   ```bash
   https://github.com/ainabler/showcase.git
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Run the Application**
   Start the Streamlit app using the following command:
   ```bash
   streamlit run main.py
   ```

2. **Access the Application**
   Open your web browser and navigate to `http://localhost:8501` to access the application interface.

3. **Interact with the Features**
   - 📝 Input prompts or queries for the LLM.
   - 🤖 Leverage agentic capabilities for complex tasks.
   - 📊 View real-time results powered by Groq API.

## Features
- 🖥️ **Streamlit Interface:** User-friendly and interactive front end.
- ⚡ **Groq Integration:** High-performance LLM operations via Groq API.

## Troubleshooting
- ⚠️ **Missing Dependencies:** Ensure all dependencies are installed correctly by re-running `pip install -r requirements.txt`.
- ❌ **Invalid API Key:** Verify your Groq API key 
- 🌐 **Connection Issues:** Check your internet connection and API access.

## Acknowledgments
Special thanks to the Groq team for providing robust API support and the Streamlit community for their excellent resources. Thanks to https://github.com/durgeshsamariya for the great readme.md template

---

Enjoy using the project! For any issues, feel free to raise a GitHub issue or contact the maintainer.
