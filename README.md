# FishyGuard

FishyGuard is a Python desktop application that detects phishing content in emails and messages using a fine-tuned DistilBERT transformer. It features a clean GUI built with Tkinter and ttk for easy input and result display. The app stores prediction history in a local SQLite database and is packaged as a standalone deployable application.

## Features

- Phishing detection on text-based content using a transformer model  
- User-friendly GUI built with Tkinter and ttk  
- Local SQLite database for storing prediction history  
- Packaged as a standalone desktop app for easy deployment  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/fishyguard.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python fishyguard.py
   ```


Usage:
Launch the app, enter email or message text, and get instant phishing detection results. The app logs past predictions in the local database for review.

Requirements:
```
- Python 3.8+
- Tkinter (usually included with Python)
- PyTorch
- Hugging Face Transformers
- SQLite
```

Warning:
```
Phishing detection uses machine learning and may have false positives or negatives. Use as a supplementary tool, not a sole defense mechanism.
```

Contributing:
Contributions, issue reports, and pull requests are welcome to improve the project.

License:
MIT License
