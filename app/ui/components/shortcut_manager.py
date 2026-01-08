from app.utils.settings import load_settings, save_settings

class ShortcutManager:
    def __init__(self, app):
        app.bind("<Control-t>", lambda e: app.toggle_theme())
        app.bind("<Control-o>", lambda e: app.show_upload_screen())
        app.bind("<Control-h>", lambda e: app.show_history_screen())
        app.bind("<Control-r>", lambda e: self.toggle_resume_view(app))
        app.bind("<Control-m>", lambda e: self.toggle_pdf_mode(app))

    def toggle_resume_view(self, app):
        v = app.settings["resume_view"]
        app.settings["resume_view"] = "parsed" if v == "raw" else "raw"
        save_settings(app.settings)
        app.show_result_screen(app.current_screen.analysis_data)

    def toggle_pdf_mode(self, app):
        m = app.settings["pdf_mode"]
        app.settings["pdf_mode"] = "scroll" if m == "page" else "page"
        save_settings(app.settings)
        app.show_result_screen(app.current_screen.analysis_data)
