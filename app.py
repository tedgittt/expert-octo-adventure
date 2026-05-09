import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Tampilan Tema Gelap
st.set_page_config(page_title="Notorious AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; background: #2563eb; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏴 NOTORIOUS AI")
st.caption("Neural Predictor for Scalping Signals")

# Masukkan API Key kamu di sidebar
api_key = st.sidebar.text_input("Gemini API Key", type="password", value="AIzaSyBZtoAMlijbBkCBwMHB2e3PFuJtF3cmTpo")

uploaded_file = st.file_uploader("Upload Screenshot Chart (XAUUSD/Forex)", type=['png', 'jpg', 'jpeg'])

if st.button("GENERATE SIGNAL"):
    if not uploaded_file:
        st.error("Upload gambarnya dulu, Bos!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            img = Image.open(uploaded_file)
            
            with st.spinner('Menganalisis pergerakan market...'):
                prompt = "Analisis chart trading ini untuk strategi scalping. Berikan output JSON: { 'signal': 'BUY/SELL', 'entry': '...', 'tp': '...', 'sl': '...', 'confidence': '...%', 'reason': '...' }"
                response = model.generate_content([prompt, img])
                
                # Membersihkan & Membaca Data
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(res_text)
                
                # Tampilkan Hasil
                st.divider()
                color = "#22c55e" if "BUY" in data['signal'].upper() else "#ef4444"
                st.markdown(f"<h1 style='text-align: center; color: {color};'>{data['signal']}</h1>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("ENTRY", data['entry'])
                col2.metric("TAKE PROFIT", data['tp'])
                col3.metric("STOP LOSS", data['sl'])
                
                st.warning(f"**Confidence:** {data['confidence']}")
                st.info(f"**Analisis:** {data['reason']}")
                
        except Exception as e:
            st.error(f"Koneksi Gagal: {e}")
  
