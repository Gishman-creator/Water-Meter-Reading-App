import streamlit as st
from ultralytics import YOLO
from PIL import Image
import base64
import os
import io

# Load custom model
model = YOLO("best.pt")

# Set configurations matching premium wide structure
st.set_page_config(page_title="Vera Metric", layout="wide")

# Initialize session state variables if not present
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "image_name" not in st.session_state:
    st.session_state.image_name = ""
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# Callback helpers triggered via query parameters or hidden inputs
query_params = st.query_params

if "action" in query_params:
    action = query_params["action"]
    if action == "reset":
        st.session_state.uploaded_image = None
        st.session_state.image_name = ""
        st.session_state.run_analysis = False
        st.query_params.clear()
        st.rerun()
    elif action == "analyze":
        st.session_state.run_analysis = True
        st.query_params.clear()
        st.rerun()
    elif action.startswith("sample_"):
        sample_name = action.replace("sample_", "")
        if os.path.exists(sample_name):
            st.session_state.uploaded_image = Image.open(sample_name)
            st.session_state.image_name = sample_name
            st.session_state.run_analysis = False
        st.query_params.clear()
        st.rerun()

# 2MB File size check implementation hidden upload catch
uploaded_file = st.file_uploader("upload_hidden", type=["jpg", "jpeg", "png", "webp", "bmp"], key="hidden_uploader", label_visibility="collapsed")
if uploaded_file is not None:
    if uploaded_file.size > 2 * 1024 * 1024:
        st.error("File size exceeds the 2MB limit.")
    else:
        st.session_state.uploaded_image = Image.open(uploaded_file)
        st.session_state.image_name = uploaded_file.name
        st.session_state.run_analysis = False
        st.rerun()

# Convert Images to Base64 data strings for structural custom tags safely
def get_image_base64(img):
    if img is None:
        return ""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()

# Render template structures matching conditions
source_preview_html = "[Selected Meter Snapshot]"
if st.session_state.uploaded_image is not None:
    img_b64 = get_image_base64(st.session_state.uploaded_image)
    source_preview_html = f'<img src="{img_b64}" style="max-height:248px; object-fit:contain;" />'

# Core calculation block running model inference matching requested framework
recognized_number = "Awaiting..."
output_preview_html = "[Annotated Bounding Visual Output]"

if st.session_state.uploaded_image is not None and st.session_state.run_analysis:
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
    recognized_number = "".join([item[1] for item in digit_detections]) or "No digits recognized."
    
    # Render plotted arrays back into Base64 format string parameters
    mapped_array = result.plot(line_width=2)
    mapped_image = Image.fromarray(mapped_array[..., ::-1]) # Convert BGR to RGB
    out_b64 = get_image_base64(mapped_image)
    output_preview_html = f'<img src="{out_b64}" style="max-height:248px; object-fit:contain;" />'

# Original HTML Layout string - completely untouched with simple unique replace tags
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vera Metric</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            background-color: #0b0b0c !important;
            color: #f3f4f6 !important;
            padding: 2rem;
            min-height: 100vh;
        }

        h1, h2, h3, h4, h5, h6, label, p {
            font-family: 'Inter', sans-serif !important;
        }

        h1 {
            color: #ffffff;
            font-weight: 700;
            letter-spacing: -0.04em;
            margin-bottom: 0.25rem;
        }

        .subtitle {
            color: #9ca3af;
            margin-bottom: 3.5rem;
            font-size: 1rem;
        }

        .section-title {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #4b5563;
            margin-bottom: 1rem;
        }

        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        @media (max-width: 900px) {
            .container {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background-color: #121214;
            border: 1px solid #222226;
            border-radius: 6px;
            padding: 1.5rem;
            min-height: 300px;
        }

        .collapsible-header {
            width: 100%;
            background-color: #1a1a1e;
            border: 1px solid #222226;
            color: #ffffff;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            user-select: none;
            margin-bottom: 0.5rem;
        }

        .collapsible-header:hover {
            background-color: #1f1f24;
            border-color: #3f3f46;
        }

        .collapsible-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.25s ease-out, margin-bottom 0.25s ease-out;
        }

        .collapsible-content.expanded {
            max-height: 200px;
            margin-bottom: 1.5rem;
        }

        .sample-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            padding-top: 0.5rem;
        }

        .sample-card {
            background-color: #1a1a1e;
            border: 1px solid #222226;
            border-radius: 4px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .sample-card:hover {
            border-color: #3f3f46;
            transform: translateY(-2px);
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

        .sample-card span {
            display: block;
            padding: 0.4rem;
            font-size: 0.75rem;
            color: #9ca3af;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .file-uploader {
            border: 1px dashed #222226;
            border-radius: 6px;
            padding: 2.5rem 2rem;
            text-align: center;
            background-color: #161619;
            cursor: pointer;
            transition: border-color 0.2s;
        }

        .file-uploader:hover {
            border-color: #3f3f46;
        }

        .file-uploader p {
            font-size: 0.9rem;
            color: #9ca3af;
        }

        .btn-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .html-btn {
            width: 100%;
            background-color: #121214;
            color: #f3f4f6;
            border: 1px solid #222226;
            border-radius: 6px;
            padding: 0.85rem;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
            text-decoration: none;
        }

        .html-btn:hover {
            background-color: #1f1f24;
            border-color: #3f3f46;
        }

        .html-btn.primary {
            background-color: #ff4b4b;
            color: white;
            border: 1px solid transparent;
        }

        .html-btn.primary:hover {
            background-color: #e63636;
        }

        .icon-plus {
            display: inline-block;
            width: 14px;
            height: 14px;
            background: linear-gradient(to right, currentColor 2px, transparent 2px) no-repeat 6px 0,
                        linear-gradient(to bottom, currentColor 2px, transparent 2px) no-repeat 0 6px;
            background-size: 2px 14px, 14px 2px;
        }

        .readout-group {
            margin-bottom: 1.5rem;
        }

        .readout-group label {
            display: block;
            font-size: 0.85rem;
            color: #9ca3af;
            margin-bottom: 0.5rem;
        }

        .custom-input {
            width: 100%;
            background-color: #1a1a1e;
            border: 1px solid #222226;
            color: #ffffff;
            font-family: monospace;
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-align: center;
            padding: 0.75rem;
            border-radius: 6px;
            outline: none;
            opacity: 0.8;
        }

        .image-container {
            margin-top: 1rem;
            width: 100%;
        }

        .image-container img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            border: 1px solid #222226;
            display: block;
        }

        .image-caption {
            font-size: 0.8rem;
            color: #9ca3af;
            margin-top: 0.5rem;
            text-align: left;
        }

        .placeholder-text {
            color: #9ca3af;
            text-align: center;
            padding: 2rem;
            border: 1px solid #222226;
            border-radius: 6px;
            background-color: #121214;
            font-size: 0.95rem;
        }
        
        div[data-testid="stFileUploader"] {
            display: none;
        }}
    </style>
</head>
<body>

    <h1>Vera Metric</h1>
    <p class="subtitle">Optical character recognition for utility meters</p>

    <div class="container">
        <div>
            <div class="section-title">Source File</div>
            <div class="panel">
                
                <div id="upload-state" style="display: __UPLOAD_DISPLAY__;">
                    <div class="collapsible-header" onclick="toggleGrid()">
                        <span>Choose a sample configuration</span>
                        <span id="arrow-icon">▼</span>
                    </div>
                    
                    <div id="grid-content" class="collapsible-content">
                        <div class="sample-grid">
                            <div class="sample-card" onclick="window.parent.location.href='?action=sample_water_meter_000853.jpg'">
                                <div class="sample-thumb-placeholder">📷 [000853]</div>
                                <span>meter_000853.jpg</span>
                            </div>
                            <div class="sample-card" onclick="window.parent.location.href='?action=sample_water_meter_000746.jpg'">
                                <div class="sample-thumb-placeholder">📷 [000746]</div>
                                <span>meter_000746.jpg</span>
                            </div>
                            <div class="sample-card" onclick="window.parent.location.href='?action=sample_water_meter_000597.jpg'">
                                <div class="sample-thumb-placeholder">📷 [000597]</div>
                                <span>meter_000597.jpg</span>
                            </div>
                        </div>
                    </div>

                    <div class="file-uploader" onclick="window.parent.document.querySelector('input[type=file]').click()">
                        <p>Drag and drop file here</p>
                        <p style="font-size: 0.75rem; margin-top: 0.5rem; color: #6b7280;">Limit 2MB per file • JPG, JPEG, PNG, WEBP, BMP</p>
                    </div>
                </div>

                <div id="active-state" style="display: __ACTIVE_DISPLAY__;">
                    <div class="btn-row">
                        <a href="?action=reset" target="_self" class="html-btn">
                            <i class="icon-plus"></i> Upload Another Image
                        </a>
                        <a href="?action=analyze" target="_self" class="html-btn primary">Run Analysis</a>
                    </div>
                    <div class="image-container">
                        <div id="selected-preview-box" style="width:100%; display:flex; align-items:center; justify-content:center; background-color:#1a1a1e; border: 1px solid #222226; border-radius:4px;">
                            __SOURCE_PREVIEW__
                        </div>
                        <div class="image-caption">Source alignment geometry (__IMAGE_NAME__)</div>
                    </div>
                </div>

            </div>
        </div>

        <div>
            <div class="section-title">Processed Output</div>
            
            <div id="output-awaiting" class="placeholder-text" style="display: __AWAITING_DISPLAY__;">
                Awaiting image upload and analysis loop.
            </div>

            <div id="output-results" class="panel" style="display: __RESULTS_DISPLAY__;">
                <div class="readout-group">
                    <label>Value Sequence Readout</label>
                    <input type="text" class="custom-input" value="__RECOGNIZED_NUMBER__" disabled />
                </div>
                
                <div class="image-container">
                    <div style="width:100%; display:flex; align-items:center; justify-content:center; background-color:#1a1a1e; border: 1px solid #222226; border-radius:4px;">
                        __OUTPUT_PREVIEW__
                    </div>
                    <div class="image-caption">Output bounding alignment</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function toggleGrid() {
            const content = document.getElementById('grid-content');
            const arrow = document.getElementById('arrow-icon');
            if (content.classList.contains('expanded')) {
                content.classList.remove('expanded');
                arrow.innerText = '▼';
            } else {
                content.classList.add('expanded');
                arrow.innerText = '▲';
            }
        }
    </script>
</body>
</html>
"""

# Replace tags safely without altering CSS code blocks
rendered_html = html_template.replace("__UPLOAD_DISPLAY__", "block" if st.session_state.uploaded_image is None else "none") \
                             .replace("__ACTIVE_DISPLAY__", "none" if st.session_state.uploaded_image is None else "block") \
                             .replace("__AWAITING_DISPLAY__", "none" if st.session_state.run_analysis else "block") \
                             .replace("__RESULTS_DISPLAY__", "block" if st.session_state.run_analysis else "none") \
                             .replace("__SOURCE_PREVIEW__", source_preview_html) \
                             .replace("__IMAGE_NAME__", st.session_state.image_name) \
                             .replace("__RECOGNIZED_NUMBER__", recognized_number) \
                             .replace("__OUTPUT_PREVIEW__", output_preview_html)

# Inject finalized clean code output safely
st.markdown(rendered_html, unsafe_allow_html=True)