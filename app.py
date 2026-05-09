import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Notorious AI Chartalyzer",
    page_icon="📈",
    layout="centered"
)

# --- CUSTOM NEON DARK THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00ff88 0%, #00bd65 100%);
        color: black !important;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00ff88; }
    .signal-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #00ff88;
        background-color: #0f1116;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.5);
    }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #333; }
    h1, h2, h3 { color: #00ff88 !important; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🛡️ ACCESS CONTROL")
    st.markdown("Enter your **Gemini API Key** to power the analysis.")
    api_key_input = st.text_input("API Key:", type="password", placeholder="AIzaSy...")
    st.info("No key? Get one for free at [Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.markdown("### 🛠️ CONFIGURATION")
    st.caption("Model: Gemini 1.5 Flash (Ultra-Fast)")

# --- MAIN INTERFACE ---
st.title("🤖 NOTORIOUS AI")
st.markdown("### *Scalp Trading Chartalyzer*")
st.write("---")

# Instructions
with st.expander("📖 HOW TO USE (READ FIRST)"):
    st.markdown("""
    1. **Setup:** Enter your Gemini API Key in the sidebar.
    2. **Screenshot:** Capture your chart (TradingView/MT4/MT5). 
    3. **Indicators:** For best results, include RSI, Bollinger Bands, or Volume.
    4. **Upload:** Drag & Drop the image here.
    5. **Analyze:** Click the button and wait for the AI logic.
    """)

# Layout
col1, col2 = st.columns(2)

with col1:
    trade_mode = st.selectbox("Trading Instrument:", ["Binary Options (Fixed Time)", "CFD (Forex/Crypto)"])
    uploaded_file = st.file_uploader("Upload Chart Screenshot", type=["jpg", "png", "jpeg"])

with col2:
    if uploaded_file:
        st.image(uploaded_file, caption="Target Chart", use_container_width=True)

# --- LOGIC ENGINE ---
if st.button("EXECUTE CHART ANALYSIS"):
    if not api_key_input:
        st.error("❌ Error: Please enter an API Key in the sidebar!")
    elif not uploaded_file:
        st.warning("⚠️ Warning: Please upload a chart image first.")
    else:
        try:
            genai.configure(api_key=api_key_input)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prepare image
            img = Image.open(uploaded_file)
            
            # Prompt Construction
            prompt = f"""
            You are 'Notorious AI Chartalyzer', a high-stakes professional trader.
            Analyze this {trade_mode} chart. 
            
            Required Format:
            ---
            ## 🎯 SIGNAL: [BUY/SELL/NEUTRAL]
            - **Confidence Score:** [0-100]%
            - **Target/Expiry:** [Price or Time]
            - **Risk Level:** [Low/Medium/High]
            ---
            ### 🔍 TECHNICAL LOGIC:
            - Candlestick Analysis: [Brief observation]
            - Indicator Reading: [RSI/Volume/Trends]
            - Market Structure: [S/R levels detected]
            
            *Always provide a clear disclaimer that trading is risky.*
            """

            with st.spinner("🧠 Notorious AI is scanning market structure..."):
                response = model.generate_content([prompt, img])
                
            st.markdown(f'<div class="signal-card">{response.text}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# --- FOOTER ---
st.write("---")
st.caption("Powered by Gemini 1.5 Flash Vision Engine | Created for the Notorious Trading Community")
