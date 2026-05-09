import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

st.set_page_config(page_title="Notorious AI", layout="centered")

st.title("🏴 NOTORIOUS AI")
st.caption("Neural Predictor for Scalping Signals")

# Gunakan model sesuai cURL yang berhasil
MODEL_NAME = 'gemini-1.5-flash-latest' 
API_KEY = "AIzaSyBZtoAMlijbBkCBwMHB2e3PFuJtF3cmTpo"

uploaded_file = st.file_uploader("Upload Screenshot Chart", type=['png', 'jpg', 'jpeg'])

if st.button("GENERATE SIGNAL"):
    if not uploaded_file:
        st.error("Upload gambarnya dulu!")
    else:
        try:
            # Konfigurasi API
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_NAME)
            
            img = Image.open(uploaded_file)
            
            with st.spinner('Menganalisis market...'):
                # Instruksi khusus untuk scalping
                prompt = "Analisis chart ini untuk scalping. Berikan output JSON murni: { \"signal\": \"BUY/SELL\", \"entry\": \"...\", \"tp\": \"...\", \"sl\": \"...\", \"confidence\": \"...%\", \"reason\": \"...\" }"
                
                response = model.generate_content([prompt, img])
                
                # Membersihkan string JSON
                res_text = response.text.replace('```json', '').replace('
```', '').strip()
                data = json.loads(res_text)
                
                # UI Hasil Analisis
                st.divider()
                color = "#22c55e" if "BUY" in data['signal'].upper() else "#ef4444"
                st.markdown(f"<h1 style='text-align: center; color: {color};'>{data['signal']}</h1>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("ENTRY", data['entry'])
                c2.metric("TP", data['tp'])
                c3.metric("SL", data['sl'])
                
                st.subheader(f"Confidence: {data['confidence']}")
                st.write(f"**Analisis:** {data['reason']}")
                
        except Exception as e:
            st.error(f"Gagal: {e}")
                
