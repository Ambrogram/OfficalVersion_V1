import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import datetime
from database.db_operations import insert_test_record

class TestRunner:
    def __init__(self, parent, settings, app):
        self.settings = settings
        self.app = app  # Store the app reference
        
        self.root = tk.Toplevel(parent)
        self.root.title("Reaction Time Test")
        
        self.event_counter = 0
        self.correct_answers = 0
        self.current_color = ''
        self.current_display_color = ''
        self.test_start_time = time.time()
        self.response_recorded = False  # Track if the response for the current event has been recorded
        
        self.colors = self.settings['colors']
        self.color_values = {
            'Red': '#FF0000',
            'Green': '#008000',
            'Blue': '#0000FF',
            'Yellow': '#FFFF00',
            'White': '#FFFFFF',
            'Orange': '#FFA500',
            'Cyan': '#00FFFF'
        }
        self.key_to_color = {
            'r': 'Red',
            'g': 'Green',
            'b': 'Blue',
            'y': 'Yellow',
            'w': 'White',
            'o': 'Orange',
            'c': 'Cyan'
        }
        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()

        # Create a style object
        self.style = ttk.Style()
        self.style.configure("TLabel", background="black", foreground="white", font=('Helvetica', 16))

        # Apply the style to the label
        self.feedback_label = ttk.Label(self.root, text="", style="TLabel")
        self.feedback_label.pack(pady=10)
        
        self.root.bind("<KeyPress>", self.record_response)
        self.show_stimulus()
        self.root.mainloop()

    def show_stimulus(self):
        print(f"Event {self.event_counter+1}/{self.settings['events']}")  # Debug print
        self.response_recorded = False  # Reset response recorded flag
        self.level = random.choice(['A', 'B', 'C'])
        self.current_color = random.choice(self.colors)
        if self.level == "C":
            mismatch_colors = [c for c in self.colors if c != self.current_color]
            self.current_display_color = random.choice(mismatch_colors)
        else:
            self.current_display_color = self.current_color

        self.canvas.delete("all")
        text = self.current_color.upper()
        fill = self.color_values[self.current_display_color]
        if self.level == 'A':
            x0, y0 = random.randint(50, 550), random.randint(50, 350)
            self.canvas.create_oval(x0, y0, x0 + 100, y0 + 100, fill=fill, outline="")
        else:
            self.canvas.create_text(300, 200, text=text, fill=fill, font=('Helvetica', 32))

        self.event_counter += 1
        if self.event_counter < self.settings['events']:  # Schedule next stimulus only if more events are left
            interval = random.uniform(*self.settings['frequency']) * 1000
            self.root.after(int(interval), self.show_stimulus)
        else:
            print("Last event shown, finishing test.")  # Debug print
            self.root.after(0, self.finish_test)  # Ensure the test finishes after the last stimulus is shown

    def record_response(self, event):
        if not self.response_recorded:  # Check if response for the current event has been recorded
            self.response_recorded = True  # Mark the response as recorded
            selected_color = self.key_to_color.get(event.keysym.lower())
            correct = (selected_color == self.current_color if self.level != 'C' else selected_color == self.current_display_color)
            if correct:
                self.correct_answers += 1

            self.feedback_label.config(text=f"{'Correct' if correct else 'Incorrect'}. Total correct: {self.correct_answers}/{self.event_counter}")
            print(f"Response recorded. Total correct: {self.correct_answers}/{self.event_counter}")  # Debug print

    def finish_test(self):
        print("Finishing test...")  # Debug print
        total_test_time = time.time() - self.test_start_time
        correct_rate = (self.correct_answers / self.event_counter) * 100
        self.feedback_label.config(text=f"Test complete. Correct Rate: {correct_rate:.2f}%, Total Time Cost: {total_test_time:.2f} seconds")
        self.root.unbind("<KeyPress>")

        # Show options to save to database or retake test
        self.show_finish_options(total_test_time, correct_rate)

    def show_finish_options(self, total_test_time, correct_rate):
        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=20)

        save_button = ttk.Button(options_frame, text="Save to Database", command=lambda: self.save_test_results(total_test_time, correct_rate))
        save_button.pack(side=tk.LEFT, padx=10)

        retake_button = ttk.Button(options_frame, text="Retake Test", command=self.retake_test)
        retake_button.pack(side=tk.LEFT, padx=10)

    def save_test_results(self, total_test_time, correct_rate):
        test_info = {
            'ParticipantID': self.app.participant_id,
            'SettingID': self.settings['settingID'],
            'TestDate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'CorrectAnswers': self.correct_answers,
            'CorrectRate': correct_rate,
            'TotalTimeCost': total_test_time
        }
        insert_test_record(test_info)
        # Show detailed test result in a messagebox
        participant_name = f"{self.app.first_name} {self.app.last_name}"  # Assuming these are stored in app
        result_message = f"Test results saved successfully.\n\n" \
                         f"Participant ID: {self.app.participant_id}\n" \
                         f"Participant Name: {participant_name}\n" \
                         f"Setting ID: {self.settings['settingID']}\n\n" \
                         f"Correct Answers: {self.correct_answers}\n" \
                         f"Correct Rate: {correct_rate:.2f}%\n" \
                         f"Total Time Cost: {total_test_time:.2f} seconds"
        messagebox.showinfo("Success", result_message)
        self.return_to_main()

    def retake_test(self):
        self.root.destroy()
        TestRunner(self.root.master, self.settings, self.app)

    def return_to_main(self):
        self.root.destroy()
        self.app.root.focus_set()  # Set focus back to the main application window
