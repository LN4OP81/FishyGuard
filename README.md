# FishyGuard - AI Phishing Detector

FishyGuard is a desktop application built with Python that serves as an AI-powered phishing detection engine for text-based content like emails and messages. It features a user-friendly graphical interface and uses a trained transformer model to achieve high-accuracy detection.

## Features

- **AI-Powered Detection:** Uses a trained transformer model (DistilBERT) to analyze text and predict whether it is phishing or safe.  
- **Simple UI:** An intuitive interface built with Tkinter for easy text input and clear results.  
- **Prediction History:** Utilizes a local SQLite database to maintain a history of all past predictions.  

## How to Run

1. **Clone the repository:**  
   ```bash
   git clone <your-repo-url>
   cd FishyGuard
   ```
   
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Tools Used:
- Python
- Tkinter / ttk
- Hugging Face Transformers
- PyTorch
- SQLite
- PyInstaller
- Pillow
