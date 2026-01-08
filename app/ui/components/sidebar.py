import customtkinter as ctk

class SideBar(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master, width=70, corner_radius=0)
        self.callback = callback

        self.pack_propagate(False)

        ctk.CTkButton(self, text="📂", width=60, command=lambda: callback("upload")).pack(pady=10)
        ctk.CTkButton(self, text="📜", width=60, command=lambda: callback("history")).pack(pady=10)
        ctk.CTkButton(self, text="⚙", width=60, command=lambda: callback("settings")).pack(pady=10)
        ctk.CTkButton(self, text="🌗", width=60, command=lambda: callback("theme")).pack(pady=10)

        self.settings_panel = None

    def toggle_settings_panel(self):
        from app.ui.components.settings_panel import SettingsPanel
        if self.settings_panel and self.settings_panel.winfo_exists():
            self.settings_panel.destroy()
            self.settings_panel = None
        else:
            self.settings_panel = SettingsPanel(self.master)
            self.settings_panel.place(relx=1, rely=0, anchor="ne")
