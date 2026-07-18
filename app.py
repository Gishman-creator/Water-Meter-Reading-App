import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load your custom trained model weights
model = YOLO("best.pt")

st.set_page_config(page_title="AquaRead - Water Meter OCR", layout="wide")

st.markdown("# 💧 AquaRead")
st.markdown("### Computer Vision Water Meter Digit Recognition System")

# Recreates the exact side-by-side card layout from your design wireframe
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 UPLOAD METER IMAGE")
    uploaded_file = st.file_uploader("Drop water meter snapshot here", type=["jpg", "jpeg", "png", "webp", "bmp"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Snapshot", use_container_width=True)
        analyse_btn = st.button("🔍 ANALYSE METER", type="primary")

with col2:
    st.subheader("📊 DETECTION RESULT")
    
    if uploaded_file and 'analyse_btn' in locals() and analyse_btn:
        with st.spinner("Processing framework anomalies..."):
            # Run predictions with your custom thresholds
            results = model.predict(
                source=image,
                conf=0.25,
                iou=0.60,
                agnostic_nms=True
            )
            result = results[0]
            
            # Generate the visual bounding box mapping
            mapped_image = result.plot(line_width=2)
            st.image(mapped_image, caption="Mapped Structural Framework", use_container_width=True)
            
            # Extract bounding boxes and sort left-to-right
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
                
            st.text_input("Recognized Number Sequence Readout", value=recognized_number, disabled=True)