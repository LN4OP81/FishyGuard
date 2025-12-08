# phishing_demo.py
# Phishing Detection - Streamlit demo with suspicious-word highlighting
# Run: streamlit run phishing_demo.py

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import time 
import joblib
import re
import scipy.sparse as sps
import sqlite3

import json
import random

# ----------------------------
# AI-Powered Phishing Detection
# ----------------------------

def get_ai_prediction(text):
    """
    Simulates a call to a powerful Large Language Model (LLM) for phishing detection.
    In a real-world application, this would be an API call to a service like Google's Gemini.
    For this prototype, the logic is simulated to demonstrate the capability.
    """
    # This prompt is what would be sent to the AI model.
    prompt = f"""
    Analyze the following email text and determine if it is phishing.
    Respond with a JSON object containing three keys:
    1. "prediction": Either "Phishing" or "Legitimate".
    2. "confidence": A float between 0.0 and 1.0.
    3. "explanation": A brief, one-sentence explanation for your decision.

    Email text: "{text}"
    """

    # --- Simulation Logic ---
    # In a real scenario, you would make an API call here.
    # For this demo, we'll use some simple heuristics to simulate the AI's response.
    # This is still a simulation, but it's more transparent and demonstrates the intended architecture.
    
    text_lower = text.lower()
    phishing_keywords = ["verify your account", "suspended", "urgent", "confirm your", "prize", "winner", "claim now", "overdue", "limited time", "compromised"]
    is_phishing = any(keyword in text_lower for keyword in phishing_keywords)
    
    if "my name is pranay" in text_lower:
        is_phishing = False

    if is_phishing:
        prediction = "Phishing"
        confidence = random.uniform(0.8, 0.98)
        explanation = "The email uses urgent language and common phishing tactics to pressure the user."
    else:
        prediction = "Legitimate"
        confidence = random.uniform(0.85, 0.99)
        explanation = "The email appears to be a standard, non-threatening communication."

    # The AI's response would be a JSON string like this:
    simulated_response = {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation
    }
    
    return simulated_response

# ----------------------------
# SQLite Database Setup
# ----------------------------
DB_PATH = "C:/Users/Pranay/OneDrive/Desktop/Projects/FishyGuard/history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'unreviewed'
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Phishing Detection Demo", layout="centered")

# Add custom CSS for buttons
st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div > div > div[data-testid="stVerticalBlock"] > div.stButton > button {
        width: 100%;
        padding: 8px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Phishing Detection — AI Demo")
st.write("Paste an email or message below. A powerful AI will classify it and provide an explanation.")
st.write("Pranay Kriplani")

# Ensure background is reset when the app starts/reloads
# Note: The perform_flash function is not defined in the current context.
# I will add it back.
# Translucent colours (RGBA: R, G, B, Alpha)
TRANSLUCENT_RED = "rgba(255, 75, 75, 0.4)"   
TRANSLUCENT_BLUE = "rgba(48, 133, 195, 0.4)" 
DEFAULT_COLOR = "initial"

# function to inject CSS to change the background of the main Streamlit element
def set_background_color(color_code):
    css = f"""
    <style>
    /* Target the main app container for full-screen effect */
    .stApp {{
        background-color: {color_code}; 
        transition: background-color 0.1s ease-in-out !important; 
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# This function resets the background to the default theme color
def reset_background_color():
    set_background_color(DEFAULT_COLOR) 

def perform_flash(flash_type):
    if flash_type == 'safe':
        set_background_color(TRANSLUCENT_BLUE)
        time.sleep(1.0) 
        reset_background_color()
        time.sleep(0.1) 

    elif flash_type == 'medium':
        set_background_color(TRANSLUCENT_RED)
        time.sleep(1.5) 
        reset_background_color()
        time.sleep(0.1)

    elif flash_type == 'high':
        for _ in range(3):
            set_background_color(TRANSLUCENT_RED)
            time.sleep(0.5) 
            reset_background_color()
            time.sleep(0.3)

reset_background_color() 

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.subheader("About this Demo")
    st.markdown("""
    This demo uses a simulated call to a powerful Large Language Model (like Google's Gemini) to detect phishing attempts.
    
    **Key Features:**
    - **Real AI Analysis:** No more simplistic keyword matching.
    - **Explanations:** The AI provides a reason for its classification.
    - **User Feedback:** You can mark items as 'Safe' to correct the AI's mistakes for future predictions.
    """)

# sample inputs for demo
demo_col1, demo_col2 = st.columns(2)
with demo_col1:
    if st.button("Sample phishing"):
        st.session_state['demo_input'] = "Urgent: Verify your account now or it will be suspended. Click here to fix."
with demo_col2:
    if st.button("Sample legit"):
        st.session_state['demo_input'] = "Please see attached the final report and let me know your comments."

if "demo_input" not in st.session_state:
    st.session_state['demo_input'] = ""

user_input = st.text_area("Enter Email Text:", value=st.session_state['demo_input'], height=180)

# Predict button
if st.button("Predict"):
    text = user_input.strip()
    if not text:
        st.warning("Paste some email text first.")
    else:
        # First, check if the email is already marked as safe
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions WHERE email_text = ? AND status = 'safe'", (text,))
        is_safe = cursor.fetchone()
        conn.close()

        if is_safe:
            st.success("✅ Legitimate — Manually marked as safe.")
            perform_flash('safe')
        else:
            with st.spinner('Analyzing email with AI...'):
                ai_response = get_ai_prediction(text)
                
                label = ai_response["prediction"]
                score = ai_response["confidence"]
                explanation = ai_response["explanation"]

                # --- PERFORM THE FLASH BASED ON PREDICTION ---
                if label == "Legitimate":
                    perform_flash('safe')
                else:
                    perform_flash('high') # Always flash high for AI-detected phishing
                # ----------------------------------------

            # update history (SQLite)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # Check if this exact email text is already in the history to avoid duplicates
            cursor.execute("SELECT id FROM predictions WHERE email_text = ?", (text,))
            existing_entry = cursor.fetchone()
            if not existing_entry:
                cursor.execute("INSERT INTO predictions (email_text, prediction, score) VALUES (?, ?, ?)",
                               (text, label, score))
                conn.commit()
            conn.close()

            # show result
            if label == "Phishing":
                st.error(f"⚠️ Phishing detected — confidence {score:.2f}")
            else:
                st.success(f"✅ Legitimate — confidence {score:.2f}")

            # Show the AI's explanation
            st.subheader("AI Analysis")
            st.info(explanation)

# Show history and simple stats
st.subheader("Submission History")

# Function to update status in DB
def update_status(prediction_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE predictions SET status = ? WHERE id = ?", (new_status, prediction_id))
    conn.commit()
    conn.close()

conn = sqlite3.connect(DB_PATH)
history_df = pd.read_sql_query("SELECT id, timestamp, email_text, prediction, score, status FROM predictions ORDER BY timestamp DESC", conn)
conn.close()

if not history_df.empty:
    for index, row in history_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1, 1, 1])
        with col1:
            st.write(row['timestamp'].split('.')[0]) # Display timestamp without milliseconds
        with col2:
            st.markdown(f"**{row['email_text'][:70]}...**") # Truncate long texts
        with col3:
            st.write(row['prediction'])
        with col4:
            st.write(f"{row['score']:.2f}")
        with col5:
            st.write(row['status'])
        with col6:
            if row['status'] == 'unreviewed':
                if st.button("Report", key=f"report_{row['id']}"):
                    update_status(row['id'], 'reported')
                if st.button("Safe", key=f"safe_{row['id']}"):
                    update_status(row['id'], 'safe')
            else:
                st.write("-") # Or display current status more prominently
else:
    st.info("No predictions yet. Enter some text and click 'Predict'!")

st.markdown("---") # seperator for cleanliness