import pandas as pd
import spacy
import tkinter as tk
from tkinter import messagebox

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

# Load the dataset
df = pd.read_csv('mediiii.csv')

# Function to preprocess text using NLP and extract symptoms
def extract_symptoms(user_input):
    doc = nlp(user_input.lower())
    extracted_symptoms = []
    for token in doc:
        if token.text in df['symptom'].str.lower().tolist():
            extracted_symptoms.append(token.text)
    return extracted_symptoms

# Function to get recommended medicine based on symptoms
def recommend_medicine(selected_symptoms):
    print(f"Filtering for symptoms: {', '.join(selected_symptoms)}")
    filtered_df = df[df['symptom'].str.lower().isin([sym.lower() for sym in selected_symptoms])]
    print(f"Filtered DataFrame:\n{filtered_df}")
    if not filtered_df.empty:
        medicine = filtered_df.iloc[0]['medicine']
        dosage = filtered_df.iloc[0]['dosage']
        return medicine, dosage
    else:
        return None, "No recommendation found. Please consult a doctor."

# Tkinter UI setup
class MedicineBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Recommendation Bot with NLP")
        self.root.geometry("800x650")
        self.root.configure(bg="#ADD8E6")

        self.homepage()

    def homepage(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Medicine Recommendation Bot with NLP", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        self.label.pack(pady=10)

        self.choice_label = tk.Label(self.root, text="Would you like to get a recommendation based on symptoms?", font=("Helvetica", 12), bg="#ADD8E6")
        self.choice_label.pack(pady=5)

        self.symptom_input_label = tk.Label(self.root, text="Enter your symptoms (e.g., 'I have a headache and nausea'):", font=("Helvetica", 12), bg="#ADD8E6")
        self.symptom_input_label.pack(pady=5)

        self.symptom_input = tk.Entry(self.root, width=50, font=("Helvetica", 12))
        self.symptom_input.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.process_symptoms, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button.pack(pady=20)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.quit_button.pack(pady=10)

    def process_symptoms(self):
        user_input = self.symptom_input.get()
        if not user_input.strip():
            messagebox.showerror("Error", "Please enter your symptoms.")
            return

        extracted_symptoms = extract_symptoms(user_input)
        if not extracted_symptoms:
            messagebox.showerror("Error", "No recognizable symptoms found. Please try again.")
        else:
            medicine, dosage = recommend_medicine(extracted_symptoms)
            if medicine:
                messagebox.showinfo("Recommendation", f"Recommended medicine: {medicine}\nDosage: {dosage}")
            else:
                messagebox.showinfo("Recommendation", "No recommendation found. Please consult a doctor.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineBotApp(root)
    root.mainloop()
