import customtkinter as ctk
from tkinter import scrolledtext, Canvas, Frame
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class ResultScreen(ctk.CTkFrame):
    def __init__(self, master, analysis_data):
        super().__init__(master)

        self.analysis_data = analysis_data
        self.pdf_images = []  # Store PhotoImage objects
        self.current_page = 0

        # ---------------- MAIN SPLIT ----------------
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- LEFT PANEL: PDF Preview ----------------
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            left_frame,
            text="Resume Preview",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 10))

        # Canvas + Scrollbar for multi-page PDF
        self.canvas_frame = Frame(left_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, bg="#1E1E1E")
        self.scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.image_container = Frame(self.canvas, bg="#1E1E1E")
        self.canvas.create_window((0, 0), window=self.image_container, anchor="nw")
        self.image_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # ---------------- RIGHT PANEL: Analysis ----------------
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(
            right_frame,
            text="Analysis Results",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(0, 20))

        # Scores card
        scores_frame = ctk.CTkFrame(right_frame)
        scores_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(scores_frame, text=f"Match Score: {analysis_data['match_score']}%", font=("Segoe UI", 16, "bold"), text_color="#00FF00").pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(scores_frame, text=f"Similarity Score: {analysis_data['similarity_score']}%", font=("Segoe UI", 16), text_color="#00FFFF").pack(anchor="w", padx=10, pady=5)

        # Skills as pill-shaped tags
        def create_skill_frame(skills, color):
            frame = ctk.CTkFrame(right_frame)
            frame.pack(fill="x", pady=(0, 10))
            for skill in skills:
                pill = ctk.CTkLabel(frame, text=skill, corner_radius=15, fg_color=color, padx=10, pady=5, font=("Segoe UI", 12))
                pill.pack(side="left", padx=5, pady=5)
            return frame

        create_skill_frame(analysis_data['matched_skills'], "#00FF00")
        create_skill_frame(analysis_data['missing_skills'], "#FF5555")

        # Back button
        self.back_btn = ctk.CTkButton(right_frame, text="Analyze Another Resume", command=self.go_back)
        self.back_btn.pack(pady=(20, 0))

        # Load PDF preview
        self.load_preview(analysis_data.get("filepath"))

    def load_preview(self, filepath):
        if not filepath:
            return

        filepath = Path(filepath)  # Convert string to Path

        if not filepath.exists():
            ctk.CTkLabel(self.image_container, text=f"File not found: {filepath}", font=("Segoe UI", 12), text_color="red").pack()
            return

        # Multi-page PDF
        if filepath.suffix.lower() == ".pdf":
            try:
                pages = convert_from_path(filepath, dpi=150)
                self.pdf_images.clear()
                for page in pages:
                    page.thumbnail((600, 800))
                    img = ImageTk.PhotoImage(page)
                    self.pdf_images.append(img)
                    ctk.CTkLabel(self.image_container, image=img).pack(pady=5)
            except Exception as e:
                ctk.CTkLabel(self.image_container, text=f"Error loading PDF: {e}", font=("Segoe UI", 12), text_color="red").pack()

        # DOCX preview (first 20 lines)
        elif filepath.suffix.lower() == ".docx":
            from docx import Document
            try:
                doc = Document(filepath)
                text_preview = "\n".join([p.text for p in doc.paragraphs if p.text][:20])
                scrolled = scrolledtext.ScrolledText(self.image_container, wrap="word", font=("Segoe UI", 12), width=50, height=30, bg="#2B2B2B", fg="white", insertbackground="white")
                scrolled.insert("1.0", text_preview)
                scrolled.pack(fill="both", expand=True)
            except Exception as e:
                ctk.CTkLabel(self.image_container, text=f"Error loading DOCX: {e}", font=("Segoe UI", 12), text_color="red").pack()

    def go_back(self):
        self.master.show_upload_screen()
