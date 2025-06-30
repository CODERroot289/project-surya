from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel,
    QPushButton, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
import sys

class DateEditPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Date")
        self.resize(250, 120)

        layout = QVBoxLayout()

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.show_selected_date)

        layout.addWidget(QLabel("Choose a date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def show_selected_date(self):
        date = self.date_edit.date()
        date_str = date.toString("dd MMMM yyyy")
        QMessageBox.information(self, "Selected Date", f"You chose: {date_str}")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DateEditPopup()
    dialog.exec_()
