# Pdf_Changes_Detection
Project Overview:-
Font Change Detection in PDF Documents is a Python-based application designed to automatically detect and highlight font inconsistencies within PDF files. The project follows a rule-based approach, eliminating the need for machine learning models or training datasets. It is especially useful for document verification, auditing, and quality assurance in academic and organizational environments.The system identifies the most frequently used font in a document (default font) and flags any text that deviates from it. Detected font changes are visually highlighted in a newly generated PDF file.

Objectives:-
Extract font names and font sizes used in a PDF document
Identify the default (most frequently used) font
Detect font changes across the document
Highlight font inconsistencies directly in the PDF
Provide a user-friendly GUI for easy interaction
Support batch processing of multiple PDF files

Technologies & Libraries Used:-
Python 3.11
PyMuPDF (fitz) – PDF text and font extraction
Tkinter & ttk – GUI development
collections.Counter – Font frequency analysis
