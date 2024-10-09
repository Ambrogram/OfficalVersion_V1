import customtkinter as ctk
from PIL import Image, ImageTk
from gui.researcher_window import ResearcherWindow
from gui.participant_window import ParticipantWindow

class App:
    def __init__(self, root):
        self.root = root
        self.settings = None  # Shared attribute to store settings
        self.participant_id = None  # Attribute to store the participant ID
        self.first_name = None  # Attribute to store the participant's first name
        self.last_name = None  # Attribute to store the participant's last name
        
        # Set window background color
        self.root.configure(bg='#2d2d2d')
        
        # Welcome message
        welcome_label = ctk.CTkLabel(root, text="WELCOME", font=("Helvetica", 24, "bold"))
        welcome_label.pack(pady=(100, 20))

        # Researcher button
        researcher_button = ctk.CTkButton(root, text="Researcher", command=self.open_researcher_window)
        researcher_button.pack(ipadx=10, ipady=5, pady=10)

        # Participant button
        participant_button = ctk.CTkButton(root, text="Participants", command=self.open_participant_window)
        participant_button.pack(ipadx=10, ipady=5, pady=10)

    def open_researcher_window(self):
        researcher_window = ResearcherWindow(self.root, self)

    def open_participant_window(self):
        participant_window = ParticipantWindow(self.root, self)

def main():
    ctk.set_appearance_mode("dark")
    # Update the path to the theme file
    theme_path = "./OfficalVersion_V1/human_reaction_test/NightTrain.json"
    ctk.set_default_color_theme(theme_path)
    root = ctk.CTk()
    root.title("Welcome to the Reaction Time Test")
    root.geometry("1024x576")  # 16:9 aspect ratio

    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
