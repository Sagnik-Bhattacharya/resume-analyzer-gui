import customtkinter as ctk
from app.ui.theme import set_theme
from app.ui.screens.upload_screen import UploadScreen
from app.ui.screens.upload_screen import UploadScreen
from app.ui.screens.result_screen import ResultScreen

class ResumeAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        set_theme()
        self.title("Resume Analyzer")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.current_screen = None
        self.show_upload_screen()

    def show_upload_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = UploadScreen(self)
        self.current_screen.pack(fill="both", expand=True)

    def show_result_screen(self, analysis_data):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = ResultScreen(self, analysis_data)
        self.current_screen.pack(fill="both", expand=True)