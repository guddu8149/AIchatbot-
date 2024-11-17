import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Load the dataset
try:
    df = pd.read_csv('mediiii.csv')
    if df.empty:
        raise ValueError("The CSV file is empty.")
    if not all(col in df.columns for col in ['symptom', 'medicine', 'dosage']):
        raise ValueError("The CSV file must contain 'symptom', 'medicine', and 'dosage' columns.")
except FileNotFoundError:
    print("Error: mediiii.csv file not found.")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Function to get recommended medicine based on symptoms
def recommend_medicine(selected_symptoms):
    filtered_df = df[df['symptom'].str.lower().apply(
        lambda x: any(sym.lower() in x for sym in selected_symptoms))]
    if not filtered_df.empty:
        medicine = filtered_df.iloc[0]['medicine']
        dosage = filtered_df.iloc[0]['dosage']
        return medicine, dosage
    else:
        return None, "No recommendation found. Please consult a doctor."

# Function to list all available medicines
def list_all_medicines():
    return df['medicine'].unique().tolist()

# Function to get details of a specific medicine
def specific_medicine(medicine_name):
    filtered_df = df[df['medicine'].str.lower() == medicine_name.lower()]
    if not filtered_df.empty:
        return "\n".join([f"{key}: {value}" for key, value in filtered_df.iloc[0].to_dict().items()])
    else:
        return "Medicine not found. Please consult a doctor."

# Tkinter UI setup
class MedicineBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Recommendation Bot")
        self.root.geometry("800x650")
        self.root.configure(bg="#ADD8E6")

        self.symptoms_set = df['symptom'].unique().tolist()  # Dynamic symptoms list
        self.homepage()

    def homepage(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Medicine Recommendation Bot", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        self.label.pack(pady=10)

        self.choice_label = tk.Label(self.root, text="Would you like to take a specific medicine or get a recommendation based on symptoms?", font=("Helvetica", 12), bg="#ADD8E6")
        self.choice_label.pack(pady=5)

        self.choice_var = tk.StringVar(value="medicine")
        self.medicine_radio = tk.Radiobutton(self.root, text="Medicine", variable=self.choice_var, value="medicine", bg="#ADD8E6", font=("Helvetica", 12))
        self.medicine_radio.pack(anchor="w", padx=20)

        self.symptoms_radio = tk.Radiobutton(self.root, text="Symptoms", variable=self.choice_var, value="symptoms", bg="#ADD8E6", font=("Helvetica", 12))
        self.symptoms_radio.pack(anchor="w", padx=20)

        self.continue_button = tk.Button(self.root, text="Continue", command=self.next_step, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.continue_button.pack(pady=20)

    def next_step(self):
        choice = self.choice_var.get()
        if choice == "medicine":
            self.medicine_step()
        elif choice == "symptoms":
            self.symptoms_step()

    def medicine_step(self):
        self.clear_frame()

        self.medicine_label = tk.Label(self.root, text="Please select the medicine:", font=("Helvetica", 12), bg="#ADD8E6")
        self.medicine_label.pack(pady=5)

        # Dropdown menu for medicines
        medicines = list_all_medicines()
        self.medicine_var = tk.StringVar(value=medicines[0])
        self.medicine_menu = tk.OptionMenu(self.root, self.medicine_var, *medicines)
        self.medicine_menu.config(font=("Helvetica", 12), bg="#ADD8E6")
        self.medicine_menu.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.show_medicine, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.homepage, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.back_button.pack(pady=10)

    def show_medicine(self):
        medicine_name = self.medicine_var.get()
        medicine_details = specific_medicine(medicine_name)
        messagebox.showinfo("Medicine Details", medicine_details)

    def symptoms_step(self):
        self.clear_frame()

        self.symptom_label = tk.Label(self.root, text="Please select your symptoms:", font=("Helvetica", 12), bg="#ADD8E6")
        self.symptom_label.pack(pady=5)

        # Checkboxes for symptoms
        self.selected_symptoms = []
        self.checkbuttons = []
        for symptom in self.symptoms_set:
            var = tk.StringVar()
            chk = tk.Checkbutton(self.root, text=symptom, variable=var, onvalue=symptom, offvalue="", bg="#ADD8E6", font=("Helvetica", 12))
            chk.pack(anchor="w", padx=20)
            self.checkbuttons.append((chk, var))
        self.submit_button = tk.Button(self.root, text="Submit", command=self.show_recommendation, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.homepage, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.back_button.pack(pady=10)

    def show_recommendation(self):
        self.selected_symptoms = [var.get() for chk, var in self.checkbuttons if var.get()]
        if not self.selected_symptoms:
            messagebox.showerror("Error", "Please select at least one symptom.")
            return
        medicine, dosage = recommend_medicine(self.selected_symptoms)
        messagebox.showinfo("Recommendation", f"For {', '.join(self.selected_symptoms)}, I recommend {medicine} with a dosage of {dosage}.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineBotApp(root)
    root.mainloop()
