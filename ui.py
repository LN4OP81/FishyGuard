import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from model import PhishingModel
from database import PredictionHistory
import base64
from PIL import Image, ImageTk
import io

class FishyGuardUI:
    def __init__(self, master):
        self.master = master
        master.title("FishyGuard")
        master.geometry("800x600")

        # --- Style ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#0078d7", foreground="white", font=('Helvetica', 10, 'bold'))
        self.style.map("TButton", background=[('active', '#005a9e')])
        self.style.configure("Treeview", rowheight=25, fieldbackground="#f0f0f0")
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        self.model = PhishingModel()
        self.db = PredictionHistory()

        # --- Main frame ---
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input frame ---
        input_frame = ttk.LabelFrame(main_frame, text="Enter Email Text", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        self.text_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=('Helvetica', 10))
        self.text_area.pack(fill=tk.X, expand=True, padx=5, pady=5)

        self.analyze_button = ttk.Button(input_frame, text="Analyze", command=self.analyze_text)
        self.analyze_button.pack(pady=5)

        # --- Result frame ---
        result_frame = ttk.LabelFrame(main_frame, text="Analysis Result", padding="10")
        result_frame.pack(fill=tk.X, pady=5)

        self.result_label = ttk.Label(result_frame, text="Awaiting analysis...", font=("Helvetica", 14, "italic"), foreground="#888")
        self.result_label.pack(pady=10)

        # --- History frame ---
        history_frame = ttk.LabelFrame(main_frame, text="Prediction History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.history_tree = ttk.Treeview(history_frame, columns=("Timestamp", "Text", "Prediction"), show="headings")
        self.history_tree.heading("Timestamp", text="Timestamp")
        self.history_tree.heading("Text", text="Text")
        self.history_tree.heading("Prediction", text="Prediction")
        self.history_tree.column("Timestamp", width=150, anchor='w')
        self.history_tree.column("Text", width=400, anchor='w')
        self.history_tree.column("Prediction", width=100, anchor='center')
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.load_history()

    def analyze_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to analyze.")
            return

        self.analyze_button.config(state=tk.DISABLED)
        self.result_label.config(text="Analyzing...", foreground="#888", font=("Helvetica", 14, "italic"))
        self.master.update_idletasks()

        try:
            prediction, confidence = self.model.predict(text)
            self.db.add_prediction(text, prediction, confidence)
            self.load_history()

            if prediction == "Phishing":
                self.result_label.config(text=f"Phishing ({confidence:.2f})", foreground="red", font=("Helvetica", 14, "bold"))
            else:
                self.result_label.config(text=f"Safe ({confidence:.2f})", foreground="green", font=("Helvetica", 14, "bold"))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {e}")
            self.result_label.config(text="Error", foreground="orange")
        finally:
            self.analyze_button.config(state=tk.NORMAL)

    def load_history(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        
        history = self.db.get_all_predictions()
        for row in history:
            # id, text, prediction, score, timestamp
            self.history_tree.insert("", tk.END, values=(row[4], row[1][:70] + "...", row[2]))