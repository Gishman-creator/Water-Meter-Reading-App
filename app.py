import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import base64
from io import BytesIO

def get_image_base64(img_path):
    try:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img.thumbnail((400, 300))
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        pass
    return ""

img_853 = get_image_base64("water_meter_000853.jpg")
img_746 = get_image_base64("water_meter_000746.jpg")
img_597 = get_image_base64("water_meter_000597.jpg")

# Load your custom trained model weights
model = YOLO("best.pt")

# Set geometric wide layout configurations
st.set_page_config(page_title="Vera Metric", layout="wide")

# Initialize session state variables
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Handle sample selections via query parameters
if "sample" in st.query_params:
    sample_name = st.query_params["sample"]
    if os.path.exists(sample_name):
        st.session_state.uploaded_image = Image.open(sample_name)
        st.session_state.run_analysis = False
        st.session_state.analysis_results = None
    st.query_params.clear()
    st.rerun()


# Inject premium Inter font and custom styled variables directly matching the images
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0b0c !important;
        color: #f3f4f6 !important;
    }
    h1, h2, h3, h4, h5, h6, label, p {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Panel styling via container keys */
    .st-key-source-panel, .st-key-processed-panel {
        background-color: #121214 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        padding: 1.5rem !important;
    }
    
    /* Expander Accordion Overrides to match collapsible-header */
    .stDetails, [data-testid="stExpander"], [data-testid="stDetails"] {
        border: 1px solid #222226 !important;
        background-color: transparent !important;
        border-radius: 6px !important;
        margin-bottom: 0.5rem !important;
    }
    .stDetails summary, [data-testid="stExpander"] summary, [data-testid="stDetails"] summary {
        background-color: #1a1a1e !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
    }
    .stDetails summary:hover, [data-testid="stExpander"] summary:hover, [data-testid="stDetails"] summary:hover {
        background-color: #1f1f24 !important;
    }
    /* Expander internal content block overrides */
    .stDetails [data-testid="stVerticalBlock"], [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        padding: 0.5rem 0 !important;
    }
    
    /* Section titles styling */
    .section-title {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: #4b5563 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sample Grid styling via Streamlit columns and customized buttons */
    div[class*="st-key-card-"] button {
        background-color: #161619 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        overflow: hidden !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        text-align: center !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        padding: 0 !important;
        height: auto !important;
        width: 100% !important;
    }

    div[class*="st-key-card-"] button:hover {
        border-color: #3f3f46 !important;
        transform: translateY(-2px) !important;
        background-color: #161619 !important;
    }

    div[class*="st-key-card-"] button div[data-testid="stMarkdownContainer"] {
        padding: 0.5rem 0.4rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
        display: block !important;
        margin: 0 !important;
    }

    div[class*="st-key-card-"] button p {
        color: #58a6ff !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: block !important;
    }

    /* File Uploader styling wrapper */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #161619 !important;
        border: 1px dashed #222226 !important;
        border-radius: 6px !important;
        padding: 2.5rem 2rem !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: #3f3f46 !important;
    }
    [data-testid="stFileUploader"] button {
        display: none !important; /* Removes native browse button entirely */
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div, 
    [data-testid="stFileUploaderDropzoneInstructions"] > span, 
    [data-testid="stFileUploaderDropzoneInstructions"] > small {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "Drag and drop file here" !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #f3f4f6 !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"]::after {
        content: "Limit 2MB per file • JPG, JPEG, PNG, WEBP, BMP" !important;
        font-size: 0.75rem !important;
        color: #6b7280 !important;
        display: block !important;
        text-align: center !important;
    }
    /* Completely removes native file download/list row display info */
    [data-testid="stFileUploaderFileName"], .stFileUploaderFile, [data-testid="stFileUploaderDeleteBtn"] {
        display: none !important;
    }
    
    /* Primary and secondary structural actions styles */
    .stButton {
        width: 100% !important;
    }
    .stButton > button {
        width: 100% !important;
        background-color: #121214 !important;
        color: #f3f4f6 !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        padding: 0.85rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #1f1f24 !important;
        border-color: #3f3f46 !important;
    }
    .stButton > button * {
        width: auto !important;
        flex: none !important;
    }
    .stButton > button[data-testid*="secondary"]::before {
        content: "+" !important;
        font-size: 1.4rem !important;
        margin-right: 0.4rem !important;
        font-weight: 400 !important;
        display: inline-block !important;
        line-height: 1 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[data-testid*="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border: 1px solid transparent !important;
    }
    .stButton > button[data-testid*="primary"]:hover {
        background-color: #e63636 !important;
        border-color: transparent !important;
    }
    .stButton > button[data-testid*="primary"]:disabled {
        background-color: #552222 !important;
        color: #9ca3af !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    .stButton > button:disabled {
        cursor: not-allowed !important;
    }
    
    /* Value Sequence Output Readout Box */
    div[data-testid="stTextInput"] {
        margin-bottom: 1.5rem !important;
    }
    div[data-testid="stTextInput"] label {
        display: block !important;
        font-size: 0.85rem !important;
        color: #9ca3af !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTextInput"] input {
        width: 100% !important;
        background-color: #1a1a1e !important;
        border: 1px solid #222226 !important;
        color: #ffffff !important;
        font-family: monospace !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        letter-spacing: 3px !important;
        text-align: center !important;
        padding: 0.75rem !important;
        border-radius: 6px !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] input:disabled {
        opacity: 0.8 !important;
        cursor: not-allowed !important;
    }
    
    /* Image Display frames */
    .image-container, [data-testid="stImage"] {
        margin-top: 1rem !important;
        width: 100% !important;
    }
    .image-container img, [data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
        border-radius: 4px !important;
        border: 1px solid #222226 !important;
        display: block !important;
    }
    .image-caption, [data-testid="stImageCaption"] {
        font-size: 0.8rem !important;
        color: #9ca3af !important;
        margin-top: 0.5rem !important;
        text-align: left !important;
    }
    
    /* Dynamic placeholder view */
    .placeholder-text {
        color: #9ca3af !important;
        text-align: center !important;
        padding: 2rem !important;
        border: 1px solid #222226 !important;
        border-radius: 6px !important;
        background-color: #121214 !important;
        font-size: 0.95rem !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Inject base64 sample thumbnails as button backgrounds
st.markdown(
    f"""
    <style>
    div[class*="st-key-card-853"] button::before {{
        content: "" !important;
        width: 100% !important;
        aspect-ratio: 4 / 3 !important;
        background-image: url("{img_853}") !important;
        background-size: cover !important;
        background-position: center !important;
        border-bottom: 1px solid #222226 !important;
        display: block !important;
    }}
    div[class*="st-key-card-746"] button::before {{
        content: "" !important;
        width: 100% !important;
        aspect-ratio: 4 / 3 !important;
        background-image: url("{img_746}") !important;
        background-size: cover !important;
        background-position: center !important;
        border-bottom: 1px solid #222226 !important;
        display: block !important;
    }}
    div[class*="st-key-card-597"] button::before {{
        content: "" !important;
        width: 100% !important;
        aspect-ratio: 4 / 3 !important;
        background-image: url("{img_597}") !important;
        background-size: cover !important;
        background-position: center !important;
        border-bottom: 1px solid #222226 !important;
        display: block !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown("<h1 style='color:#ffffff; font-weight:700; letter-spacing:-0.04em; margin-bottom:0.25rem;'>Vera Metric</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle' style='color:#9ca3af; margin-bottom:3.5rem; font-size:1rem;'>Optical character recognition for utility meters</p>", unsafe_allow_html=True)

# Define Main Structural Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='section-title'>Source File</div>", unsafe_allow_html=True)
    
    with st.container(key="source-panel"):
        # Condition 1: Setup Workspace Configuration Dropzone / Grid
        if st.session_state.uploaded_image is None:
            # Collapsible container layout matching mockup
            with st.expander("Choose a sample configuration", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    with st.container(key="card-853"):
                        if st.button("meter_000853.jpg", key="btn_click_853", use_container_width=True):
                            st.session_state.uploaded_image = Image.open("water_meter_000853.jpg")
                            st.session_state.run_analysis = False
                            st.session_state.analysis_results = None
                            st.rerun()
                with col_b:
                    with st.container(key="card-746"):
                        if st.button("meter_000746.jpg", key="btn_click_746", use_container_width=True):
                            st.session_state.uploaded_image = Image.open("water_meter_000746.jpg")
                            st.session_state.run_analysis = False
                            st.session_state.analysis_results = None
                            st.rerun()
                with col_c:
                    with st.container(key="card-597"):
                        if st.button("meter_000597.jpg", key="btn_click_597", use_container_width=True):
                            st.session_state.uploaded_image = Image.open("water_meter_000597.jpg")
                            st.session_state.run_analysis = False
                            st.session_state.analysis_results = None
                            st.rerun()

            # Clean File Drop / Select Drag-area matching mockup style
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
                    st.session_state.run_analysis = False
                    st.session_state.analysis_results = None
                    st.rerun()

        # Condition 2: Active presentation image preview screen context
        else:
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                if st.button("Upload Another Image", use_container_width=True):
                    st.session_state.uploaded_image = None
                    st.session_state.run_analysis = False
                    st.session_state.analysis_results = None
                    st.rerun()
                    
            with btn_col2:
                if st.session_state.run_analysis:
                    st.button("Analyzing...", type="primary", use_container_width=True, disabled=True)
                else:
                    if st.button("Run Analysis", type="primary", use_container_width=True):
                        st.session_state.run_analysis = True
                        st.rerun()
                
            st.image(st.session_state.uploaded_image, caption="Source alignment geometry", use_container_width=True)

with col2:
    st.markdown("<div class='section-title'>Processed Output</div>", unsafe_allow_html=True)
    
    if st.session_state.uploaded_image is not None:
        if st.session_state.run_analysis:
            with st.container(key="processed-panel"):
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
                    
                    mapped_image = result.plot(line_width=2)
                    
                    st.session_state.analysis_results = {
                        "recognized_number": recognized_number,
                        "mapped_image": mapped_image
                    }
                    st.session_state.run_analysis = False
                    st.rerun()
                    
        elif st.session_state.analysis_results is not None:
            with st.container(key="processed-panel"):
                st.text_input("Value Sequence Readout", value=st.session_state.analysis_results["recognized_number"], disabled=True)
                st.image(st.session_state.analysis_results["mapped_image"], caption="Output bounding alignment", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="placeholder-text">
                    Awaiting image upload and analysis loop.
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class="placeholder-text">
                Awaiting image upload and analysis loop.
            </div>
            """, 
            unsafe_allow_html=True
        )