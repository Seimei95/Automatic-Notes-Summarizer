import tkinter as tk
import fitz
import string, re
from tkinter import filedialog
import nltk
import os
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq
from app import generate_summary

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
        if num < 1 or num > pdf.page_count:
            print(f"page number {num} is out of range. This PDF has only {pdf.page_count} pages.")
            return
        print(f"The content of page {num} is: \n")
        page_content = pdf.load_page(num-1).get_text()
        page_content = page_content.lower()
        page_content = re.sub(r"\d+"," ",page_content)
        page_content = page_content.translate(str.maketrans(" "," ",string.punctuation))
        page_content = re.sub(r"\s+"," ",page_content).strip()
        NLTK_cache_path = os.path.join(os.path.dirname(__file__),"NLTK_cache")
        if not os.path.exists(NLTK_cache_path):
            os.makedirs(NLTK_cache_path)
        nltk.data.path.append("NLTK_cache")
        text = page_content
        sentences = sent_tokenize(text)
        vectorize = TfidfVectorizer()
        matrix = vectorize.fit_transform(sentences)
        num_sentences = 3
        sentence_scores = matrix.sum(axis = 1)
        scored_sentences = [(score.item(), idx ,sent) for idx, (score, sent) in enumerate(zip(sentence_scores, sentences))]
        top_sentences = heapq.nlargest(num_sentences, scored_sentences, key=lambda x: x[0])
        top_sentences_sorted = sorted(top_sentences, key=lambda x: x[1])
        summary = " ".join([sent for _, _, sent in top_sentences_sorted])
        print(f"{summary}\n")
        return summary  
    except Exception as e:
        print(f"Error opening PDF file: {e}")
    except ValueError as e:
        print(f"Our experts suggest {e} isn't a valid page number. Please try again.")

def get_pdf_content(file_path):
    try:
        pdf = fitz.open(file_path)
        all_text = []
        for i in range(0, pdf.page_count):
            page_content = pdf.load_page(i).get_text()
            page_content = page_content.lower()
            page_content = re.sub(r"\d+","",page_content)
            page_content = page_content.translate(str.maketrans(" "," ",string.punctuation))
            page_content = re.sub(r"\s+"," ",page_content).strip()
            all_text.append(page_content)
        final_text = "".join(all_text)
        NLTK_cache_path = os.path.join(os.path.dirname(__file__),"NLTK_cache")
        if not os.path.exists(NLTK_cache_path):
            os.makedirs("NLTK_cache")
        nltk.data.path.append("NLTK_cache")
        sentences = sent_tokenize(final_text)
        vectorize = TfidfVectorizer()
        matrix = vectorize.fit_transform(sentences)
        num_sentences = 10
        sentence_scores = matrix.sum(axis = 1)
        scored_sentences = [(score.item(), idx ,sent) for idx, (score, sent) in enumerate(zip(sentence_scores, sentences))]
        top_sentences = heapq.nlargest(num_sentences, scored_sentences, key=lambda x: x[0])
        top_sentences_sorted = sorted(top_sentences, key=lambda x: x[1])
        summary = " ".join([sent for _, _, sent in top_sentences_sorted])
        print(f"{summary}\n")
        return summary
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None
    except ValueError as e:
        print(f"Our experts suggest {e} isn't a valid PDF. Please try again.")

def summarize(text, mode="local"):
    if mode == "online":
        return generate_summary(text)
    else:
        return get_pdf_content(text)

while True:
    number_input  = input("To extract metadata from a PDF file, choose 1 \nTo find total page numbers from a PDF file, choose 2 \nTo summarize an individual page from PDF, choose 3 \nTo summarize whole PDF, choose 4 \nTo exit the program, choose q \n")
    if number_input == "1":
        get_metadata(file_path)
    elif number_input == "2":
        get_total_page_number(file_path)
    elif number_input == "3":
        get_page_summary(file_path)
    elif number_input == "4":
        choice = input(str(f"Please choose an option y/n" "\n" "Online Advanced summary - y or Simple Offline Summary - n"))
        if choice == "y":
            summarize(file_path, mode = "online")
        elif choice == "n":
            summarize(file_path)
        else:
            print("Invalid option, Please choose either y/n")
    elif number_input.lower() == "q":
        print("See you on the next PDF file!")
        break
    else:
        print("Invalid input. Please select a valid option.")

    

