import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

# Page Configuration
st.set_page_config(page_title="Notorious AI | Analyzer", layout="centered")

# Custom CSS for Modern Glassmorphism
st.markdown("""
    <style>
    .main { background: #0e1117; color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        background: linear-gradient(90deg, #1e40af, #4338ca); 
        color: white; 
        border: none; 
        padding: 12px; 
        font-weight: bold; 
        transition: 0.3s; 
    }
    .stButton>button:hover { 
        background: linear-gradient(90deg, #2563eb, #4f46e5); 
        transform: scale(1.02); 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏴 NOTORIOUS AI")
st.caption("Universal Chart Analyzer - Crypto, Forex, Gold & Stocks")

# API Configuration
API_KEY = "AIzaSyBZtoAMlijbBkCBwMHB2e3PFuJtF3cmTpo"
MODEL_NAME = 'gemini-1.5-flash-latest'

uploaded_file = st.file_uploader("Upload Chart Screenshot", type=['png', 'jpg', 'jpeg'])

if st.button("GENERATE SCALP SIGNAL"):
    if not uploaded_file:
        st.error("Please upload a chart image first!")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_NAME)
            
            img = Image.open(uploaded_file)
            
            with st.spinner('Analyzing market structure...'):
                prompt = """
                Analyze this chart deeply for a scalping strategy.
                Detect market structure (BOS/CHoCH), supply/demand zones, or any visible indicators.
                The asset can be anything (Crypto, Forex, Stocks, etc.).
                Provide the output in pure JSON format:
                {
                    "asset": "Asset Name",
                    "signal": "BUY or SELL or WAIT",
                    "entry": "Entry Price Range",
                    "tp": "Take Profit Target",
                    "sl": "Stop Loss Level",
                    "confidence": "Number %",
                    "reason": "Short technical analysis in English"
                }
                """
                
                response = model.generate_content([prompt, img])
                
                # Robust JSON extraction
                raw_text = response.text
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                
                if match:
                    json_data = match.group(0)
                    data = json.loads(json_data)
                    
                    st.divider()
                    
                    # Result Header Logic
                    sig = data['signal'].upper()
                    color = "#22c55e" if sig == "BUY" else "#ef4444"
                    if sig == "WAIT": color = "#eab308"
                    
                    st.markdown(f"<h1 style='text-align: center; color: {color};'>{sig} {data['asset']}</h1>", unsafe_allow_html=True)
                    
                    # Metric Rows
                    col1, col2, col3 = st.columns(3)
                    with col1: st.metric("ENTRY", data['entry'])
                    with col2: st.metric("TAKE PROFIT", data['tp'])
                    with col3: st.metric("STOP LOSS", data['sl'])
                    
                    # Additional Details
                    st.info(f"**Analysis:** {data['reason']}")
                    st.warning(f"**Confidence Level:** {data['confidence']}")
                    
                else:
                    st.error("AI returned an invalid format. Please try again.")
                    
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.markdown("<br><hr><center><small>Notorious AI © 2026 | Financial markets carry risk. Use for educational purposes only.</small></center>", unsafe_allow_html=True)
