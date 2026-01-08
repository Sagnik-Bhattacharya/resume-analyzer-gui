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
        self.tk_images = []
        self.zoom_factor = 1.0

        # ---------------- MAIN FRAME ----------------
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- LEFT FRAME: Scrollable PDF ----------------
        self.left_frame = ctk.CTkFrame(main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

        ctk.CTkLabel(self.left_frame, text="Resume Preview", font=("Segoe UI", 18, "bold")).pack(pady=(0,10))

        # Scrollable canvas
        self.canvas_frame = ctk.CTkFrame(self.left_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, bg="#1C1C1C")
        self.scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame for images
        self.image_container = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0,0), window=self.image_container, anchor="nw")
        self.image_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Zoom buttons
        nav_frame = ctk.CTkFrame(self.left_frame)
        nav_frame.pack(pady=5)
        ctk.CTkButton(nav_frame, text="Zoom +", command=lambda: self.zoom(1.25)).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Zoom -", command=lambda: self.zoom(0.8)).pack(side="left", padx=5)
        # Load PDF
        self.load_pdf(analysis_data.get("filepath"))

        # ---------------- RIGHT FRAME: Analysis ----------------
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10,0))

        # Match / similarity scores
        ctk.CTkLabel(right_frame, text="Analysis Results", font=("Segoe UI", 20, "bold")).pack(pady=(0,20))
        ctk.CTkLabel(right_frame, text=f"Match Score: {analysis_data['match_score']}%", text_color="#00FF00").pack(anchor="w", padx=10)
        ctk.CTkLabel(right_frame, text=f"Similarity Score: {analysis_data['similarity_score']}%", text_color="#00FFFF").pack(anchor="w", padx=10)

        # Skill pills
        self.create_skill_frame(right_frame, "Matched Skills", analysis_data['matched_skills'], "#00FF00")
        self.create_skill_frame(right_frame, "Missing Skills", analysis_data['missing_skills'], "#FF5555")

        # Back button
        self.back_btn = ctk.CTkButton(right_frame, text="Analyze Another Resume", command=self.go_back)
        self.back_btn.pack(pady=(20,0))
        self.focused_page_label = ctk.CTkLabel(self.left_frame, text="")
        self.focused_page_label.pack(pady=(5,0))

        self.single_page_mode = True  # Toggle variable
        self.show_page(0)  # Start at first page

        # ---------------- NAVIGATION ----------------
        nav_frame = ctk.CTkFrame(self.left_frame)
        nav_frame.pack(pady=5)
        self.prev_btn = ctk.CTkButton(nav_frame, text="<< Prev", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn = ctk.CTkButton(nav_frame, text="Next >>", command=self.next_page)
        self.next_btn.pack(side="left", padx=5)
        self.zoom_in_btn = ctk.CTkButton(nav_frame, text="Zoom +", command=lambda: self.zoom(1.25))
        self.zoom_in_btn.pack(side="left", padx=5)
        self.zoom_out_btn = ctk.CTkButton(nav_frame, text="Zoom -", command=lambda: self.zoom(0.8))
        self.zoom_out_btn.pack(side="left", padx=5)

    # ---------------- LOAD PDF ----------------
    def load_pdf(self, filepath):
        if not filepath:
            return
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.exists():
            print(f"File not found: {filepath}")
            return
        try:
            self.pdf_pages = convert_from_path(filepath, dpi=150)
            self.display_pages()
        except Exception as e:
            print(f"Error loading PDF: {e}")

    # ---------------- DISPLAY ALL PAGES ----------------
    def display_pages(self):
        for widget in self.image_container.winfo_children():
            widget.destroy()
        self.tk_images.clear()

        for page in self.pdf_pages:
            w,h = page.size
            img = page.resize((int(w*self.zoom_factor), int(h*self.zoom_factor)))
            tk_img = ImageTk.PhotoImage(img)
            self.tk_images.append(tk_img)  # keep reference
            lbl = ctk.CTkLabel(self.image_container, image=tk_img)
            lbl.pack(pady=5)

    # ---------------- ZOOM ----------------
    def zoom(self, factor):
        self.zoom_factor *= factor
        self.display_pages()

    # ---------------- SKILL FRAME ----------------
    def create_skill_frame(self, parent, title, skills, color):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(frame, text=title, font=("Segoe UI",14,"bold")).pack(anchor="w", padx=10, pady=5)
        skills_container = ctk.CTkFrame(frame)
        skills_container.pack(anchor="w", padx=10, pady=5)
        for skill in skills:
            pill = ctk.CTkLabel(skills_container, text=skill, fg_color=color, corner_radius=12, padx=10, pady=5)
            pill.pack(side="left", padx=5, pady=5)

    # ---------------- BACK ----------------
    def go_back(self):
        self.master.show_upload_screen()
    
    # Show single page with indicator
    def show_page(self, index):
        if 0 <= index < len(self.pdf_pages):
            self.current_page = index
            for widget in self.image_container.winfo_children():
                widget.destroy()

            pil_img = self.pdf_pages[index].copy()
            w,h = pil_img.size
            pil_img = pil_img.resize((int(w*self.zoom_factor), int(h*self.zoom_factor)))

            tk_img = ImageTk.PhotoImage(pil_img)
            label = ctk.CTkLabel(self.image_container, image=tk_img)
            label.image = tk_img
            label.pack()
            self.focused_page_label.configure(text=f"Page {index+1} of {len(self.pdf_pages)}")

    def next_page(self):
        if self.current_page + 1 < len(self.pdf_pages):
            self.show_page(self.current_page + 1)

    def prev_page(self):
        if self.current_page - 1 >= 0:
            self.show_page(self.current_page - 1)

    def zoom(self, factor):
        self.zoom_factor *= factor
        self.show_page(self.current_page)

