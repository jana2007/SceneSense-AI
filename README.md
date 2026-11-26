# 👁️ SceneSense AI
### AI-Powered Visual Understanding Assistant

SceneSense AI is a computer vision application that transforms images into meaningful insights using artificial intelligence.

It combines object detection, image captioning, and optical character recognition (OCR) to help users understand the contents of images through an interactive dashboard.

## ✨ Features

- **Object Detection:** Identifies objects in images using YOLOv8.
- **Scene Understanding:** Generates natural-language image descriptions using BLIP.
- **Text Recognition:** Extracts readable text from images using EasyOCR.
- **Live Camera:** Capture images directly through your device camera for analysis.
- **Detection History:** Stores previous analyses using SQLite.
- **Analytics Dashboard:** Displays object statistics, detection frequency, and analysis activity.
- **PDF Reports:** Generates downloadable reports containing analysis results.
- **Interactive UI:** Dark-themed dashboard with sidebar navigation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| YOLOv8 | Object detection |
| BLIP | Image captioning |
| EasyOCR | Text extraction |
| OpenCV | Image processing |
| PyTorch | Deep learning framework |
| SQLite | Analysis history storage |
| ReportLab | PDF report generation |
| NumPy | Numerical operations |

## 📁 Project Structure

```text
SceneSense/
│
├── app.py
├── detector.py
├── captioner.py
├── ocr_reader.py
├── history.py
├── report_generator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/jana2007/SceneSense-AI.git
```

### 2. Navigate to the project folder

```bash
cd SceneSense
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

**Note:** The AI models may download their required weights the first time they are initialized. An internet connection is needed for those initial downloads.

## 🚀 How It Works

1. Upload an image or capture one using the live camera.
2. YOLOv8 identifies objects present in the image.
3. BLIP generates a natural-language scene description.
4. EasyOCR extracts readable text.
5. The results are displayed in the application.
6. Analysis details are saved in the SQLite database.
7. Users can explore previous analyses and analytics.
8. A PDF report can be downloaded for each analysis.

## 📊 Application Modules

- Overview Dashboard
- Image Analysis
- Live Camera
- Detection History
- Analytics Dashboard
- PDF Report Generation

## 🔮 Future Improvements

- Real-time video object detection
- Improved scene understanding
- More advanced object recognition
- Cloud-based deployment
- User authentication and personalized history
- Additional image analysis capabilities

## 👩‍💻 Developer

**Jana Daisy**

Computer Science and Engineering Student

## 📌 Project Information

**Project:** SceneSense AI  
**Domain:** Artificial Intelligence and Computer Vision  
**Status:** Core features implemented; further improvements planned.

---

*Built with Python, Computer Vision, and Artificial Intelligence.*