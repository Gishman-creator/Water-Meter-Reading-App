# Vera Metric - Water Meter Reading Web Application

An intelligent, premium computer vision application optimized for utility data management. This application provides a responsive web interface to upload images of physical water meters, detect key structures (casing and reading windows), extract individual digits, and sort them horizontally to output the current water meter reading.

The project utilizes a custom-trained **YOLO11** model to execute real-time object detection and segmentation.

---

## Connected Repositories & Resources

*   **Web App Source Code:** [Gishman-creator/Water-Meter-Reading-App](https://github.com/Gishman-creator/Water-Meter-Reading-App) (This repository)
*   **Model Training Pipeline:** [Gishman-creator/water-meter-model-pipeline](https://github.com/Gishman-creator/water-meter-model-pipeline) — Contains the Google Colab notebooks, dataset preparation scripts, YOLO11 training details, and model fine-tuning steps.
*   **Live Web Application:** [Streamlit App - Vera Metric](https://water-meter-reading-app-2shehkejqgq9jubvlx9v36.streamlit.app/#vera-metric)

---

## Features

*   **Real-time YOLO11 Inference:** Fast and precise detection of physical casings (`meter`), digits window (`window`), and numeric digits (`0-9`, `u` for unreadable).
*   **Tilt & Rotation Robustness:** The underlying model is trained with extensive augmentations (`shear`, `degrees`, `scale`, `mosaic`) to handle camera tilt, perspective distortion, and poor lighting.
*   **Digit Parsing & Sorting:** Reconstructs the physical counter digit sequence by sorting digit bounding boxes from left to right.
*   **Interactive Demo:** Pre-loaded with three high-resolution sample water meter images for instant testing.
*   **Sleek User Interface:** Custom CSS implementation styling Streamlit into a responsive, premium dark-mode application using the Google Inter font.

---

## Local Development Setup

To run this application locally, follow these steps:

### Prerequisites
*   Python 3.8 to 3.11 (YOLO11 requires Python >= 3.8)
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/Gishman-creator/Water-Meter-Reading-App.git
cd Water-Meter-Reading-App
```

### 2. Set Up a Virtual Environment (Recommended)
Creating a virtual environment ensures that the application dependencies do not conflict with other Python projects on your system.

**On Windows (PowerShell/CMD):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries, including `streamlit` and the `ultralytics` YOLO engine. We use `opencv-python-headless` to keep headless installations clean.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Dev Server
Launch the Streamlit web application:
```bash
streamlit run app.py
```
The app will automatically compile and open in your default browser at `http://localhost:8501`.

---

## Streamlit Cloud Deployment

This app is optimized for seamless deployment to **Streamlit Community Cloud**.

### Setup for Deployment
1. Ensure your latest changes are pushed to your public GitHub repository (`main` or `master` branch).
2. The `requirements.txt` file is pre-configured with `opencv-python-headless` instead of `opencv-python`.
   > [!IMPORTANT]
   > Streamlit Community Cloud runs on a headless Linux environment. Using standard `opencv-python` causes missing shared library errors (e.g., `libGL.so.1`) because X11/GUI libraries are not installed on headless servers. `opencv-python-headless` resolves this automatically.

### Steps to Deploy
1. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/) and log in using your GitHub account.
2. Click **New app** in the workspace.
3. Select your repository: `Gishman-creator/Water-Meter-Reading-App`.
4. Choose the active branch (e.g., `main`).
5. Specify the Main file path: `app.py`.
6. Click **Deploy!**

Streamlit Cloud will automatically provision a container, install dependencies from `requirements.txt`, and launch your app.

---

## Project Structure

```
├── app.py                  # Main Streamlit web application and custom CSS styling
├── best.pt                 # Saved weights for the custom-trained YOLO11 model
├── requirements.txt        # Python library dependencies
├── water_meter_000597.jpg  # Preloaded sample image 1
├── water_meter_000746.jpg  # Preloaded sample image 2
├── water_meter_000853.jpg  # Preloaded sample image 3
└── README.md               # Project documentation (this file)
```

---

## Model Class Reference

The YOLO11 model detects the following classes:
*   `0: meter` — Outer structural casing of the water meter.
*   `1: window` — Reading counter window frame containing digits.
*   `2-11: 0-9` — Numerical values.
*   `12: u` — Unreadable/partially rotated digit (falls back to a placeholder value `?` or omitted to keep accuracy high).
