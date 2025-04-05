import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os

class PDFModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Modifier App")

        # Buttons
        tk.Button(root, text="Password Protect PDF", command=self.password_protect).pack(pady=5)
        tk.Button(root, text="Remove PDF Password", command=self.remove_password).pack(pady=5)
        tk.Button(root, text="Resize PDF", command=self.resize_pdf).pack(pady=5)
        tk.Button(root, text="Merge PDFs", command=self.merge_pdfs).pack(pady=5)
        tk.Button(root, text="Remove Pages", command=self.remove_pages).pack(pady=5)
        tk.Button(root, text="Add Watermark", command=self.add_watermark).pack(pady=5)

    def password_protect(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            password = simpledialog.askstring("Password", "Enter a password:")
            if password:
                reader = PdfReader(file)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                writer.encrypt(password)
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                with open(output_file, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", "PDF Password Protected Successfully!")

    def remove_password(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            password = simpledialog.askstring("Password", "Enter the password:")
            try:
                reader = PdfReader(file)
                if reader.is_encrypted:
                    reader.decrypt(password)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                with open(output_file, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", "Password Removed Successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def resize_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            reader = PdfReader(file)
            writer = PdfWriter()
            for page in reader.pages:
                page.scale_by(0.75)  # Resizing to 75%
                writer.add_page(page)
            output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", "PDF Resized Successfully!")

    def merge_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if files:
            writer = PdfWriter()
            for file in files:
                reader = PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
            output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", "PDFs Merged Successfully!")

    def remove_pages(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            reader = PdfReader(file)
            pages_to_remove = simpledialog.askstring("Pages", "Enter page numbers to remove (comma-separated):")
            if pages_to_remove:
                pages_to_remove = [int(num) - 1 for num in pages_to_remove.split(",")]
                writer = PdfWriter()
                for i, page in enumerate(reader.pages):
                    if i not in pages_to_remove:
                        writer.add_page(page)
                output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
                with open(output_file, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", "Pages Removed Successfully!")

    def add_watermark(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        watermark_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")], title="Select Watermark PDF")
        if file and watermark_file:
            reader = PdfReader(file)
            watermark = PdfReader(watermark_file).pages[0]
            writer = PdfWriter()
            for page in reader.pages:
                page.merge_page(watermark)
                writer.add_page(page)
            output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", "Watermark Added Successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFModifierApp(root)
    root.mainloop()
