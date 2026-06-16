# Legacy Scribe 🚀

Legacy Scribe is an Agentic AI tool designed to automate the translation, deconstruction, and modernization of legacy codebases (like COBOL, PL/I, JCL, and Legacy SQL) into modern, cloud-native Python/FastAPI solutions.

This project was built as a prototype inspired by the **Legacy Modernization through Agentic AI Challenge (1a)** issued at the **India Agentic AI Summit 2026** (Delhi, June 19).

---

## ✨ Features

- **Multi-language Legacy Parsing**: Supports COBOL, PL/I, JCL, Legacy SQL schemas, and mainframe logs.
- **Neural Deconstruction Console**: Watch the agent process syntax, state-machine transitions, and security implications in real-time.
- **ROI & Effort Estimation**: Estimates developer effort (in hours), modernization costs (based on a blended rate), and potential annual savings.
- **Modern Tech Stack Target**: Generates equivalent modular Python code leveraging modern frameworks like FastAPI.
- **Security Audit**: Automatically scans for legacy security patterns and lists modern remediation steps.
- **Automated Report Generation**: Download comprehensive TXT reports containing all analysis metrics and the modernized code snippet.

---

## 🛠️ Prerequisites

- Python 3.9 or higher
- [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/gcloud) installed
- Authenticated GCP account with Vertex AI API access

---

## 🚀 Getting Started

### 1. Clone & Set Up Directory

```bash
git clone <your-repo-url>
cd Legacy_Scribe
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Authenticate with Google Cloud

Ensure you have credentials set up for Vertex AI. The app uses Application Default Credentials (ADC):

```bash
gcloud auth application-default login
```

### 5. Launch the App

```bash
streamlit run app.py
```

---

## ⚙️ How it Works Under the Hood

1. **Streamlit UI** handles code inputs, model configuration, and dynamically displays progress and results.
2. **Vertex AI SDK (`google-genai`)** is called using the latest Gemini models (e.g. `gemini-1.5-flash` or `gemini-1.5-pro`).
3. **Structured Outputs** are enforced using Pydantic schemas, ensuring the response is always returned in a reliable, valid format.
4. **ROI calculation logic** translates complexity metrics into estimated hours and modernization costs (blended at $150/hr).

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
