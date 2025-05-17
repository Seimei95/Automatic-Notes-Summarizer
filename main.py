import tkinter as tk
import fitz
from tkinter import filedialog

print("Welcome to Automatic Notes summarizer \n")
print("This program will help you summarize your notes and make them more concise.\n")
print("Please select a PDF file to extract metadata from: \n")

root = tk.Tk()
root.withdraw()  

file_path = filedialog.askopenfilename(
    title = "Select a file:"
    )

def get_metadata(file_path):
    try:
        pdf = fitz.open(file_path)
        metadata = pdf.metadata
        for key, value in metadata.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error opening PDF file: {e}")
    exit()

number_input  = input("To extract metadata from a PDF file, choose 1 \n")
if number_input == "1":
    get_metadata(file_path)
else:
    print("Invalid input. Please select a valid option.")
    exit()
