import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# Load your custom trained model weights
model = YOLO("best.pt")

# Set geometric wide layout configurations
st.set_page_config(page_title="Vera Metric", layout="wide")

# Inject premium Inter font and custom styled variables directly matching the images
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
    
    /* Secondary Button: Upload Another Image */
    .stButton>button {
        width: 100%;
        background-color: #121214 !important;
        color: #f3f4f6 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        padding: 0.85rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1f1f24 !important;
        border-color: #3f3f46 !important;
    }
    
    /* Primary Button: Run Analysis */
    .stButton>button[data-testid="baseButton-primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
    }
    .stButton>button[data-testid="baseButton-primary"]:hover {
        background-color: #e63636 !important;
    }
    
    /* Expander Accordion Overrides */
    .stDetails {
        border: 1px solid #222226 !important;
        background-color: #121214 !important;
        border-radius: 6px !important;
        margin-bottom: 1rem !important;
    }
    .stDetails summary {
        background-color: #121214 !important;
        color: #ffffff !important;
        padding: 0.85rem 1.25rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Sample Card Components matching Image 1 */
    .sample-card-container {
        background-color: #1f1f24;
        border: 1px solid #2a2a30;
        border-radius: 6px;
        overflow: hidden;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .sample-thumb-placeholder {
        width: 100%;
        height: 80px;
        background-color: #1a1a1e;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        color: #8b929e;
        border-bottom: 1px solid #222226;
        letter-spacing: 0.5px;
    }
    
    /* Hiding Streamlit file uploader default design elements to match Image 2 */
    [data-testid="stFileUploader"] {
        background-color: #121214 !important;
        border: none !important;
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #161619 !important;
        border: 1px dashed #222226 !important;
        border-radius: 6px !important;
        padding: 2.5rem 1.5rem !important;
    }
    [data-testid="stFileUploader"] section > button {
        display: none !important; /* Removes native browse button entirely */
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #8b929e !important;
    }
    /* Completely removes native file download/list row display info */
    [data-testid="stFileUploaderFileName"], .stFileUploaderFile, [data-testid="stFileUploaderDeleteBtn"] {
        display: none !important;
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
    
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    # Condition 1: Setup Workspace Configuration Dropzone / Grid
    if st.session_state.uploaded_image is None:
        
        # Collapsible container layout matching Image 2
        with st.expander("Choose a sample configuration", expanded=False):
            samples = ["water_meter_000853.jpg", "water_meter_000746.jpg", "water_meter_000597.jpg"]
            grid_cols = st.columns(3)
            
            for i, sample_name in enumerate(samples):
                with grid_cols[i]:
                    short_name = sample_name.replace("water_", "")
                    id_number = short_name.split('_')[-1].split('.')[0]
                    
                    # Exact visual mockup structure matching Image 1
                    st.markdown(
                        f"""
                        <div class="sample-card-container">
                            <div class="sample-thumb-placeholder">📷&nbsp;&nbsp;<span style="color:#7289da;">[{id_number}]</span></div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    if st.button(f"{short_name}", key=f"btn_{sample_name}"):
                        if os.path.exists(sample_name):
                            st.session_state.uploaded_image = Image.open(sample_name)
                            st.rerun()
                        else:
                            st.error(f"Sample asset '{sample_name}' not found.")

        # Clean File Drop / Select Drag-area matching Image 2 style context
        uploaded_file = st.file_uploader(
            "Drag and drop file here\n\nLimit 2MB per file • JPG, JPEG, PNG, WEBP, BMP", 
            type=["jpg", "jpeg", "png", "webp", "bmp"], 
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            if uploaded_file.size > 2 * 1024 * 1024:
                st.error("File size exceeds the 2MB limit. Please upload a compressed or smaller structural layout file.")
            else:
                st.session_state.uploaded_image = Image.open(uploaded_file)
                st.rerun()

    # Condition 2: Active presentation image preview screen context
    if st.session_state.uploaded_image is not None:
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("+ Upload Another Image"):
                st.session_state.uploaded_image = None
                st.rerun()
                
        with btn_col2:
            analyse_btn = st.button("Run Analysis", type="primary")
            
        st.image(st.session_state.uploaded_image, caption="Source alignment geometry", use_container_width=True)

with col2:
    st.markdown("<h2>Processed Output</h2>", unsafe_allow_html=True)
    
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
        st.markdown(
            """
            <div style='color:#9ca3af; text-align:center; padding:2rem; border:1px solid #222226; border-radius:6px; background-color:#121214; font-size:0.95rem;'>
                Awaiting image upload and analysis loop.
            </div>
            """, 
            unsafe_allow_html=True
        )