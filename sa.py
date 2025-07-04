# from PyQt5.QtWidgets import (
#     QApplication, QDialog, QVBoxLayout, QLabel,
#     QPushButton, QDateEdit, QMessageBox
# )
# from PyQt5.QtCore import QDate
# import sys

# class DateEditPopup(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Select Date")
#         self.resize(250, 120)

#         layout = QVBoxLayout()

#         self.date_edit = QDateEdit(QDate.currentDate())
#         self.date_edit.setCalendarPopup(True)

#         self.ok_button = QPushButton("OK")
#         self.ok_button.clicked.connect(self.show_selected_date)

#         layout.addWidget(QLabel("Choose a date:"))
#         layout.addWidget(self.date_edit)
#         layout.addWidget(self.ok_button)
#         self.setLayout(layout)

#     def show_selected_date(self):
#         date = self.date_edit.date()
#         date_str = date.toString("dd MMMM yyyy")
#         QMessageBox.information(self, "Selected Date", f"You chose: {date_str}")
#         self.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = DateEditPopup()
#     dialog.exec_()'
# from PyQt5.QtWidgets import QApplication, QLabel
# from PyQt5.QtGui import QFont, QFontDatabase
# import sys,time

# app = QApplication(sys.argv)

# # Check available fonts
# available_fonts = QFontDatabase().families()
# preferred_fonts = [
#     "Noto Sans Malayalam",
#     "Rachana",
#     "Meera",
#     "AnjaliOldLipi",
#     "Kartika"  # fallback font in Windows for Malayalam
# ]

# # Select the first matching Malayalam-supporting font
# L=[]
# for font_name in preferred_fonts:
#     print(available_fonts)
#     if font_name in available_fonts:
#         mal_font = QFont(font_name, 20)
#         L.append(mal_font)
#         break
# else:
#     mal_font = QFont("Arial", 20)  # Fallback (will render broken text)

# label = QLabel("അശ്വതി, ഭൂതം, കാർത്തിക")
# label
# time.sleep(5)
# label.show()

# sys.exit(app.exec_())
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
# from PyQt5.QtGui import QFont
# from googletrans import Translator

# class TranslatorApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Live Google Malayalam Translator")
#         self.setMinimumWidth(500)

#         self.translator = Translator()

#         layout = QVBoxLayout()

#         self.input_line = QLineEdit()
#         self.input_line.setPlaceholderText("Type in English...")
#         self.input_line.textChanged.connect(self.translate_text)

#         self.output_label = QLabel("")
#         self.output_label.setFont(QFont("Noto Sans Malayalam", 20))  # Make sure this font is installed

#         layout.addWidget(self.input_line)
#         layout.addWidget(self.output_label)
#         self.setLayout(layout)

#     def translate_text(self, text):
#         if not text.strip():
#             self.output_label.setText("")
#             return

#         try:
#             translated = self.translator.translate(text, src='en', dest='ml')
#             self.output_label.setText(translated.text)
#         except Exception as e:
#             self.output_label.setText("Translation error")

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = TranslatorApp()
#     window.show()
#     sys.exit(app.exec_())
import tkinter as tk
from tkinter import messagebox
import tempfile
import os

# Sample dictionary
receipt_data = {
    "store_name": "Alstine Store",
    "address": "123 Main Street, City",
    "date": "2025-07-03",
    "items": [
        {"name": "Apple", "qty": 2, "price": 30},
        {"name": "Bread", "qty": 1, "price": 25},
        {"name": "Milk", "qty": 2, "price": 20}
    ],
    "tax": 5,
    "footer": "Thank you for shopping!"
}

# Generate receipt as text
def generate_receipt_text(data):
    lines = []
    lines.append(f"{data['store_name']}")
    lines.append(f"{data['address']}")
    lines.append(f"Date: {data['date']}")
    lines.append("=" * 30)
    total = 0
    for item in data['items']:
        name = item['name']
        qty = item['qty']
        price = item['price']
        amount = qty * price
        total += amount
        lines.append(f"{name:<10} x{qty:<2} @₹{price:<4} = ₹{amount}")
    lines.append("=" * 30)
    lines.append(f"Subtotal: ₹{total}")
    tax_amount = total * data['tax'] / 100
    lines.append(f"Tax ({data['tax']}%): ₹{tax_amount:.2f}")
    grand_total = total + tax_amount
    lines.append(f"Total: ₹{grand_total:.2f}")
    lines.append("=" * 30)
    lines.append(data['footer'])
    return "\n".join(lines)

# Print function
def print_receipt(text):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:

        f.write(text)
        filename = f.name

    try:
        os.startfile(filename, "print")  # Windows only
    except Exception as e:
        messagebox.showerror("Print Error", str(e))

# Preview window
def show_receipt_preview():
    receipt_text = generate_receipt_text(receipt_data)

    win = tk.Tk()
    win.title("Receipt Preview")
    win.geometry("400x500")

    text_box = tk.Text(win, font=("Courier", 10), wrap="none")
    text_box.insert("1.0", receipt_text)
    text_box.configure(state="disabled")
    text_box.pack(expand=True, fill="both", padx=10, pady=10)

    print_btn = tk.Button(win, text="🖨️ Print", command=lambda: print_receipt(receipt_text))
    print_btn.pack(pady=10)

    win.mainloop()

# Run
show_receipt_preview()
