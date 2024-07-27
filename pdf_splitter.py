import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

class PDFToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Muj PDF tool")
        self.geometry("400x400")
        self.configure(bg='#e0e0e0')
        self.create_widgets()

    def create_widgets(self):
        button_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 12, 'bold'), 'relief': 'flat'}

        merge_button = tk.Button(self, text="Merge PDFs", command=self.merge_pdfs, **button_style)
        merge_button.pack(pady=15, fill='x', padx=20)

        split_button = tk.Button(self, text="Split PDF", command=self.split_pdf, **button_style)
        split_button.pack(pady=15, fill='x', padx=20)

        split_after_button = tk.Button(self, text="Split after PDF", command=self.split_after_pdf, **button_style)
        split_after_button.pack(pady=15, fill='x', padx=20)

        extract_button = tk.Button(self, text="Extract Text", command=self.extract_text, **button_style)
        extract_button.pack(pady=15, fill='x', padx=20)

        rotate_button = tk.Button(self, text="Rotate Pages", command=self.rotate_pages, **button_style)
        rotate_button.pack(pady=15, fill='x', padx=20)

        rotate_chosen_button = tk.Button(self, text="Rotate Chosen Pages", command=self.rotate_chosen_pages, **button_style)
        rotate_chosen_button.pack(pady=15, fill='x', padx=20)

    def merge_pdfs(self):
        try:
            files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
            if files:
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output_file:
                    merger = PdfMerger()
                    for pdf in files:
                        merger.append(pdf)
                    merger.write(output_file)
                    merger.close()
                    messagebox.showinfo("Success", "PDFs merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging PDFs: {e}")

    def split_pdf(self):
        try:
            file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file:
                reader = PdfReader(file)
                for i in range(len(reader.pages)):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"page_{i+1}.pdf")
                    if output_file:
                        with open(output_file, 'wb') as output_pdf:
                            writer.write(output_pdf)
                messagebox.showinfo("Success", "PDF split successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while splitting the PDF: {e}")

    def split_after_pdf(self):
        # split_after in nr. of page, after wchich the pdf is splitted
        try:
            file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file:
                num_pages = len(PdfReader(file).pages)
                split_after = simpledialog.askinteger("Input", f"Enter page number to split after (1-{num_pages}):", minvalue=1, maxvalue=num_pages)
                
                if split_after is None or split_after < 1 or split_after >= num_pages:
                    messagebox.showerror("Error", "Invalid page number. Please enter a valid number.")
                    return

                reader = PdfReader(file)
                writer1 = PdfWriter()
                writer2 = PdfWriter()

                for i in range(split_after):
                    writer1.add_page(reader.pages[i])

                for i in range(split_after, num_pages):
                    writer2.add_page(reader.pages[i])

                output_file1 = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="part1.pdf")
                if output_file1:
                    with open(output_file1, 'wb') as output_pdf:
                        writer1.write(output_pdf)

                output_file2 = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="part2.pdf")
                if output_file2:
                    with open(output_file2, 'wb') as output_pdf:
                        writer2.write(output_pdf)

                messagebox.showinfo("Success", "PDF split successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while splitting the PDF: {e}")

    def extract_text(self):
        try:
            file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                output_file = filedialog.asksaveasfilename(defaultextension=".txt")
                if output_file:
                    with open(output_file, 'w') as output_txt:
                        output_txt.write(text)
                    messagebox.showinfo("Success", "Text extraction successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while extracting text: {e}")

    def rotate_pages(self):
        try:
            file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file:
                angle = simpledialog.askinteger("Input", "Enter rotation angle (90, 180, 270):")
                if angle not in [90, 180, 270]:
                    messagebox.showerror("Error", "Invalid angle. Please enter 90, 180, or 270.")
                    return
                
                reader = PdfReader(file)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.rotate(angle)
                    writer.add_page(page)
                
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output_file:
                    with open(output_file, 'wb') as output_pdf:
                        writer.write(output_pdf)
                    messagebox.showinfo("Success", "PDF rotation successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while rotating the PDF: {e}")

    def rotate_chosen_pages(self):
        try:
            file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if file:
                reader = PdfReader(file)
                num_pages = len(reader.pages)
                
                while True:
                    try:
                        page_nums = simpledialog.askstring("Input", f"Enter page numbers to rotate (comma-separated, 1-{num_pages}):")
                        if page_nums is None:
                            return
                        
                        page_nums = [int(p.strip()) for p in page_nums.split(',')]
                        if any(p < 1 or p > num_pages for p in page_nums):
                            raise ValueError("Page number out of range.")
                        
                        break
                    except ValueError:
                        messagebox.showerror("Error", "Invalid page numbers. Please enter valid numbers.")

                angle = simpledialog.askinteger("Input", "Enter rotation angle (90, 180, 270):")
                if angle not in [90, 180, 270]:
                    messagebox.showerror("Error", "Invalid angle. Please enter 90, 180, or 270.")
                    return
                
                writer = PdfWriter()
                
                for i, page in enumerate(reader.pages):
                    if i + 1 in page_nums:
                        page.rotate(angle)
                    writer.add_page(page)
                
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                if output_file:
                    with open(output_file, 'wb') as output_pdf:
                        writer.write(output_pdf)
                    messagebox.showinfo("Success", "Chosen pages rotation successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while rotating chosen pages: {e}")

if __name__ == "__main__":
    app = PDFToolkit()
    app.mainloop()