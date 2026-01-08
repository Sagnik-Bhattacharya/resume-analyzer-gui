import customtkinter as ctk
import json, os

from app.ui.screens.upload_screen import UploadScreen
from app.ui.screens.result_screen import ResultScreen
from app.ui.screens.history_screen import HistoryScreen
from app.ui.components.sidebar import SideBar
from app.ui.components.shortcut_manager import ShortcutManager
from app.utils.settings import load_settings, save_settings
class ResumeAnalyzerApp(ctk.CTk):
    def __init__(self):
        self.settings = load_settings()
        # Ensure default keys exist to prevent KeyError
        if "window" not in self.settings:
            self.settings["window"] = {"width": 1100, "height": 700}
        if "theme" not in self.settings:
            self.settings["theme"] = "dark"
        ctk.set_appearance_mode(self.settings["theme"])
        super().__init__()

        # ---- Window state persistence ----
        w = self.settings["window"].get("width", 1100)
        h = self.settings["window"].get("height", 700)
        self.geometry(f"{w}x{h}")
        self.minsize(900, 600)
        self.title("Resume Analyzer")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # ---- Persistent layout ----
        self.sidebar = SideBar(self, self.on_sidebar_action)
        self.sidebar.pack(side="left", fill="y")

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.current_screen = None
        self.show_upload_screen()

        # ---- Shortcut manager ----
        ShortcutManager(self)

    # ---- Sidebar Actions ----
    def on_sidebar_action(self, action):
        if action == "upload":
            self.show_upload_screen()
        elif action == "history":
            self.show_history_screen()
        elif action == "settings":
            self.sidebar.toggle_settings_panel()
        elif action == "theme":
            self.toggle_theme()

    # ---- Theme Toggle ----
    def toggle_theme(self):
        new_theme = "light" if self.settings["theme"] == "dark" else "dark"
        self.settings["theme"] = new_theme
        ctk.set_appearance_mode(new_theme)
        save_settings(self.settings)

    # ---- Screens ----
    def show_upload_screen(self):
        self._swap_screen(UploadScreen(self))

    def show_result_screen(self, analysis_data):
        self._swap_screen(ResultScreen(self, analysis_data))

    def show_history_screen(self):
        self._swap_screen(HistoryScreen(self))

    def _swap_screen(self, screen):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen
        self.current_screen.pack(in_=self.container, fill="both", expand=True)

    # ---- Window close ----
    def on_close(self):
        w, h = self.winfo_width(), self.winfo_height()
        self.settings["window"] = {"width": w, "height": h}
        save_settings(self.settings)
        self.destroy()
