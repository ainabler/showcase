import streamlit as st
import yfinance as yf
from groq import Groq

# Page configuration
st.set_page_config(page_title="Stock Analysis", page_icon=":chart_with_upwards_trend:", layout="wide")

# Initialize session state
if "groq_api" not in st.session_state:
    st.session_state.groq_api = ""

def get_llm_response(prompt, model="llama-3.1-8b-instant"):
    """Get response from Groq LLM"""
    try:
        client = Groq(api_key=st.session_state.groq_api)
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Reduced for more focused responses
            max_tokens=1024,
            stream=True
        )
        
        return "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    except Exception as e:
        st.error(f"LLM Error: {e}")
        return None

def get_stock_data(ticker_symbol):
    """Fetch and format stock data"""
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        return {
            "company_info": {
                "name": info.get('longName', 'N/A'),
                "industry": info.get('industryDisp', 'N/A'),
                "sector": info.get('sectorDisp', 'N/A'),
                "summary": info.get('longBusinessSummary', 'N/A')
            },
            "price_data": {
                "current_price": info.get('currentPrice', 'N/A'),
                "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
                "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
                "50_day_avg": info.get('fiftyDayAverage', 'N/A'),
                "200_day_avg": info.get('twoHundredDayAverage', 'N/A')
            },
            "financials": {
                "market_cap": info.get('marketCap', 'N/A'),
                "pe_ratio": info.get('trailingPE', 'N/A'),
                "price_to_book": info.get('priceToBook', 'N/A'),
                "revenue_growth": info.get('revenueGrowth', 'N/A'),
                "earnings_growth": info.get('earningsGrowth', 'N/A')
            },
            "analysis": {
                "recommendation": info.get('recommendationKey', 'N/A'),
                "target_mean_price": info.get('targetMeanPrice', 'N/A'),
                "beta": info.get('beta', 'N/A')
            }
        }
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

def generate_analysis_prompt(data):
    """Generate prompt for LLM analysis"""
    return f"""As an experienced stock analyst, analyze the following data and provide insights:

            Company: {data['company_info']['name']}
            Industry: {data['company_info']['industry']}
            Current Price: ${data['price_data']['current_price']}

            Please provide analysis in the following format:
            # {data['company_info']['name']}

            ## Company Overview
            [Brief company description and industry position]

            ## Market Performance
            - Current Price: {data['price_data']['current_price']} pastikan mata uang sesuai dengan negara dimana perusahaan ini beroperasi
            - 52-Week Range: {data['price_data']['52_week_low']} - {data['price_data']['52_week_high']}pastikan mata uang sesuai dengan negara dimana perusahaan ini beroperasi

            ## Fundamental Analysis
            [Analysis based on financial metrics]{data}

            ## Technical Analysis
            [Analysis based on price movements and averages]{data}

            ## Recommendation
            [Your professional opinion]

            *Disclaimer: This analysis is for informational purposes only and should not be considered as investment advice.* give result only in bahasa indonesia"""

# Sidebar
with st.sidebar:
    st.subheader("Stock Analysis Settings")
    groq_api = st.text_input("Groq API Key:", type="password")
    if st.button("Save API Key"):
        st.session_state.groq_api = groq_api
        st.success("API key saved successfully!")

    model = st.selectbox(
        "Select Language Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    )

# Main content
st.title("Stock Analysis Dashboard")

ticker = st.text_input("Enter Stock Ticker Symbol:", help="Example: AAPL for Apple Inc.")

if st.button("Analyze"):
    if not st.session_state.groq_api:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not ticker:
        st.warning("Please enter a stock ticker symbol.")
    else:
        
        with st.spinner("Analyzing stock data..."):
            stock_data = get_stock_data(ticker)
            # Display additional metrics in expandable section
            with st.expander("View Detailed Metrics"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Market Cap", f"${stock_data['financials']['market_cap']:,.2f}")
                            st.metric("P/E Ratio", stock_data['financials']['pe_ratio'])
                        with col2:
                            st.metric("Beta", stock_data['analysis']['beta'])
                            st.metric("Price to Book", stock_data['financials']['price_to_book'])
            if stock_data:
                analysis_prompt = generate_analysis_prompt(stock_data)
                analysis = get_llm_response(analysis_prompt, model)
                if analysis:
                    st.markdown(analysis)
          
                    
                    