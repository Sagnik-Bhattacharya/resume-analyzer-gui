import customtkinter as ctk
from app.services.resume_service import ResumeService

class HistoryScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.service = ResumeService()

        # Title
        self.title = ctk.CTkLabel(
            self,
            text="Resume History",
            font=("Segoe UI", 24, "bold")
        )
        self.title.pack(pady=20)

        # List of resumes
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_history()

        # Back button
        self.back_btn = ctk.CTkButton(
            self,
            text="Back",
            command=self.master.show_upload_screen
        )
        self.back_btn.pack(pady=10)

    def load_history(self):
        resumes = self.service.get_all_resumes()

        for resume in resumes:
            btn = ctk.CTkButton(
                self.list_frame,
                text=resume['filename'],
                command=lambda r=resume: self.view_resume(r)
            )
            btn.pack(pady=5, fill="x")

    def view_resume(self, resume_data):
        self.master.show_result_screen(resume_data)
