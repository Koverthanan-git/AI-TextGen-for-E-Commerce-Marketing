import streamlit as st
import requests
import pandas as pd
from pymongo import MongoClient

st.title("AI TextGen for E-Commerce & Marketing")

# Input form
with st.form("input_form"):
    product_name = st.text_input("Product Name", value="XYZ Smartwatch")
    category = st.text_input("Category", value="Electronics")
    features = st.text_area("Features", value="heart rate monitor, GPS, AMOLED display")
    audience = st.text_input("Target Audience", value="millennials")
    tone = st.selectbox("Tone", ["Professional", "Casual", "Persuasive"])
    output_type = st.selectbox("Output Type", ["Ad Copy", "Product Description"])
    submit_button = st.form_submit_button("Generate")

if submit_button:
    # Send request to Flask API
    payload = {
        "product_name": product_name,
        "category": category,
        "features": features,
        "audience": audience,
        "tone": tone,
        "output_type": output_type
    }
    try:
        response = requests.post("http://localhost:5000/generate", json=payload)
        if response.status_code == 200:
            st.success("Generated Text:")
            st.write(response.json()["generated_text"])
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {str(e)}")

# Display previous outputs from MongoDB
st.subheader("Previous Outputs")
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["textgen_db"]
    collection = db["outputs"]
    records = list(collection.find().sort("timestamp", -1).limit(10))  # Last 10 records
    if records:
        df = pd.DataFrame(records)
        df["timestamp"] = df["timestamp"].astype(str)  # Convert for display
        st.dataframe(df[["product_name", "category", "output_type", "generated_text", "timestamp"]])
    else:
        st.write("No previous outputs found.")
except Exception as e:
    st.error(f"Failed to fetch previous outputs: {str(e)}")