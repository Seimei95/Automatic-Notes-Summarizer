import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  

file_path = filedialog.askopenfilename(
    title = "Select a file:"
    )
if file_path:
    print(f"Selected file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"file content is: {content}")
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print("No file selected.")
