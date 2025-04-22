# Phishing AI Detector 🔍🛡️

A full-stack machine learning solution for phishing detection, combining a trained AI model, a real-time web application, and a Chrome browser extension. Built using Python, FastAPI, Streamlit, and JavaScript, this project enables phishing detection through both desktop and browser workflows.

---

## 🚀 Project Highlights

- ✅ Trained a phishing detection model on Kaggle-sourced data of real vs. fake promotional messages.
- 🌍 Built a **Streamlit web interface** to interact with the model.
- 🔌 Developed a **FastAPI backend** that serves predictions via a REST API.
- 🧩 Integrated a **Chrome extension** that detects phishing directly from any webpage.
- 📊 Demonstrated complete deployment from model training to multi-platform user access.

---

## 🧠 Technologies Used

- Python 3.10+
- FastAPI, Streamlit
- scikit-learn, pandas, NumPy, joblib
- JavaScript, HTML, CSS (for Chrome extension)
- Jupyter Notebooks (for model training)
- Kaggle (dataset source)

---

## 🗂️ Project Structure

```
phishing_project/
├── chrome-extension/           # Chrome extension source code
├── data/                       # Raw and cleaned training data
├── models/                     # Trained model + vectorizer
│   ├── clf.joblib
│   └── vect.joblib
├── notebook/                   # Model training Jupyter notebook
│   └── phishing_detector.ipynb
├── src/                        # FastAPI backend server
│   └── api.py
├── ui/                         # Streamlit frontend UI
│   └── app.py
├── requirements.txt
└── README.md
```

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/phishing-ai-detector.git
cd phishing-ai-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔌 Running the Backend API (FastAPI)

1. Navigate to the `src/` folder:

```bash
cd src
```

2. Start the server using Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

Test endpoint at: `http://localhost:8000/docs`

---

## 🌍 Running the Streamlit Web App

1. Open a new terminal.
2. Navigate to the `ui/` folder:

```bash
cd ui
```

3. Start the app:

```bash
streamlit run app.py
```

The web UI will launch at: `http://localhost:8501`

- Enter promotional or ad text
- The app will communicate with the backend to detect phishing

---

## 🧩 Installing & Using the Chrome Extension

### Installation

1. Open Google Chrome and go to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load Unpacked** and select the `chrome-extension/` folder

### Usage

- Highlight any suspicious text on a website
- Right-click and choose **"Check for Phishing"**
- The extension will send it to the local FastAPI server and display the result

🟡 **Note**: Ensure the backend (`uvicorn`) is running locally at `http://localhost:8000` while using the extension.

---

## 📊 Model Training Overview

The model was trained on a Kaggle dataset of labeled promotional messages. Workflow includes:

1. **Text preprocessing**: tokenization, stopword removal, TF-IDF vectorization
2. **Modeling**: Logistic Regression
3. **Evaluation**: Accuracy, precision, recall, ROC-AUC
4. **Serialization**: Saved as `.joblib` files

All steps are documented in `notebook/phishing_detector.ipynb`.

---

## ✅ Key Accomplishments

- Built a production-ready ML pipeline
- Integrated a browser-native phishing detection extension
- Created both frontend (Streamlit) and backend (FastAPI) services
- Bridged machine learning with real-world cybersecurity application

---

## 🧑‍💻 Author

**Dante Warhola**  
University of Pittsburgh — Computer Science  
Powerlifting Club Business Manager | Cybersecurity Enthusiast  
[LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com)

---

## 📜 License

This project is licensed under the MIT License.


---

## 🐳 Running the Project with Docker

This project includes a Dockerfile to run both the backend API (FastAPI) and frontend UI (Streamlit) together inside a single container.

### 🔧 Build the Docker Image

From the root of the project:

```bash
docker build -t phishing-ai .
```

### ▶️ Run the Docker Container

```bash
docker run -p 8000:8000 -p 8501:8501 phishing-ai
```

This will expose:
- **FastAPI API** at `http://localhost:8000`
- **Streamlit UI** at `http://localhost:8501`

Make sure Docker Desktop is running before building or launching the container.
