
import streamlit as st
import numpy as np
from PIL import Image

from detector import SceneDetector
from captioner import SceneCaptioner
from ocr_reader import SceneOCR
from history import AnalysisHistory
from report_generator import generate_pdf_report


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="SceneSense AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM UI DESIGN
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #10101A;
    color: #FFFFFF;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: #171727;
    border-right: 1px solid #34344A;
}

section[data-testid="stSidebar"] h1 {
    color: #A78BFA;
    font-size: 27px;
}

section[data-testid="stSidebar"] p {
    color: #B8B8CC;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

p, label {
    color: #D0D0E0;
}

[data-testid="stMetric"] {
    background: #1B1B2A;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #34344A;
}

[data-testid="stMetricLabel"] {
    color: #B8B8CC;
}

[data-testid="stMetricValue"] {
    color: #A78BFA;
}

.stButton > button {
    background: #8B5CF6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #7C3AED;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #8B5CF6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: #7C3AED;
    color: white;
}

.stTextInput input,
.stTextArea textarea {
    background: #1B1B2A;
    color: white;
    border: 1px solid #454560;
    border-radius: 8px;
}

[data-testid="stFileUploader"] {
    background: #1B1B2A;
    border: 1px dashed #8B5CF6;
    border-radius: 12px;
    padding: 15px;
}

hr {
    border-color: #34344A;
}

.hero {
    background: linear-gradient(
        120deg,
        #252044,
        #35235B,
        #241B40
    );
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #55418B;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #D5C9F5;
    font-size: 15px;
}

.feature-card {
    background: #1B1B2A;
    padding: 22px;
    border: 1px solid #454064;
    border-radius: 14px;
    min-height: 145px;
    margin-bottom: 16px;
}

.feature-card h3 {
    color: #A78BFA !important;
    font-size: 19px;
    margin-bottom: 12px;
}

.feature-card p {
    color: #B8B8CC;
    font-size: 14px;
    line-height: 1.6;
}

.footer {
    text-align: center;
    color: #77778F;
    font-size: 12px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD AI MODELS
# ==================================================

@st.cache_resource
def load_detector():
    return SceneDetector()


@st.cache_resource
def load_captioner():
    return SceneCaptioner()


@st.cache_resource
def load_ocr():
    return SceneOCR()


@st.cache_resource
def load_history():
    return AnalysisHistory()


# ==================================================
# COMMON FUNCTIONS
# ==================================================

def show_pdf_download(
    filename,
    detected_objects,
    scene_description,
    extracted_text
):

    pdf_report = generate_pdf_report(
        filename,
        detected_objects,
        scene_description,
        extracted_text
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_report,
        file_name="SceneSense_Analysis_Report.pdf",
        mime="application/pdf",
        key="download_" + filename
    )


def analyze_image(image, filename):

    image_array = np.array(image.convert("RGB"))

    # OBJECT DETECTION

    with st.spinner("Detecting objects..."):

        detector = load_detector()

        output_image, detected_objects = (
            detector.detect_objects(image_array)
        )

    # SCENE DESCRIPTION

    with st.spinner("Generating scene description..."):

        captioner = load_captioner()

        scene_description = captioner.generate_caption(image)

    # OCR

    with st.spinner("Extracting text..."):

        ocr = load_ocr()

        extracted_text = ocr.extract_text(image_array)

    # SAVE HISTORY

    history = load_history()

    history.save_analysis(
        filename,
        detected_objects,
        scene_description,
        extracted_text
    )

    # RESULTS

    st.divider()

    st.markdown("## 📊 Analysis Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Objects Detected",
        len(detected_objects)
    )

    col2.metric(
        "Unique Object Types",
        len(set(obj["name"] for obj in detected_objects))
    )

    left, right = st.columns(2)

    with left:

        st.markdown("### 🎯 Object Detection")

        st.image(
            output_image,
            use_container_width=True
        )

        if detected_objects:

            for index, obj in enumerate(detected_objects, 1):

                st.write(
                    f"**{index}. {obj['name'].title()}** "
                    f"— {obj['confidence']}% confidence"
                )

        else:

            st.warning("No objects detected.")

    with right:

        st.markdown("### 🧠 Scene Description")

        st.info(scene_description)

        st.markdown("### 📝 Extracted Text")

        if extracted_text:

            for index, item in enumerate(extracted_text, 1):

                st.write(
                    f"**{index}. {item['text']}** "
                    f"— {item['confidence']}% confidence"
                )

        else:

            st.warning("No readable text found.")

    st.divider()

    st.markdown("### 📄 Your Analysis Report")

    show_pdf_download(
        filename,
        detected_objects,
        scene_description,
        extracted_text
    )

    st.success("Analysis completed and saved successfully!")


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.markdown("# 👁️ SceneSense")

    st.caption("AI VISUAL UNDERSTANDING PLATFORM")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Overview",
            "🖼️ Image Analysis",
            "📷 Live Camera",
            "📚 Detection History",
            "📊 Analytics"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ⚡ AI ENGINE")

    st.caption("YOLOv8 · Object Detection")
    st.caption("BLIP · Scene Description")
    st.caption("EasyOCR · Text Extraction")

    st.divider()

    st.caption("SceneSense AI")
    st.caption("Computer Vision Project")


# ==================================================
# GLOBAL HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>👁️ SceneSense AI</h1>
    <p>
        Transform images into intelligent insights.
        Detect objects, understand scenes and extract text
        using artificial intelligence.
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# PAGE 1: OVERVIEW
# ==================================================

if page == "🏠 Overview":

    st.markdown("## Welcome to SceneSense")

    st.write(
        "Your intelligent visual understanding workspace. "
        "Analyze images, explore objects and discover insights."
    )

    history = load_history()

    analytics = history.get_analytics()

    records = history.get_history()

    st.markdown("### 📈 Platform Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Images Analyzed",
        analytics["total_images"]
    )

    col2.metric(
        "Objects Detected",
        analytics["total_objects"]
    )

    col3.metric(
        "Unique Objects",
        analytics["unique_objects"]
    )

    st.divider()

    st.markdown("### ✨ What can SceneSense do?")

    feature1, feature2 = st.columns(2)

    with feature1:

        st.html("""
        <div class="feature-card">
            <h3>🎯 Object Detection</h3>
            <p>
                Identify objects in images using the
                YOLOv8 computer vision model.
            </p>
        </div>
        """)

        st.html("""
        <div class="feature-card">
            <h3>🧠 Scene Understanding</h3>
            <p>
                Generate natural-language descriptions
                of images using the BLIP AI model.
            </p>
        </div>
        """)

    with feature2:

        st.html("""
        <div class="feature-card">
            <h3>📝 Text Recognition</h3>
            <p>
                Extract readable text from images
                using EasyOCR.
            </p>
        </div>
        """)

        st.html("""
        <div class="feature-card">
            <h3>📄 PDF Reports</h3>
            <p>
                Generate downloadable reports containing
                your complete image analysis.
            </p>
        </div>
        """)

    st.divider()

    st.markdown("### 🕒 Recent Activity")

    if records:

        for record in records[:5]:

            with st.container(border=True):

                st.markdown(
                    f"**📷 {record['filename']}**"
                )

                st.caption(record["analysis_time"])

                st.write(
                    f"Description: {record['scene_description']}"
                )

                st.write(
                    f"Objects detected: "
                    f"{len(record['detected_objects'])}"
                )

    else:

        st.info(
            "No activity yet. Start by analyzing your first image!"
        )


# ==================================================
# PAGE 2: IMAGE ANALYSIS
# ==================================================

elif page == "🖼️ Image Analysis":

    st.markdown("## 🖼️ Image Analysis")

    st.write(
        "Upload an image and let SceneSense understand it."
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        st.markdown("### Original Image")

        st.image(
            image,
            use_container_width=True
        )

        if st.button(
            "🔍 Analyze Image",
            key="analyze_upload"
        ):

            analyze_image(
                image,
                uploaded_file.name
            )

    else:

        st.info("Upload an image to begin analysis.")


# ==================================================
# PAGE 3: LIVE CAMERA
# ==================================================

elif page == "📷 Live Camera":

    st.markdown("## 📷 Live Camera")

    st.write(
        "Capture a photo using your device camera "
        "and analyze it with SceneSense AI."
    )

    camera_image = st.camera_input(
        "Take a picture",
        key="scenesense_camera"
    )

    if camera_image is not None:

        captured_image = Image.open(
            camera_image
        ).convert("RGB")

        st.markdown("### Captured Image")

        st.image(
            captured_image,
            use_container_width=True
        )

        if st.button(
            "🔍 Analyze Captured Image",
            key="analyze_camera"
        ):

            analyze_image(
                captured_image,
                "Webcam_Capture.jpg"
            )


# ==================================================
# PAGE 4: DETECTION HISTORY
# ==================================================

elif page == "📚 Detection History":

    st.markdown("## 📚 Detection History")

    st.write(
        "Explore all your previously analyzed images."
    )

    history = load_history()

    records = history.get_history()

    if records:

        st.metric(
            "Total Analyses",
            len(records)
        )

        st.divider()

        for record in records:

            with st.expander(
                f"🖼️ {record['filename']} — "
                f"{record['analysis_time']}"
            ):

                st.markdown("### 🧠 Scene Description")

                st.info(record["scene_description"])

                st.markdown("### 🎯 Detected Objects")

                if record["detected_objects"]:

                    for obj in record["detected_objects"]:

                        st.write(
                            f"- **{obj['name'].title()}** "
                            f"({obj['confidence']}%)"
                        )

                else:

                    st.write("No objects detected.")

                st.markdown("### 📝 Extracted Text")

                if record["extracted_text"]:

                    for item in record["extracted_text"]:

                        st.write(
                            f"- {item['text']} "
                            f"({item['confidence']}%)"
                        )

                else:

                    st.write("No readable text found.")

    else:

        st.info(
            "Your history is empty. "
            "Analyze an image to start building your collection!"
        )


# ==================================================
# PAGE 5: ANALYTICS
# ==================================================

elif page == "📊 Analytics":

    st.markdown("## 📊 Analytics Dashboard")

    st.write(
        "Explore statistics and insights from your image analyses."
    )

    history = load_history()

    analytics = history.get_analytics()

    records = history.get_history()

    if analytics["total_images"] > 0:

        st.markdown("### Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Images Analyzed",
            analytics["total_images"]
        )

        col2.metric(
            "Objects Detected",
            analytics["total_objects"]
        )

        col3.metric(
            "Unique Object Types",
            analytics["unique_objects"]
        )

        st.divider()

        st.markdown("### 🎯 Object Detection Statistics")

        object_counts = analytics["object_counts"]

        if object_counts:

            sorted_objects = dict(
                sorted(
                    object_counts.items(),
                    key=lambda item: item[1],
                    reverse=True
                )
            )

            st.bar_chart(
                sorted_objects,
                horizontal=True
            )

            most_common = analytics["most_common"]

            if most_common:

                st.markdown("### 🏆 Most Detected Object")

                st.success(
                    f"{most_common[0][0]} is your most frequently "
                    f"detected object, appearing "
                    f"{most_common[0][1]} times."
                )

        st.divider()

        st.markdown("### 📋 Object Summary")

        for name, count in analytics["most_common"]:

            st.write(
                f"**{name}** — {count} detection(s)"
            )

        st.divider()

        st.markdown("### 🕒 Recent Activity")

        for record in records[:5]:

            with st.container(border=True):

                st.write(f"**📷 {record['filename']}**")

                st.caption(record["analysis_time"])

                st.write(
                    f"Objects detected: "
                    f"{len(record['detected_objects'])}"
                )

    else:

        st.info(
            "Your analytics dashboard is waiting for data. "
            "Analyze some images to see your statistics!"
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown("""
<div class="footer">
    SceneSense AI | Intelligent Visual Understanding
    <br><br>
    Built with Python · YOLOv8 · BLIP · EasyOCR · OpenCV · SQLite
</div>
""", unsafe_allow_html=True)
