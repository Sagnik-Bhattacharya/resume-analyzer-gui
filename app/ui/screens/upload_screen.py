import os
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
from app.utils.file_utils import is_valid_resume
from app.parsers.pdf import parse_pdf
from app.parsers.docx import parse_docx
from app.nlp.clean import clean_text
from app.nlp.skills import extract_skills
from app.core.matcher import compute_similarity
from app.core.scorer import score_resume
from app.services.resume_service import ResumeService

JOB_DESCRIPTION = """
Looking for a Python developer with experience in
Machine Learning, MongoDB, NLP, and Data Analysis.
"""

class UploadScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_file = None

        # ---------------- MAIN CONTAINER ----------------
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # ---------------- TITLE ----------------
        self.title = ctk.CTkLabel(
            container,
            text="Upload Your Resume",
            font=("Segoe UI", 28, "bold")
        )
        self.title.pack(pady=(0, 20))

        self.info = ctk.CTkLabel(
            container,
            text="Supported formats: PDF, DOCX",
            text_color="gray",
            font=("Segoe UI", 14)
        )
        self.info.pack(pady=(0, 30))

        # ---------------- UPLOAD BUTTON ----------------
        self.upload_btn = ctk.CTkButton(
            container,
            text="Choose Resume File",
            command=self.choose_file,
            width=250,
            height=50,
            fg_color="#0078D7",
            hover_color="#005EA3",
            font=("Segoe UI", 14, "bold")
        )
        self.upload_btn.pack(pady=10)
        
        self.history_btn = ctk.CTkButton(
            container,
            text="View Resume History",
            command=self.show_history  # ✅ this now points to a proper method
        )
        self.history_btn.pack(pady=10)

        # File info label
        self.file_label = ctk.CTkLabel(
            container,
            text="No file selected",
            text_color="gray",
            font=("Segoe UI", 12)
        )
        self.file_label.pack(pady=10)

        # ---------------- ANALYZE BUTTON ----------------
        self.analyze_btn = ctk.CTkButton(
            container,
            text="Analyze Resume",
            state="disabled",
            width=250,
            height=50,
            fg_color="#00B894",
            hover_color="#009966",
            font=("Segoe UI", 14, "bold"),
            command=self.analyze_resume
        )
        self.analyze_btn.pack(pady=30)

    # ---------------- CHOOSE FILE ----------------
    def show_history(self):
        self.master.show_history_screen()  # This is now a proper class method
        
    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Resume Files", "*.pdf *.docx")]
        )

        if file_path and is_valid_resume(file_path):
            self.selected_file = file_path
            self.file_label.configure(
                text=os.path.basename(file_path),
                text_color="white"
            )
            self.analyze_btn.configure(state="normal")
        else:
            self.file_label.configure(
                text="Invalid file format",
                text_color="red"
            )

    # ---------------- ANALYZE RESUME ----------------
    def analyze_resume(self):
        if not self.selected_file:
            return

        _, ext = os.path.splitext(self.selected_file.lower())

        if ext == ".pdf":
            text = parse_pdf(self.selected_file)
        elif ext == ".docx":
            text = parse_docx(self.selected_file)
        else:
            return

        cleaned_text = clean_text(text)
        skills = extract_skills(cleaned_text)

        job_cleaned = clean_text(JOB_DESCRIPTION)
        job_skills = extract_skills(job_cleaned)

        similarity = compute_similarity(cleaned_text, job_cleaned)
        score_data = score_resume(skills, job_skills)

        print("\n===== ANALYSIS RESULT =====")
        print("Match Score:", score_data["score"], "%")
        print("Similarity Score:", similarity, "%")
        print("Matched Skills:", score_data["matched_skills"])
        print("Missing Skills:", score_data["missing_skills"])
        print("===========================\n")

        # Build analysis dictionary
        analysis_data = {
            "filename": Path(self.selected_file).name,
            "filepath": Path(self.selected_file),
            "skills": skills,
            "matched_skills": score_data["matched_skills"],
            "missing_skills": score_data["missing_skills"],
            "match_score": score_data["score"],
            "similarity_score": similarity
        }

        # Save to DB
        service = ResumeService()
        service.save_analysis(
            filename=analysis_data["filename"],
            skills=skills,
            score_data=score_data,
            similarity=similarity,
            filepath=analysis_data["filepath"]
        )

        # Switch screen to results
        self.master.show_result_screen(analysis_data)
