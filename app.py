import streamlit as st
from PIL import Image
import base64
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE-GEMINI-API-KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Prompt Template
PROMPT_TEMPLATE = """
You are an expert manufacturing engineer and manufacturing quality consultant. A user will upload an image of a Manufacturing defected components. Based on the visual characteristics of the image, analyze the structure and provide an expert assessment of its condition.

Your response must follow this specific format:

Defect: Yes / No along with Probability of Defect in percentage.

Explain the Type of Defect: (E.g., Material Defects,Structural Defects,Operational Defects, Dimensional Defects,Functional Defects,Surface/Visual Defects,Process-Related Defects, Assembly Defects,Handling and Packaging Defect etc.)
Observed Defects: Describe what is seen in the image that supports your diagnosis.
Possible Causes: Based on the defect type, list the likely causes.
Recommendations: What should be done immediately to address or further investigate the issue.
Repair Strategy: Detailed step-by-step repair methodology suitable for this defect.

Only give answers based on what is visible in the image. Do not speculate beyond visual evidence. Be concise but thorough. Use Manufacture engineering terminology and best practices.
"""

def analyze_image(image):
    # Convert PIL Image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Generate content with the image and prompt
    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [
                {"text": PROMPT_TEMPLATE},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
            ]}
        ]
    )

    return response.text

# Streamlit App

st.markdown("<h1 style='text-align: center;'>🔧 Manufacturing <span style='color: red;'>Defect</span> <span style='color: green;'>Detection</span> System 🛠️</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>🛠️⚙️🏭 Prototype for Automated Defect Analysis</h3>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Upload Construction Image")
uploaded_file = st.sidebar.file_uploader(label="Upload the Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Uploaded Image")

    with st.spinner("Analyzing image..."):
        result = analyze_image(img)

    st.markdown("### Analysis Result")
    st.markdown(result)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee;">
    <p>Manufacturing Defect Detection System - Prototype Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)
