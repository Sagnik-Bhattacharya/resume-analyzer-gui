import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Scrollbar, Frame
from pdf2image import convert_from_path
from PIL import ImageTk
from docx import Document

class ResultScreen(ctk.CTkFrame):
    def __init__(self, master, analysis_data):
        super().__init__(master)

        self.analysis_data = analysis_data
        self.pdf_images = []  # store PDF pages to prevent GC

        # ---------------- MAIN SPLIT FRAME ----------------
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- LEFT FRAME: PDF / DOCX Preview ----------------
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        preview_label = ctk.CTkLabel(left_frame, text="Resume Preview", font=("Segoe UI", 18, "bold"))
        preview_label.pack(pady=(0, 10))

        # Scrollable canvas for multi-page PDF
        self.canvas = Canvas(left_frame, bg="#2B2B2B")
        self.scrollbar = Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#2B2B2B")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Load preview
        self.load_preview(analysis_data["filepath"])

        # ---------------- RIGHT FRAME: Analysis ----------------
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        title = ctk.CTkLabel(right_frame, text="Analysis Results", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(0, 20))

        # Scores
        scores_frame = ctk.CTkFrame(right_frame)
        scores_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(scores_frame, text=f"Match Score: {analysis_data['match_score']}%", font=("Segoe UI", 16, "bold"), text_color="#00FF00").pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(scores_frame, text=f"Similarity Score: {analysis_data['similarity_score']}%", font=("Segoe UI", 16), text_color="#00FFFF").pack(anchor="w", padx=10, pady=5)

        # Skill cards
        def create_skill_cards(frame, skills, color):
            card_frame = ctk.CTkFrame(frame)
            card_frame.pack(fill="x", pady=(0, 10))
            for skill in skills:
                lbl = ctk.CTkLabel(card_frame, text=skill, font=("Segoe UI", 12, "bold"), fg_color=color, corner_radius=15, padx=10, pady=5)
                lbl.pack(side="left", padx=5, pady=5)
        
        create_skill_cards(right_frame, analysis_data['matched_skills'], "#00FF00")
        create_skill_cards(right_frame, analysis_data['missing_skills'], "#FF5555")

        # Back button
        self.back_btn = ctk.CTkButton(right_frame, text="Analyze Another Resume", command=self.go_back)
        self.back_btn.pack(pady=(20, 0))

    # ---------------- LOAD PREVIEW ----------------
    def load_preview(self, filepath: Path):
        if not filepath.exists():
            lbl = ctk.CTkLabel(self.scrollable_frame, text=f"File not found: {filepath}", font=("Segoe UI", 12))
            lbl.pack()
            return

        if filepath.suffix.lower() == ".pdf":
            try:
                pages = convert_from_path(filepath, dpi=120)
                for page in pages:
                    page.thumbnail((500, 700))
                    img = ImageTk.PhotoImage(page)
                    self.pdf_images.append(img)
                    lbl = ctk.CTkLabel(self.scrollable_frame, image=img)
                    lbl.pack(pady=10)
            except Exception as e:
                lbl = ctk.CTkLabel(self.scrollable_frame, text=f"Error loading PDF: {e}")
                lbl.pack()
        elif filepath.suffix.lower() == ".docx":
            try:
                doc = Document(filepath)
                lines = [p.text for p in doc.paragraphs if p.text]
                preview_text = "\n".join(lines[:50])
                lbl = ctk.CTkLabel(self.scrollable_frame, text=preview_text, anchor="nw", justify="left")
                lbl.pack(fill="both", expand=True)
            except Exception as e:
                lbl = ctk.CTkLabel(self.scrollable_frame, text=f"Error loading DOCX: {e}")
                lbl.pack()
        else:
            lbl = ctk.CTkLabel(self.scrollable_frame, text="Preview not available")
            lbl.pack()

    def go_back(self):
        self.master.show_upload_screen()
