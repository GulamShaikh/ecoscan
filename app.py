.import streamlit as st
import requests

st.set_page_config(page_title="EcoScan", page_icon="🌿", layout="centered")
st.title("🌿 EcoScan – Plastic-Free Product Checker")
st.write("Scan or enter a product name below to check eco-friendliness and get greener alternatives.")

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

    st.info(f"Scanning: **{final_product}**")
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
