import tkinter as tk
import fitz
#from sys import ps1
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
        print("\n")
    except Exception as e:
        print(f"Error opening PDF file: {e}")

def get_total_page_number(file_path):
    try:
        pdf =  fitz.open(file_path)
        page_count = pdf.page_count
        print(f"Number of pages in the PDF: {page_count}\n")
    except Exception as e:
        print(f"error in opening file{e}")

def get_page_summary(file_path):
    try:
        pdf = fitz.open(file_path)
        num = int(input("Enter the page number you want to summarize: "))
        if num <1 or num > pdf.page_count:
            print(f"page number {num} is out of range. This PDF has only {pdf.page_count} pages.")
            return
        page_content = pdf.load_page(num-1).get_text()
        print(f"The content of page {num} is: \n")
        print(page_content)
        print("\n") 
    except Exception as e:
        print(f"Error opening PDF file: {e}")
    except ValueError as e:
        print(f"Our experts suggest {e} isn't a valid page number. Please try again.")

def get_pdf_content(file_path):
    try:
        pdf = fitz.open(file_path)
        number_pages = pdf.page_count
        pdf_content = []
        for i in range(0, number_pages):
            page_content = pdf.load_page(i).get_text()
            page_content = page_content.replace("\n", "  ")
            pdf_content.append(page_content)
            print(pdf_content)
    except Exception as e:
        print(f"Error opening PDF file: {e}")

while True:
    number_input  = input("To extract metadata from a PDF file, choose 1 \nTo find total page numbers from a PDF file, choose 2 \nTo summarize an individual page from PDF, choose 3 \nTo summarize whole PDF, choose 4 \nTo exit the program, choose q \n")
    if number_input == "1":
        get_metadata(file_path)
    elif number_input == "2":
        get_total_page_number(file_path)
    elif number_input == "3":
        get_page_summary(file_path)
    elif number_input == "4":
        get_pdf_content(file_path)
    elif number_input.lower() == "q":
        print("See you on the next PDF file!")
        break
    else:
        print("Invalid input. Please select a valid option.")

    
