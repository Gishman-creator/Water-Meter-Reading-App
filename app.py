import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load your custom trained model weights
model = YOLO("best.pt")

# Set geometric wide layout configurations
st.set_page_config(page_title="Vera Metric", layout="wide")

# Inject premium Inter font and custom styled variables directly
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
    
    /* Top Right Image Overlay Style for Close Window Icon */
    .image-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    .close-overlay-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: rgba(18, 18, 20, 0.8);
        color: #f3f4f6;
        border: 1px solid #222226;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        text-align: center;
        line-height: 30px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.2s;
        z-index: 99;
    }
    .close-overlay-btn:hover {
        background-color: #1f1f24;
        border-color: #3f3f46;
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

# Header Section with Inline Alignment Setup
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("<h1 style='color:#ffffff; font-weight:700; letter-spacing:-0.04em; margin-bottom:0px;'>Vera Metric</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af; margin-bottom:3.5rem;'>Optical character recognition for utility meters</p>", unsafe_allow_html=True)

# Define Main Structural Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h2 style='font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#4b5563;'>Source File</h2>", unsafe_allow_html=True)
    
    # Track the upload/clear state using session storage keys
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "run_analysis" not in st.session_state:
        st.session_state.run_analysis = False

    # Condition 1: Upload input field is shown when no file exists
    if st.session_state.uploaded_image is None:
        uploaded_file = st.file_uploader("Upload snapshot", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state.uploaded_image = Image.open(uploaded_file)
            st.rerun()

    # Condition 2: File is uploaded. Hide input field, place layout elements strictly at top
    if st.session_state.uploaded_image is not None:
        # Place Run Analysis button inline up in the right side of the header column
        with header_col2:
            if st.button("Run Analysis", type="primary"):
                st.session_state.run_analysis = True
                st.rerun()
        
        # Absolute positioned CSS Close icon trigger matching top-right structural framework requirement
        # A tiny callback element handles state cleanup on user interaction
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        if st.button("❌ Close Image", key="overlay_close_trigger"):
            st.session_state.uploaded_image = None
            st.session_state.run_analysis = False
            st.rerun()
            
        st.image(st.session_state.uploaded_image, caption="Source alignment geometry", use_container_width=True)

with col2:
    st.markdown("<h2 style='font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#4b5563;'>Processed Output</h2>", unsafe_allow_html=True)
    
    # Process when state image is loaded and trigger analysis click is parsed
    if st.session_state.uploaded_image is not None and st.session_state.run_analysis:
        with st.spinner("Processing structural frames..."):
            results = model.predict(
                source=st.session_state.uploaded_image,
                conf=0.25,
                iou=0.60,
                agnostic_nms=True
            )
            result = results[0]
            
            # Sort sequential digit outputs left-to-right
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
            
            # TOP LAYER: Text number sequence field
            st.text_input("Value Sequence Readout", value=recognized_number, disabled=True)
            
            # BOTTOM LAYER: Mapped annotated visual feedback
            mapped_image = result.plot(line_width=2)
            st.image(mapped_image, caption="Output bounding alignment", use_container_width=True)
    else:
        st.markdown("<div style='color:#9ca3af; text-align:center; padding:2rem; border:1px solid #222226; border-radius:6px; background-color:#121214;'>Awaiting image upload and analysis loop.</div>", unsafe_allow_html=True)