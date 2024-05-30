import customtkinter as ctk
from tkinter import messagebox, Listbox  # Import Listbox from tkinter
from database.db_operations import insert_participant, get_participant_by_name, get_all_participants
from settings.settings_manager import SettingsManager
# from analysis.data_analysis import analyze_results  # Assuming this module exists

class ResearcherWindow:
    def __init__(self, root, app):
        self.root = ctk.CTkToplevel(root)
        self.root.title("Researcher Dashboard")
        self.root.geometry("1024x576")
        self.app = app

        self.root.configure(bg='#2d2d2d')
        
        self.settings_manager = None  # Initialize settings_manager here

        # Title
        title_label = ctk.CTkLabel(self.root, text="Researcher Dashboard", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Dashboard buttons
        self.create_dashboard_buttons()

    def create_dashboard_buttons(self):
        view_participants_button = ctk.CTkButton(self.root, text="View Participants", command=self.view_participants)
        view_participants_button.grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        manage_tests_button = ctk.CTkButton(self.root, text="Manage Tests", command=self.manage_tests)
        manage_tests_button.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        view_results_button = ctk.CTkButton(self.root, text="View Results", command=self.view_results)
        view_results_button.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

    def view_participants(self):
        self.clear_window()
        title_label = ctk.CTkLabel(self.root, text="Participant Information", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.create_search_field()
        self.create_form()

        # Display all participants
        participants = get_all_participants()
        if participants:
            self.display_participants(participants)

    def manage_tests(self):
        self.clear_window()
        title_label = ctk.CTkLabel(self.root, text="Manage Tests", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Include settings functionality here
        settings_button = ctk.CTkButton(self.root, text="Open Settings", command=self.open_settings)
        settings_button.grid(row=1, column=0, pady=20, padx=20, sticky="ew")

    def view_results(self):
        self.clear_window()
        title_label = ctk.CTkLabel(self.root, text="Test Results", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Retrieve and display test results
        results = analyze_results()  # Assuming this function exists and returns test results
        results_text = ctk.CTkTextbox(self.root)
        results_text.insert("end", results)
        results_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_search_field(self):
        ctk.CTkLabel(self.root, text="Search Participant Name:").grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.search_entry = ctk.CTkEntry(self.root)
        self.search_entry.grid(row=1, column=1, pady=10, padx=20, sticky="ew")

        search_button = ctk.CTkButton(self.root, text="Search", command=self.search_participant)
        search_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

    def create_form(self):
        ctk.CTkLabel(self.root, text="First Name:").grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.first_name_entry = ctk.CTkEntry(self.root)
        self.first_name_entry.grid(row=2, column=1, pady=10, padx=20, sticky="ew")

        ctk.CTkLabel(self.root, text="Last Name:").grid(row=3, column=0, pady=10, padx=20, sticky="w")
        self.last_name_entry = ctk.CTkEntry(self.root)
        self.last_name_entry.grid(row=3, column=1, pady=10, padx=20, sticky="ew")

        # Age
        ctk.CTkLabel(self.root, text="Age:").grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.age_entry = ctk.CTkEntry(self.root)
        self.age_entry.grid(row=4, column=1, pady=10, padx=20, sticky="ew")

        # Gender
        ctk.CTkLabel(self.root, text="Gender:").grid(row=5, column=0, pady=10, padx=20, sticky="w")
        self.gender_var = ctk.StringVar()
        self.gender_combobox = ctk.CTkComboBox(self.root, variable=self.gender_var, values=["Male", "Female", "Other"])
        self.gender_combobox.grid(row=5, column=1, pady=10, padx=20, sticky="ew")

        # Education
        self.education_var = ctk.StringVar()
        self.education_combobox = ctk.CTkComboBox(self.root, variable=self.education_var, 
                                        values=["-- select one --", "No formal education", "Primary education", 
                                                "Secondary education or high school", "GED", "Vocational qualification", 
                                                "Bachelor's degree", "Master's degree", "Doctorate or higher"])
        self.education_combobox.set("-- select one --")  # Default value
        ctk.CTkLabel(self.root, text="Education:").grid(row=6, column=0, pady=10, padx=20, sticky="w")
        self.education_combobox.grid(row=6, column=1, pady=10, padx=20, sticky="ew")

        # Occupation
        occupation_options = ["Pilots", "Race Car Drivers", "Video Game Testers", "Professional Gamers",
                            "Paramedics", "Firefighters", "Police Officers", "Military Personnel",
                            "Sprinters", "Soccer Players", "none of the above"]

        self.occupation_var = ctk.StringVar()
        self.occupation_combobox = ctk.CTkComboBox(self.root, variable=self.occupation_var, values=occupation_options)
        self.occupation_combobox.set("none of the above")  # Default value
        ctk.CTkLabel(self.root, text="Occupation:").grid(row=7, column=0, pady=10, padx=20, sticky="w")
        self.occupation_combobox.grid(row=7, column=1, pady=10, padx=20, sticky="ew")

        # Color Blind
        ctk.CTkLabel(self.root, text="Color Blind:").grid(row=8, column=0, pady=10, padx=20, sticky="w")
        self.color_blind_var = ctk.StringVar()
        self.color_blind_combobox = ctk.CTkComboBox(self.root, variable=self.color_blind_var, values=["Yes", "No"])
        self.color_blind_combobox.grid(row=8, column=1, pady=10, padx=20, sticky="ew")

        # Medical History
        medical_history_options = ["Neurological Disorders", "Mental Health Issues", "Substance Abuse Disorders",
                                "Sleep Disorders", "Chronic Fatigue Syndrome", "none of the above"]

        self.medical_history_var = ctk.StringVar()
        self.medical_history_combobox = ctk.CTkComboBox(self.root, variable=self.medical_history_var, values=medical_history_options)
        self.medical_history_combobox.set("none of the above")  # Default value
        ctk.CTkLabel(self.root, text="Medical History:").grid(row=9, column=0, pady=10, padx=20, sticky="w")
        self.medical_history_combobox.grid(row=9, column=1, pady=10, padx=20, sticky="ew")

        # Save button
        save_button = ctk.CTkButton(self.root, text="Save Participant", command=self.save_participant)
        save_button.grid(row=10, column=0, columnspan=2, pady=20)

    def save_participant(self):
        participant_info = {
            'FirstName': self.first_name_entry.get(),
            'LastName': self.last_name_entry.get(),
            'Age': self.age_entry.get(),
            'Gender': self.gender_var.get(),
            'Education': self.education_combobox.get(),
            'Occupation': self.occupation_combobox.get(),
            'ColorBlind': self.color_blind_var.get(),
            'MedicalHistory': self.medical_history_combobox.get()
        }

        # Save participant info to the database
        participant_id = insert_participant(participant_info)
        if participant_id:
            self.app.participant_id = participant_id  # Save the participant_id in the app context
            messagebox.showinfo("Success", "Participant saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to save participant.")

    def search_participant(self):
        participant_name = self.search_entry.get()
        participants = get_participant_by_name(participant_name)
        if participants:
            if len(participants) == 1:
                self.populate_form(participants[0])
            else:
                self.select_participant_window(participants)
        else:
            messagebox.showerror("Error", "Participant not found.")

    def select_participant_window(self, participants):
        select_window = ctk.CTkToplevel(self.root)
        select_window.title("Select Participant")
        select_window.geometry("400x300")

        ctk.CTkLabel(select_window, text="Select Participant", font=("Helvetica", 16, "bold")).pack(pady=10)

        listbox = Listbox(select_window)
        for participant in participants:
            listbox.insert("end", f"{participant['ParticipantID']}: {participant['FirstName']} {participant['LastName']}")
        listbox.pack(pady=10, padx=10, fill="both", expand=True)

        def on_select(event):
            selected = listbox.get(listbox.curselection())
            participant_id = selected.split(":")[0]
            participant = next(p for p in participants if str(p['ParticipantID']) == participant_id)
            self.populate_form(participant)
            select_window.destroy()

        listbox.bind("<<ListboxSelect>>", on_select)

    def populate_form(self, participant):
        self.first_name_entry.delete(0, "end")
        self.first_name_entry.insert(0, participant['FirstName'])

        self.last_name_entry.delete(0, "end")
        self.last_name_entry.insert(0, participant['LastName'])

        self.age_entry.delete(0, "end")
        self.age_entry.insert(0, participant['Age'])

        self.gender_var.set(participant['Gender'])
        self.education_var.set(participant['Education'])
        self.occupation_var.set(participant['Occupation'])
        self.color_blind_var.set(participant['ColorBlind'])
        self.medical_history_var.set(participant['MedicalHistory'])

    def open_settings(self):
        if self.settings_manager is None or not self.settings_manager.root.winfo_exists():
            self.settings_manager = SettingsManager(self.root, self)
        else:
            self.settings_manager.root.lift()

    def set_settings(self, settings):
        self.app.settings = settings  # Store selected settings in the shared attribute

    def display_participants(self, participants):
        participants_listbox = Listbox(self.root)
        for participant in participants:
            participants_listbox.insert("end", f"{participant['ParticipantID']}: {participant['FirstName']} {participant['LastName']}")
        participants_listbox.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
