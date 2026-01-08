import customtkinter as ctk
from tkinter import Canvas
from pathlib import Path
from PIL import Image, ImageTk
from pdf2image import convert_from_path

class ResultScreen(ctk.CTkFrame):
    def __init__(self, master, analysis_data):
        super().__init__(master)
        self.master = master
        self.analysis_data = analysis_data

        # PDF state
        self.pdf_pages = []
        self.tk_image = None  # holds ONE image for single-page view
        self.zoom_factor = 1.0
        self.current_page = 0

        # ---------------- MAIN FRAME ----------------
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- LEFT FRAME: PDF ----------------
        self.left_frame = ctk.CTkFrame(main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(self.left_frame, text="Resume Preview",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 10))

        # Canvas container (single-page view)
        self.canvas_frame = ctk.CTkFrame(self.left_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, bg="#1C1C1C")
        self.canvas.pack(fill="both", expand=True)

        # Page indicator
        self.page_label = ctk.CTkLabel(self.left_frame, text="")
        self.page_label.pack(pady=(5, 0))

        # Navigation + Zoom controls
        nav_frame = ctk.CTkFrame(self.left_frame)
        nav_frame.pack(pady=5)

        self.prev_btn = ctk.CTkButton(nav_frame, text="<< Prev", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = ctk.CTkButton(nav_frame, text="Next >>", command=self.next_page)
        self.next_btn.pack(side="left", padx=5)

        self.zoom_in_btn = ctk.CTkButton(nav_frame, text="Zoom +", command=lambda: self.perform_zoom(1.25))
        self.zoom_in_btn.pack(side="left", padx=5)

        self.zoom_out_btn = ctk.CTkButton(nav_frame, text="Zoom -", command=lambda: self.perform_zoom(0.8))
        self.zoom_out_btn.pack(side="left", padx=5)

        # Load PDF after UI setup
        self.load_pdf(analysis_data.get("filepath"))

        # ---------------- RIGHT FRAME: Analysis ----------------
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(right_frame, text="Analysis Results",
                     font=("Segoe UI", 20, "bold")).pack(pady=(0, 20))

        ctk.CTkLabel(right_frame, text=f"Match Score: {analysis_data['match_score']}%",
                     text_color="#00FF00").pack(anchor="w", padx=10)
        ctk.CTkLabel(right_frame, text=f"Similarity Score: {analysis_data['similarity_score']}%",
                     text_color="#00FFFF").pack(anchor="w", padx=10)

        self.create_skill_frame(right_frame, "Matched Skills", analysis_data['matched_skills'], "#00FF00")
        self.create_skill_frame(right_frame, "Missing Skills", analysis_data['missing_skills'], "#FF5555")

        self.back_btn = ctk.CTkButton(right_frame, text="Analyze Another Resume", command=self.go_back)
        self.back_btn.pack(pady=(20, 0))


    # ---------------- LOAD PDF ----------------
    def load_pdf(self, filepath):
        if not filepath:
            return

        filepath = Path(filepath) if isinstance(filepath, str) else filepath
        if not filepath.exists():
            print("PDF not found:", filepath)
            return

        try:
            self.pdf_pages = convert_from_path(filepath, dpi=150)
            self.show_page(0)
        except Exception as e:
            print("PDF Load Error:", e)

    # ---------------- SHOW SINGLE PAGE ----------------
    def show_page(self, index):
        if not (0 <= index < len(self.pdf_pages)):
            return

        self.current_page = index
        page = self.pdf_pages[index].copy()

        w, h = page.size
        scaled = page.resize((int(w * self.zoom_factor), int(h * self.zoom_factor)))

        self.tk_image = ImageTk.PhotoImage(scaled)  # keep alive
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.canvas.config(scrollregion=(0, 0, scaled.width, scaled.height))
        self.page_label.configure(text=f"Page {index + 1} of {len(self.pdf_pages)}")

    # ---------------- ZOOM ----------------
    def perform_zoom(self, factor):
        self.zoom_factor *= factor
        self.show_page(self.current_page)

    # ---------------- NAVIGATION ----------------
    def next_page(self):
        if self.current_page + 1 < len(self.pdf_pages):
            self.show_page(self.current_page + 1)

    def prev_page(self):
        if self.current_page - 1 >= 0:
            self.show_page(self.current_page - 1)

    # ---------------- SKILL FRAME ----------------
    def create_skill_frame(self, parent, title, skills, color):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        wrap = ctk.CTkFrame(frame)
        wrap.pack(anchor="w", padx=10, pady=5)
        for skill in skills:
            pill = ctk.CTkLabel(wrap, text=skill, fg_color=color, corner_radius=12, padx=10, pady=5)
            pill.pack(side="left", padx=5, pady=5)

    # ---------------- BACK ----------------
    def go_back(self):
        self.master.show_upload_screen()
