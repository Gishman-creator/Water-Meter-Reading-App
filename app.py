import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# Load your custom trained model weights
model = YOLO("best.pt")

# Set geometric wide layout configurations
st.set_page_config(page_title="Vera Metric", layout="wide")

# Inject premium Inter font and custom styled variables directly matching the HTML specification
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
    
    /* Panel containers styling */
    div[data-testid="stBlock"] {
        background-color: #121214;
        border: 1px solid #222226;
        border-radius: 6px;
        padding: 1.5rem;
    }
    
    /* Section titles styling */
    [data-testid="stMarkdownContainer"] h2 {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: #4b5563 !important;
        margin-bottom: 1rem !important;
        border-bottom: none !important;
    }
    
    /* Standard UI Button configuration */
    .stButton>button {
        width: 100%;
        background-color: #121214 !important;
        color: #f3f4f6 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        padding: 0.85rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1f1f24 !important;
        border-color: #3f3f46 !important;
    }
    
    /* Primary UI Button configuration override */
    .stButton>button[data-testid="baseButton-primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border: 1px solid transparent !important;
    }
    .stButton>button[data-testid="baseButton-primary"]:hover {
        background-color: #e63636 !important;
    }
    
    /* Expander Accordion Overrides to match sample layout */
    .stDetails {
        border: 1px solid #222226 !important;
        background-color: #1a1a1e !important;
        border-radius: 6px !important;
        margin-bottom: 0.5rem !important;
    }
    .stDetails summary {
        background-color: #1a1a1e !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Sample Card Components */
    .sample-card-container {
        background-color: #1a1a1e;
        border: 1px solid #222226;
        border-radius: 4px;
        overflow: hidden;
        text-align: center;
        transition: all 0.2s ease;
        margin-bottom: 1rem;
    }
    .sample-card-container:hover {
        border-color: #3f3f46;
    }
    .sample-thumb-placeholder {
        width: 100%;
        height: 70px;
        background-color: #26262b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        color: #71717a;
        border-bottom: 1px solid #222226;
    }
    
    /* File Uploader area modifications */
    [data-testid="stFileUploader"] {
        border: 1px dashed #222226 !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        background-color: #161619 !important;
    }
    
    /* Monospace Sequence Output Box styling */
    input {
        background-color: #1a1a1e !important;
        border: 1px solid #222226 !important;
        color: #ffffff !important;
        font-family: monospace !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        letter-spacing: 3px !important;
        text-align: center !important;
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown("<h1 style='color:#ffffff; font-weight:700; letter-spacing:-0.04em; margin-bottom:0.25rem;'>Vera Metric</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; margin-bottom:3.5rem; font-size:1rem;'>Optical character recognition for utility meters</p>", unsafe_allow_html=True)

# Define Main Structural Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h2>Source File</h2>", unsafe_allow_html=True)
    
    # Initialize track state logic
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    # Condition 1: Upload and Sample selection workflow configuration 
    if st.session_state.uploaded_image is None:
        
        # Collapsible container mimicking the custom accordion panel layout
        with st.expander("Choose a sample configuration", expanded=False):
            samples = ["water_meter_000853.jpg", "water_meter_000746.jpg", "water_meter_000597.jpg"]
            grid_cols = st.columns(3)
            
            for i, sample_name in enumerate(samples):
                with grid_cols[i]:
                    # Render visual card architecture wrapper block
                    short_name = sample_name.replace("water_", "")
                    st.markdown(
                        f"""
                        <div class="sample-card-container">
                            <div class="sample-thumb-placeholder">📷 [{short_name.split('_')[-1].split('.')[0]}]</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    # Trigger structural state modification on press
                    if st.button(f"Select {short_name}", key=f"btn_{sample_name}"):
                        if os.path.exists(sample_name):
                            st.session_state.uploaded_image = Image.open(sample_name)
                            st.rerun()
                        else:
                            st.error(f"Sample asset '{sample_name}' not found.")

        # Streamlit Custom File drop alignment interface wrapper boundary 
        uploaded_file = st.file_uploader("Upload snapshot", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
        if uploaded_file:
            if uploaded_file.size > 2 * 1024 * 1024:
                st.error("File size exceeds the 2MB limit. Please upload a compressed or smaller structural layout file.")
            else:
                st.session_state.uploaded_image = Image.open(uploaded_file)
                st.rerun()

    # Condition 2: Active presentation layout context
    if st.session_state.uploaded_image is not None:
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("➕ Upload Another Image"):
                st.session_state.uploaded_image = None
                st.rerun()
                
        with btn_col2:
            analyse_btn = st.button("Run Analysis", type="primary")
            
        st.image(st.session_state.uploaded_image, caption="Source alignment geometry", use_container_width=True)

with col2:
    st.markdown("<h2>Processed Output</h2>", unsafe_allow_html=True)
    
    # Process execution condition loop block checks
    if st.session_state.uploaded_image is not None and 'analyse_btn' in locals() and analyse_btn:
        with st.spinner("Processing structural frames..."):
            results = model.predict(
                source=st.session_state.uploaded_image,
                conf=0.25,
                iou=0.60,
                agnostic_nms=True
            )
            result = results[0]
            
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
            
            mapped_image = result.plot(line_width=2)
            st.image(mapped_image, caption="Output bounding alignment", use_container_width=True)
    else:
        # Default dynamic framework status state matching the exact HTML layout structure
        st.markdown(
            """
            <div style='color:#9ca3af; text-align:center; padding:2rem; border:1px solid #222226; border-radius:6px; background-color:#121214; font-size:0.95rem;'>
                Awaiting image upload and analysis loop.
            </div>
            """, 
            unsafe_allow_html=True
        )