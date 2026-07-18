import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load your custom trained model weights
model = YOLO("best.pt")

# Set premium geometric wide configurations
st.set_page_config(page_title="Vera Metric", layout="wide")

# Inject premium Inter font styling directly into the layout architecture
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0b0c !important;
        color: #f3f4f6 !important;
    }
    h1, h2, h3, h4, h5, h6, label, p {
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stBlock"] {
        background-color: #121214;
        border: 1px solid #222226;
        border-radius: 6px;
        padding: 1.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #121214 !important;
        color: #f3f4f6 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        padding: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1f1f24 !important;
        border-color: #3f3f46 !important;
    }
    input {
        background-color: #1a1a1e !important;
        border: 1px solid #222226 !important;
        color: #ffffff !important;
        font-family: monospace !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        letter-spacing: 3px !important;
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown("<h1 style='color:#ffffff; font-weight:700; letter-spacing:-0.04em;'>Vera Metric</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; margin-bottom:3.5rem;'>Optical character recognition for utility meters</p>", unsafe_allow_html=True)

# Main Structural Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h2 style='font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#4b5563;'>Source File</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload snapshot", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Source alignment geometry", use_container_width=True)
        analyse_btn = st.button("Run Analysis", type="primary")

with col2:
    st.markdown("<h2 style='font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#4b5563;'>Processed Output</h2>", unsafe_allow_html=True)
    
    if uploaded_file and 'analyse_btn' in locals() and analyse_btn:
        with st.spinner("Processing structural frames..."):
            # Execute model predictions
            results = model.predict(
                source=image,
                conf=0.25,
                iou=0.60,
                agnostic_nms=True
            )
            result = results[0]
            
            # Map structural components
            mapped_image = result.plot(line_width=2)
            st.image(mapped_image, caption="Output bounding alignment", use_container_width=True)
            
            # Sort sequential digits left-to-right
            boxes = result.boxes.data.tolist()
            digit_detections = []
            
            for box in boxes:
                class_id = int(box[5])
                class_name = model.names[class_id]
                
                if class_name not in ["meter", "window"]:
                    x_center = (box[0] + box[2]) / 2
                    display_char = "u" if "unknown" in class_name else class_name
                    digit_detections.append((x_center, display_char))
                    
            digit_detections.sort(key=lambda x: x[0])
            recognized_number = "".join([item[1] for item in digit_detections])
            
            if not recognized_number:
                recognized_number = "No digits recognized."
                
            st.text_input("Value Sequence Readout", value=recognized_number, disabled=True)
    else:
        st.markdown("<div style='color:#9ca3af; text-align:center; padding:2rem; border:1px solid #222226; border-radius:6px; background-color:#121214;'>Awaiting image upload and analysis loop.</div>", unsafe_allow_html=True)