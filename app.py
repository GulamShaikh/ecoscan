import streamlit as st
import requests

# Page config for favicon and centered layout
st.set_page_config(page_title="EcoScan", page_icon="🌿", layout="centered")

# Inject custom CSS for gradient background, header, and footer
st.markdown("""
    <style>
body {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9, #a5d6a7);
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
}
.container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
}
.header img {
    width: 70px;
    animation: pulse 2s infinite alternate;
}
.stTextInput input, .stFileUploader input {
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
}
.stButton button {
    background-color: #2e7d32;
    color: white;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 1rem;
}
.stButton button:hover {
    background-color: #1b5e20;
    transition: 0.3s ease;
}
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #4e944f;
    margin-top: 40px;
    padding-bottom: 20px;
}
@keyframes pulse {
    from { transform: scale(1); }
    to { transform: scale(1.1); }
}
</style>

""", unsafe_allow_html=True)

# Header with logo & title
st.markdown("""
    <div class="header">
        <img src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png" alt="EcoScan Logo">
        <h1>EcoScan</h1>
        <p>🌱 Plastic-Free Product Checker – Scan or type to check eco-friendliness!</p>
    </div>
""", unsafe_allow_html=True)

# Input fields
product_name = st.text_input("Enter product name", placeholder="e.g., Plastic Shampoo Bottle")

uploaded_image = st.file_uploader("Or upload product image (for simulation only)", type=["jpg", "png"])

if st.button("🔍 Scan Now"):
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
    with st.spinner("Analyzing eco-friendliness with AI..."):
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyDDKZL72D96iuI9codSXHWS11eKI9a06ek"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Is the product '{final_product}' eco-friendly? Explain why, rate it out of 100, and suggest greener alternatives."
                        }
                    ]
                }
            ]
        }
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.success("✅ Scan Complete!")
            st.markdown(result.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            st.error("❌ API request failed. Check API key or quota.")

# Footer with credits or contact info
st.markdown("""
    <div class="footer">
        Created by EcoScan Team • <a href="https://streamlit.io" target="_blank" style="color:#1b5e20; text-decoration:underline;">Powered by Streamlit</a>
    </div>
""", unsafe_allow_html=True)
