# Medicine Recommendation Bot with NLP-
This project is a user-friendly Medicine Recommendation Bot built using Python, Tkinter, and Natural Language Processing (NLP). It enables users to receive medicine recommendations by entering their symptoms in natural language. The application uses spaCy for extracting relevant symptoms from free-text input, processes them against a predefined dataset (mediiii.csv), and provides accurate medicine suggestions along with the recommended dosage.

Natural Language Input:
Users can describe their symptoms in plain English (e.g., "I have a headache and nausea"). The bot uses NLP to identify relevant symptoms.

Medicine Recommendation:
Based on the symptoms, the bot recommends appropriate medicine and dosage from the dataset.

Tkinter-Based GUI:
A clean and intuitive graphical interface for entering symptoms and viewing recommendations.

Case-Insensitive Symptom Matching:
Matches symptoms regardless of capitalization or minor input variations.

Error Handling:
Alerts users when symptoms cannot be recognized or if the dataset does not have a matching medicine.
