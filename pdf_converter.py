import os
from fpdf import FPDF
from PyPDF2 import PdfReader
from docx import Document
from pdf2docx import Converter
import tkinter as tk
from tkinter import filedialog, messagebox

class FileConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Muj konvertor")
        self.geometry("400x150")
        self.vytvor_widgets()

    def vytvor_widgets(self):
        button_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 12, 'bold'), 'relief': 'flat'}

        convert_pdf_to_txt_button = tk.Button(self, text="Convert PDF to TXT", command=self.convert_pdf_to_txt, **button_style)
        convert_pdf_to_txt_button.pack(pady=10, fill='x', padx=20)

        convert_pdf_to_docx_button = tk.Button(self, text="Convert PDF to DOCX", command=self.convert_pdf_to_docx, **button_style)
        convert_pdf_to_docx_button.pack(pady=10, fill='x', padx=20)

    
    def convert_pdf_to_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        txt_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not txt_path:
            return

        try:
            reader = PdfReader(file_path)
            with open(txt_path, 'w') as file:
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        file.write(text)
            messagebox.showinfo("Success", "PDF file converted to TXT successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert PDF to TXT: {e}")

    def convert_pdf_to_docx(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        docx_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])
        if not docx_path:
            return

        try:
            converter = Converter(file_path)
            converter.convert(docx_path, start=0, end=None)
            converter.close()
            messagebox.showinfo("Success", "PDF file conversion to DOCX successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert PDF to DOCX: {e}")

if __name__ == "__main__":
    app = FileConverterApp()
    app.mainloop()


