import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Fetch Hugging Face token safely
hf_token = os.environ.get("HF_TOKEN")

if not hf_token:
    st.error("""
    ❌ **Hugging Face API token missing!**
    
    Please set the HF_TOKEN environment variable locally or in Streamlit Cloud Secrets.
    """)
    st.stop()

HF_HEADERS = {"Authorization": f"Bearer {hf_token}"}

# Page config with custom theme
st.set_page_config(page_title="EcoScan", page_icon="🌿", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e0f2f1, #e8f5e9);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #1b5e20;
    text-align: center;
}
.header {
    text-align: center;
    margin-top: 20px;
}
.tabs .css-1v0mbdj {   /* Adjust Streamlit tab spacing */
    margin-left: 10px;
    margin-right: 10px;
}
.tab-container {
    background-color: white;
    border-radius: 15px;
    padding: 30px;
    margin: 20px auto;
    max-width: 700px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.stTextInput > label {
    font-weight: bold;
    color: #2e7d32;
}
.stButton button {
    background-color: #2e7d32;
    color: white;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}
.stButton button:hover {
    background-color: #1b5e20;
}
.footer {
    text-align: center;
    font-size: 0.9rem;
    color: #4e944f;
    margin-top: 40px;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header">
    <img src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png" width="80">
    <h1>EcoScan 🌱</h1>
    <h3>Plastic-Free Product Checker</h3>
</div>
""", unsafe_allow_html=True)

# Tabs for sections
tab1, tab2, tab3 = st.tabs(["📷 Scan", "📜 History", "🏆 Leaderboard"])

# -------------------- Tab 1: Scan
with tab1:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.header("Scan Your Product")

    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_image = st.file_uploader("Upload product image (JPG, PNG)", type=["jpg", "png"])
    with col2:
        product_name = st.text_input("Or search by product name", placeholder="e.g., Herbal Shampoo, BIC Pen")

    scan_button = st.button("🔍 Analyze Product")

    if scan_button:
        final_product = None
        if product_name:
            final_product = product_name
        elif uploaded_image:
            final_product = uploaded_image.name
            st.image(uploaded_image, caption="Scanned Product", use_column_width=True)
        else:
            st.warning("Please enter a product name or upload an image.")
            st.stop()

        st.info(f"🔎 Scanning: **{final_product}**")

        with st.spinner("Analyzing with Hugging Face AI..."):
            HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
            payload = {"inputs": final_product}
            response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)

        if response.status_code == 200:
            result = response.json()
            label = result[0]['label']
            score = result[0]['score']
            eco_score = round(score * 100, 1)

            st.success("✅ Analysis Complete!")
            analysis_html = f"""
            <h3>🔎 AI Analysis for '{final_product}'</h3>
            <p><b>Sentiment Label:</b> {label}</p>
            <p><b>Confidence Score:</b> {eco_score}%</p>
            """

            if label == "POSITIVE":
                analysis_html += "<p><b>Eco-Insight:</b> Product likely perceived as eco-friendly or sustainable.</p>"
            else:
                analysis_html += "<p><b>Eco-Insight:</b> Product may not be eco-friendly — consider alternatives.</p>"

            st.markdown(analysis_html, unsafe_allow_html=True)
        else:
            st.error(f"❌ API request failed: {response.status_code} - {response.text}")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Tab 2: History
with tab2:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.header("Your Scan History")
    st.markdown("Here’s a simulated table of your past scans:")
    history_data = pd.DataFrame({
        "Date": ["2025-07-02", "2025-07-03"],
        "Product": ["Plastic Bottle", "Plastic Pen"],
        "Score": [25, 30]
    })
    st.table(history_data)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Tab 3: Leaderboard
with tab3:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.header("Top Eco Heroes 🌍")
    leaderboard_data = pd.DataFrame({
        "User": ["Alice", "Bob", "Charlie"],
        "CO₂ Saved (kg)": [5.4, 3.2, 2.7]
    })
    fig = px.bar(leaderboard_data, x="User", y="CO₂ Saved (kg)", color="User",
                 labels={"CO₂ Saved (kg)":"CO₂ Saved (kg)"},
                 title="Leaderboard: CO₂ Savings by Users")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by Team EcoScan • Powered by Streamlit
    </div>
""", unsafe_allow_html=True)
