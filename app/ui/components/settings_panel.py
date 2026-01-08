import customtkinter as ctk
from app.utils.settings import load_settings, save_settings

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=250, height=300, corner_radius=8)
        self.configure(fg_color="#2B2B2B")
        self.pack_propagate(False)

        app = master

        ctk.CTkLabel(self, text="Settings", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Resume View (Raw / Parsed)
        ctk.CTkLabel(self, text="Resume View").pack(anchor="w", padx=10)
        resume_view = ctk.CTkSegmentedButton(self, values=["raw", "parsed"], command=lambda v: self.set_resume_view(app, v))
        resume_view.set(app.settings["resume_view"])
        resume_view.pack(pady=5, padx=10, fill="x")

        # PDF Mode (Scroll / Page)
        ctk.CTkLabel(self, text="PDF Mode").pack(anchor="w", padx=10)
        pdf_mode = ctk.CTkSegmentedButton(self, values=["scroll", "page"], command=lambda v: self.set_pdf_mode(app, v))
        pdf_mode.set(app.settings["pdf_mode"])
        pdf_mode.pack(pady=5, padx=10, fill="x")

    def set_resume_view(self, app, mode):
        app.settings["resume_view"] = mode
        save_settings(app.settings)

        # Only refresh if already on result screen
        if hasattr(app.current_screen, "analysis_data"):
            app.show_result_screen(app.current_screen.analysis_data)


    def set_pdf_mode(self, app, mode):
        app.settings["pdf_mode"] = mode
        save_settings(app.settings)

        # Only refresh if already on result screen
        if hasattr(app.current_screen, "analysis_data"):
            app.show_result_screen(app.current_screen.analysis_data)
