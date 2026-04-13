# FishyGuard

FishyGuard is a Python-based desktop cybersecurity tool that detects phishing emails using a hybrid AI detection system.  
It combines a transformer-based machine learning model with rule-based filtering and provides an interactive graphical interface for analyzing suspicious email content.

The system also stores scan history, provides analytics dashboards, and allows deeper forensic analysis using AI.

---

# Features

### AI-Powered Detection
Uses a DistilBERT transformer model from Hugging Face to classify email text as **Phishing** or **Safe**.

### Hybrid Detection System
Combines AI predictions with heuristic checks to improve detection reliability.

### Interactive Desktop Interface
A modern Tkinter-based graphical interface designed for fast scanning and clear results.

### Detection History
All scans are stored in a local SQLite database so previous analyses can be reviewed.

### Security Analytics Dashboard
Built-in analytics with visual charts showing:

- Detection distribution (Safe vs Phishing)
- Phishing activity trends over time

### AI Forensic Analysis
Suspicious emails can be analyzed further using the **Google Gemini API**, which generates a short cybersecurity-style explanation of the threat indicators.

### Log Management
Users can:

- Clear text input  
- Delete stored scan history  
- View past detection logs  

---

# Application Screenshots

## Main Detection Interface
![Main Interface](screenshots/main_interface.png)

## Scan History Log
![Scan History](screenshots/history_log.png)

## Security Analytics Dashboard
![Analytics Dashboard](screenshots/dashboard.png)

## AI Forensic Analysis Report
![Forensic Analysis](screenshots/forensic_report.png)

---

# How It Works

1. The user pastes email content into the application.
2. The system runs a **hybrid detection pipeline**:
   - Heuristic filtering layer
   - Transformer-based AI classification (DistilBERT)
3. The model predicts whether the email is **Phishing** or **Safe**.
4. The result and confidence score are stored in a **local SQLite database**.
5. The analytics dashboard visualizes detection statistics and trends.
6. If phishing is detected, the user can optionally run **AI forensic analysis** for a detailed explanation.

---

# Project Architecture

```
main.py        -> Application entry point
ui.py          -> Graphical user interface
model.py       -> AI phishing detection model
database.py    -> SQLite database for prediction history
analyst.py     -> AI-based forensic threat analysis
```

---

# Example Detection

### Input Email

```
Urgent action required! Your account has been compromised.
Click the link below immediately to verify your identity.
```

### Output

```
Prediction: Phishing
Confidence: 0.97
```

### AI Analyst Explanation

- Email creates urgency to pressure the recipient.
- Requests account verification through an external link.
- Language patterns match common phishing templates.

---

# How to Run

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd AI-Phishing-Detection-Engine
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Add your API Key

Insert your **Google Gemini API key** inside `main.py`.

## 4. Run the application

```bash
python main.py
```

---

# Technologies Used

- Python
- Tkinter / ttk
- Hugging Face Transformers
- DistilBERT
- PyTorch
- SQLite
- Matplotlib
- Google Gemini API
