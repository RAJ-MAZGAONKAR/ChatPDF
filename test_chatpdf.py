import os
import PyPDF2
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import PunktSentenceTokenizer
import string
import wikipedia
import subprocess
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, filedialog, Frame, PhotoImage
from tkinter.ttk import Style
from tkinter.font import Font
import webbrowser
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pyttsx3
import threading
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


# Initialize the text-to-speech engine
engine = pyttsx3.init()

def load_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def preprocess_text(text):
    # Tokenize sentences
    sent_tokenizer = PunktSentenceTokenizer()
    sentences = sent_tokenizer.tokenize(text)

    # Tokenize words, lemmatize
    lemmatizer = WordNetLemmatizer()
    preprocessed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum() and word != ' ']
        preprocessed_sentences.append(words)

    return preprocessed_sentences


def answer_questions(preprocessed_sentences, question, num_sentences=3):
    question_tokens = word_tokenize(question.lower())
    question_tokens = [WordNetLemmatizer().lemmatize(token) for token in question_tokens]

    sentences = []

    for sentence in preprocessed_sentences:
        overlap = len(set(sentence) & set(question_tokens))
        if overlap > 0:
            sentences.append((sentence, overlap))

    sentences.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [s[0] for s in sentences[:num_sentences]]

    return top_sentences

def open_wikipedia_page(url):
    subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', url])
    
def search_and_retrieve_summary(query):
    url = f"https://www.example.com/search?q={query}"  # Replace "example.com" with the actual website you want to search
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract the relevant summary from the website
    summary = ""
    summary_element = soup.find('div', class_='summary')  # Replace 'div' and 'summary' with the appropriate HTML tags and class names
    if summary_element:
        summary = summary_element.text.strip()

    return summary
import requests

def preprocess_text(text):
    # Tokenize sentences
    sent_tokenizer = PunktSentenceTokenizer()
    sentences = sent_tokenizer.tokenize(text)

    # Tokenize words, lemmatize
    lemmatizer = WordNetLemmatizer()
    preprocessed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum() and word != ' ']
        preprocessed_sentences.append(words)

    return preprocessed_sentences


def answer_questions(preprocessed_sentences, question, num_sentences=3):
    question_tokens = word_tokenize(question.lower())
    question_tokens = [WordNetLemmatizer().lemmatize(token) for token in question_tokens]

    sentences = []

    for sentence in preprocessed_sentences:
        overlap = len(set(sentence) & set(question_tokens))
        if overlap > 0:
            sentences.append((sentence, overlap))

    sentences.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [s[0] for s in sentences[:num_sentences]]

    return top_sentences

def open_wikipedia_page(url):
    subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', url])
    

def search_wikipedia():
    question = question_entry.get()

    if not question:
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.insert(END, "Please enter a question or keyword.")
        answer_text.configure(state="disabled")  # Disable the text box
        return

    # Search Wikipedia for the question
    try:
        search_results = wikipedia.search(question, results=5)
        if not search_results:
            raise wikipedia.exceptions.PageError

        # Get the page for the first search result
        wikipedia_page = wikipedia.page(search_results[0])
        wikipedia_answer = wikipedia_page.summary
        wikipedia_link = wikipedia_page.url  # Retrieve the page URL
    except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
        wikipedia_answer = None
        wikipedia_link = None

    answer_text.configure(state="normal")  # Enable the text box
    answer_text.delete('1.0', END)

    if wikipedia_answer:
        answer_text.insert(END, "Summary:\n")
        answer_text.insert(END, wikipedia_answer + "\n\n")
        if wikipedia_link:
            answer_text.insert(END, "Source (Refer this for more info.): ")
            answer_text.insert(END, wikipedia_link, "link")  # Insert the link with "link" tag
            answer_text.tag_config("link", foreground="blue", underline=True)  # Configure the "link" tag
            answer_text.tag_bind("link", "<Button-1>", lambda event, url=wikipedia_link: open_wikipedia_page(url))
    else:
        answer_text.insert(END, "No relevant answer found in Wikipedia.")

    answer_text.configure(state="disabled")  # Disable the text box



def open_web_page(url):
    subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', url])


def search_google():
    question = question_entry.get()

    if not question:
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.insert(END, "Please enter a question or keyword.")
        answer_text.configure(state="disabled")  # Disable the text box
        return

    # Perform Google search for the question
    try:
        search_results = search(question, num_results=3)
        if not search_results:
            raise Exception

        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)

        answer_text.insert(END, "Top Google Search Results:\n\n")
        for i, result in enumerate(search_results):
            answer_text.insert(END, f"{i + 1}. ")
            answer_text.insert(END, result, f"link{i + 1}")
            answer_text.tag_config(f"link{i + 1}", foreground="blue", underline=True)
            answer_text.tag_bind(f"link{i + 1}", "<Button-1>", lambda event, url=result: open_web_page(url))
            answer_text.insert(END, "\n")

    except:
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.insert(END, "No relevant search results found.")
    
    answer_text.configure(state="disabled")  # Disable the text box




def summarize_pdf(file_path, max_sentences):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, max_sentences)

    summarized_text = '\n'.join(str(sentence) for sentence in summary_sentences)
    return summarized_text




from tkinter import simpledialog

def summarize_pdf_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        max_sentences = simpledialog.askinteger("Number of Sentences", "Enter the number of sentences to summarize the pdf in:", parent=answer_text)
        if max_sentences is not None:
            summarized_text = summarize_pdf(file_path, max_sentences)
            answer_text.configure(state="normal")
            answer_text.delete('1.0', END)
            answer_text.insert(END, summarized_text)
            answer_text.configure(state="disabled")






def process_question():
    question = question_entry.get()

    if 'preprocessed_sentences' not in globals():
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.insert(END, "Please select a PDF file first.")
        answer_text.configure(state="disabled")  # Disable the text box
        return

    sentences = answer_questions(preprocessed_sentences, question)

    if not sentences:
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.insert(END, "No relevant answer found.")
        answer_text.configure(state="disabled")  # Disable the text box
    else:
        answer_text.configure(state="normal")  # Enable the text box
        answer_text.delete('1.0', END)
        answer_text.tag_config("question", foreground="blue")
        answer_text.tag_config("answer", foreground="green")
        answer_text.insert(END, "Question: ", "question")
        answer_text.insert(END, question + "\n\n", "question")
        answer_text.insert(END, "Top Answers:\n", "answer")

        for sentence in sentences:
            answer_text.insert(END, "- " + ' '.join(sentence) + "\n")

        answer_text.configure(state="disabled")  # Disable the text box


def load_files():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if file_path:
        try:
            text = load_pdf(file_path)
            global preprocessed_sentences
            preprocessed_sentences = preprocess_text(text)
            status_label.config(text="PDF file loaded successfully.", font=("Arial", 12, "bold"), bg="light green")
        except:
            status_label.config(text="Error occurred while loading the PDF file.", font=("Arial", 12, "bold"), bg="red")
    else:
        status_label.config(text="No PDF file selected.",font=("Arial", 12, "bold"), bg="yellow")

def load_folder():
    folder_path = filedialog.askdirectory()

    if folder_path:
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

        if not pdf_files:
            status_label.config(text="No PDF files found in the selected folder.",font=("Arial", 12, "bold"), bg="yellow")
            return

        global preprocessed_sentences
        preprocessed_sentences = []
        for file_name in pdf_files:
            file_path = os.path.join(folder_path, file_name)
            try:
                text = load_pdf(file_path)
                preprocessed_sentences.extend(preprocess_text(text))
            except:
                status_label.config(text="Error occurred while loading the PDF files.",font=("Arial", 12, "bold"), bg="red")
                return
        
        status_label.config(text="PDF files loaded successfully.",font=("Arial", 12, "bold"), bg="light green")

def clear_text():
    answer_text.configure(state="normal")
    answer_text.delete('1.0', END)
    answer_text.configure(state="disabled")

def clear_status():
    status_label.config(text="")

# Global variable to track the speech conversion status
speech_conversion_active = False


# Convert the answer text into speech
def convert_to_speech():
    answer = answer_text.get("1.0", "end")
    speech_thread = threading.Thread(target=speak, args=(answer,))
    speech_thread.start()

def speak(answer):
    engine.say(answer)
    engine.runAndWait()


    
# Create the GUI window
window = Tk()
window.title("PDF Question Answering")
window.geometry("900x700")
window.configure(bg="light blue")

# Left frame for input elements and status
left_frame = Frame(window, bg="light blue")
left_frame.pack(side="left", padx=40, pady=40)

# Logo
watermark_image = PhotoImage(file="C:/Users/RAJ/Desktop/PDF CHATBOT/hindustan_petroleum_logo.png")  # Replace with the path to your logo image
watermark_label = Label(left_frame, image=watermark_image, bg="light blue")
watermark_label.pack()

# File Input
file_label = Label(left_frame, text="Select PDF file:", font=("Arial", 10, "bold", "italic"), bg="light blue")
file_label.pack()
file_button = Button(left_frame, text="SELECT PDF", command=load_files)
file_button.pack(padx=10, pady=10)

# Folder Input
folder_label = Label(left_frame, text="Select folder path:", font=("Arial", 10, "bold", "italic"), bg="light blue")
folder_label.pack()
folder_button = Button(left_frame, text="SELECT Folder", command=load_folder)
folder_button.pack(padx=10, pady=10)

# Question Input
question_label = Label(left_frame, text="Enter your question or necessary Keyword:", font=("Arial", 14), bg="light blue")
question_label.pack()
question_entry = Entry(left_frame, width=60, font=("Arial", 10))
question_entry.pack(padx=5, pady=5)

# Search Wikipedia Button
search_wikipedia_button = Button(left_frame, text="Search Wikipedia", font=("Arial", 10, "bold", "italic"), command=search_wikipedia)
search_wikipedia_button.pack(padx=5, pady=5)

# Search in PDF Button
search_pdf_button = Button(left_frame, text="Search in PDF", font=("Arial", 10, "bold", "italic"), command=process_question)
search_pdf_button.pack(padx=5, pady=5)

# Search Google Button
search_google_button = Button(left_frame, text="Search Google", font=("Arial", 10, "bold", "italic"), command=search_google)
search_google_button.pack(padx=5, pady=5)

# Create the Summarize PDF button
summarize_pdf_button = Button(window, text="Summarize PDF", font=("Arial", 10, "bold", "italic"), command=summarize_pdf_button_click)
summarize_pdf_button.pack(padx=5, pady=5)

# Status Label
status_label = Label(left_frame, text="", bg="light blue")
status_label.pack()

# Right frame for answer display
right_frame = Frame(window)
right_frame.pack(side="right", padx=10, pady=10)

# Answer Label
answer_label = Label(right_frame, text="Answer:")
answer_label.pack()

# Answer Text Box
answer_text = Text(right_frame, height=30, width=90, font=Font(family="Times New Roman"), wrap="word")
answer_text.pack()
answer_text.configure(state="disabled")


# Convert to Speech Button
sound_button = Button(right_frame, text="🔊", font=Font(family="Arial", size=20, weight="bold"), command=convert_to_speech)
sound_button.pack(side="left", padx=5, pady=10)


# Scrollbar for Answer Text Box
scrollbar = Scrollbar(right_frame)
scrollbar.pack(side="right", fill="y")
answer_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=answer_text.yview)

# Clear Answer Button
clear_button = Button(right_frame, text="Clear Answer", font=("Arial", 10, "bold"), command=clear_text)
clear_button.pack()

# Start the GUI event loop
window.mainloop()
