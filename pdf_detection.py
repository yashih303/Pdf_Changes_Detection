import fitz
from collections import Counter
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

pdf_path = None
analysis_data = []
default_font = None


# ---------------- Select PDF ----------------
def select_pdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        status_label.config(text="PDF Selected Successfully", fg="green")


# ---------------- Analyze PDF ----------------
def analyze_pdf():
    global analysis_data, default_font
    if not pdf_path:
        messagebox.showwarning("Warning", "Please select a PDF first!")
        return

    table.delete(*table.get_children())
    analysis_data.clear()

    doc = fitz.open(pdf_path)
    font_counter = Counter()

    for page_no, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        font = span["font"]
                        size = round(span["size"], 1)
                        bbox = span["bbox"]

                        font_counter[(font, size)] += 1
                        analysis_data.append(
                            (page_no, text, font, size, bbox)
                        )

    default_font = font_counter.most_common(1)[0][0]

    for row in analysis_data:
        changed = "YES" if (row[2], row[3]) != default_font else "NO"
        table.insert("", "end", values=(row[0], row[1], row[2], row[3], changed))

    status_label.config(text="Analysis Completed", fg="blue")


# ---------------- Generate Highlighted PDF ----------------
def generate_highlighted_pdf():
    if not analysis_data:
        messagebox.showwarning("Warning", "Please analyze the PDF first!")
        return

    doc = fitz.open(pdf_path)

    for item in analysis_data:
        page_no, text, font, size, bbox = item

        if (font, size) != default_font:
            page = doc[page_no - 1]
            rect = fitz.Rect(bbox)
            annot = page.add_rect_annot(rect)
            annot.set_colors(stroke=(1, 0, 0))  # Red
            annot.set_border(width=1)
            annot.update()

    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Highlighted PDF"
    )

    if save_path:
        doc.save(save_path)
        doc.close()
        messagebox.showinfo("Success", "Highlighted PDF Generated Successfully!")
        status_label.config(text="Highlighted PDF Saved", fg="green")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Font Change Detection in PDF")
root.geometry("950x550")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Font Change Detection in PDF Documents",
    font=("Arial", 16, "bold"),
    pady=10
)
title.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Select PDF ", width=18, command=select_pdf,).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Analyze PDF", width=18, command=analyze_pdf).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Generate Highlighted PDF", width=25, command=generate_highlighted_pdf).grid(row=0, column=2, padx=10)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

columns = ("Page", "Text", "Font", "Size", "Changed")
table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=table.yview)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=160)

table.pack(fill="both", expand=True)

status_label = tk.Label(root, text="Status: Ready", anchor="w")
status_label.pack(fill="x", padx=10, pady=5)

root.mainloop()