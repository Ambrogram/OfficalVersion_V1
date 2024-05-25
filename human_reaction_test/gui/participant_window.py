import tkinter as tk
from tkinter import Toplevel, ttk, messagebox  # Import Toplevel and messagebox from tkinter
from tests.test_runner import TestRunner

class ParticipantWindow:
    def __init__(self, root, app):
        self.root = Toplevel(root)  # Use Toplevel from tkinter
        self.root.title("Participant Window")
        self.root.geometry("500x360")
        self.app = app  # Store the app reference

        self.root.configure(bg='#2d2d2d')
        
        start_button = ttk.Button(self.root, text="Start Test", command=self.start_test)
        start_button.pack(pady=20)

    def start_test(self):
        # Retrieve the selected settings from the shared attribute
        selected_settings = self.app.settings
        if selected_settings is None:
            messagebox.showerror("Error", "No settings selected. Please set the settings in the Researcher window.")
            return
        TestRunner(self.root, selected_settings, self.app) # Pass the app reference to the TestRunner
