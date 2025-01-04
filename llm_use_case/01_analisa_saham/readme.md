# Stock Analysis Dashboard

A Streamlit-based web application that provides stock analysis using real-time market data and AI-powered insights powered by Groq LLM.

## Features

- Real-time stock data fetching using yfinance
- AI-powered stock analysis using Groq LLM
- Interactive web interface built with Streamlit
- Fundamental and technical analysis generation
- Detailed metrics visualization
- Customizable language model selection

## Prerequisites

- Python 3.8 or higher
- Groq API key (get it from https://console.groq.com/playground)

## Installation

1. Clone this repository:
```bash
git clone [<repository-url>](https://github.com/ainabler/showcase.git)
cd llm_use_Case/01_analisa_saham
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the URL shown in your terminal (typically http://localhost:8501)

3. In the sidebar:
   - Enter your Groq API key
   - Select your preferred language model

4. In the main interface:
   - Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)
   - Click "Analyze" to get the analysis

## Configuration

The application uses the following language models:
- llama-3.1-8b-instant (faster, lighter model)
- llama-3.3-70b-versatile (more comprehensive analysis)

## Data Sources

- Stock data is fetched from Yahoo Finance using the yfinance library
- Analysis is generated using Groq's LLM models

## Limitations

- Analysis is dependent on the availability and accuracy of Yahoo Finance data
- API rate limits may apply based on your Groq account type
- Stock data may be delayed based on market conditions

## Disclaimer

This tool is for informational purposes only. The analysis provided should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
