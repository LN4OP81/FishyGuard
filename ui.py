import tkinter as tk
from tkinter import messagebox, ttk, TOP, BOTH, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PhishingUI:
    def __init__(self, root, model_engine, db, analyst=None):
        self.root = root
        self.model = model_engine
        self.db = db
        self.analyst = analyst
        
        self.root.title("FishyGuard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0f172a")
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#1e293b", 
                        foreground="#f8fafc", 
                        fieldbackground="#1e293b",
                        rowheight=25,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", 
                        background="#334155", 
                        foreground="#f8fafc", 
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', '#38bdf8')])

    def setup_ui(self):
        # --- LEFT SIDEBAR ---
        self.sidebar = tk.Frame(self.root, bg="#1e293b", width=220)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="FISHY-GUARD", font=("Segoe UI", 18, "bold"), 
                 bg="#1e293b", fg="#38bdf8").pack(pady=20)
        
        btn_config = {"font": ("Segoe UI", 10, "bold"), "relief": "flat", "padx": 10, "pady": 10, "cursor": "hand2"}
        
        # Dashboard Button
        tk.Button(self.sidebar, text="📊 VIEW ANALYTICS", command=self.show_dashboard,
                  bg="#1e293b", fg="white", **btn_config).pack(fill="x", padx=15, pady=5)
        
        # Clear Text Button
        tk.Button(self.sidebar, text="🧹 CLEAR INPUT", command=self.clear_text_input,
                  bg="#1e293b", fg="white", highlightthickness=1, 
                  highlightbackground="#334155", **btn_config).pack(fill="x", padx=15, pady=5)
        
        # Clear History Button
        tk.Button(self.sidebar, text="🗑 WIPE LOGS", command=self.clear_ui_history,
                  bg="#1e293b", fg="white", **btn_config).pack(fill="x", padx=15, pady=5)

        # --- MAIN WORKSPACE ---
        self.main_area = tk.Frame(self.root, bg="#0f172a")
        self.main_area.pack(side="right", expand=True, fill="both", padx=30, pady=20)

        tk.Label(self.main_area, text="Paste email content for forensic analysis:",
                 font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8").pack(anchor="w", pady=(0, 10))
        
        self.text_input = tk.Text(self.main_area, height=12, bg="#1e293b", fg="#f8fafc",
                                   insertbackground="white", font=("Consolas", 11),
                                   padx=15, pady=15, relief="flat")
        self.text_input.pack(fill="x", pady=(0, 15))

        # SCAN BUTTON
        self.scan_btn = tk.Button(self.main_area, text="SCAN", command=self.scan_email,
                                  bg="#10b981", fg="white", font=("Segoe UI", 12, "bold"),
                                  relief="flat", pady=12, cursor="hand2")
        self.scan_btn.pack(fill="x", pady=5)

        self.result_label = tk.Label(self.main_area, text="SYSTEM READY", font=("Segoe UI", 11, "bold"),
                                     bg="#0f172a", fg="#94a3b8")
        self.result_label.pack(pady=15)

        # History Section
        tk.Label(self.main_area, text="SCAN LOG HISTORY", font=("Segoe UI", 10, "bold"),
                 bg="#0f172a", fg="#38bdf8").pack(anchor="w", pady=(10, 5))

        self.history_tree = ttk.Treeview(self.main_area, columns=("ID", "Prediction", "Score", "Time"), show='headings')
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Prediction", text="RESULT")
        self.history_tree.heading("Score", text="CONFIDENCE")
        self.history_tree.heading("Time", text="TIMESTAMP")
        self.history_tree.pack(fill=BOTH, expand=True)
        
        self.load_history()

    def clear_text_input(self):
        self.text_input.delete("1.0", tk.END)
        self.result_label.config(text="SYSTEM READY", fg="#94a3b8")
        self.scan_btn.config(bg="#10b981")

    def scan_email(self):
        email_content = self.text_input.get("1.0", tk.END).strip()
        if not email_content:
            messagebox.showwarning("Warning", "Please enter email text.")
            return

        result = self.model.predict(email_content)
        prediction = result['label']
        score = result['score']

        if prediction == "Phishing":
            self.result_label.config(text=f"CRITICAL: {prediction} ({score:.2f})", fg="#ef4444")
            self.scan_btn.config(bg="#ef4444")
        else:
            self.result_label.config(text=f"SAFE: {prediction} ({score:.2f})", fg="#10b981")
            self.scan_btn.config(bg="#10b981")

        self.db.add_prediction(email_content, prediction, score)
        self.load_history()

        if prediction == "Phishing" and self.analyst:
            if messagebox.askyesno("Deep-Dive", "Threat detected. Run AI Forensic Analysis?"):
                self.run_deep_dive(email_content)

    def run_deep_dive(self, text):
        analysis = self.analyst.analyze_threat(text)
        dive_window = Toplevel(self.root)
        dive_window.title("Forensic Analysis Report")
        dive_window.geometry("600x500")
        dive_window.configure(bg="#0f172a")
        
        tk.Label(dive_window, text="AI ANALYST REPORT", font=("Segoe UI", 14, "bold"), 
                 bg="#0f172a", fg="#38bdf8").pack(pady=10)

        report_text = tk.Text(dive_window, wrap=tk.WORD, padx=20, pady=20, 
                              bg="#1e293b", fg="#f8fafc", font=("Consolas", 10), relief="flat")
        report_text.insert(tk.END, analysis)
        report_text.config(state=tk.DISABLED)
        report_text.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def load_history(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for row in self.db.get_all_predictions():
            self.history_tree.insert("", tk.END, values=(row[0], row[2], f"{row[3]:.2f}", row[4]))

    def clear_ui_history(self):
        if messagebox.askyesno("Confirm", "Delete all detection history?"):
            self.db.clear_history()
            self.load_history()
            self.result_label.config(text="SYSTEM READY", fg="#94a3b8")
            self.scan_btn.config(bg="#10b981")

    def show_dashboard(self):
        stats = self.db.get_stats()
        trends = self.db.get_daily_trends()
        dashboard_window = Toplevel(self.root)
        dashboard_window.title("Security Analytics Dashboard")
        dashboard_window.geometry("900x550")
        dashboard_window.configure(bg="#0f172a")

        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), facecolor="#0f172a")
        labels = list(stats.keys())
        values = list(stats.values())
        if any(values):
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#10b981', '#ef4444'])
        ax1.set_title("Detection Distribution")
        if trends:
            dates = [t[0] for t in trends]
            counts = [t[1] for t in trends]
            ax2.bar(dates, counts, color='#38bdf8')
            ax2.set_title("Threats Over Time")
            plt.setp(ax2.get_xticklabels(), rotation=45)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)
