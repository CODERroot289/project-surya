from PyQt5 import QtWidgets ,uic 
from PyQt5.QtWidgets import QWidget ,QDateEdit ,QMessageBox ,QVBoxLayout,QHBoxLayout,QPushButton,QDialog,QLabel 
from PyQt5.QtWidgets import  QFrame ,QScrollArea,QSizePolicy ,QTableWidget,QHeaderView ,QComboBox ,QTableWidgetItem
from PyQt5.QtWidgets import  QSpacerItem,QInputDialog, QMessageBox ,QApplication    
from PyQt5.QtCore import QDateTime ,pyqtSignal 
from PyQt5.QtCore import QDate ,QSize ,Qt
from PyQt5.QtGui import QIcon ,QKeyEvent
from PyQt5 import QtGui
import sys , datetime
from PyQt5.QtWidgets import QSpacerItem
import json
import os
from PyQt5.QtWidgets import QLineEdit, QCheckBox

now = datetime.datetime.now()
DATAFILE = "table.json"

# Format as "Day Month(in words) Year"
formatted_date = now.strftime("%d %B %Y")
default_table = {
    "columns" : ["പേര്", "നക്ഷത്രം", "പൂജകൾ","തുക"," "],
    "Rows": None,
    "nakshatram_m": ["അശ്വതി","ഭരണി","കാർത്തിക","രോഹിണി","മകം","തിരുവാതിര","ആഡ്ര","പൂയം","ആയില്യം","മകം","പൂരം","ഉത്രം","അത്തം","ചിത്തിര","ചോതി","വിശാഖം","അനിഴം","തൃക്കേട്ട","മൂലം","പൂരം","ഉത്രാടനം","തിരുവോണം","അവിട്ടം","ചതയം","പൂരം","ഉത്രട്ടാതി","രേവതി"],
    "nakshatram_l": ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"],
    "poojas":{}
}
# import winreg

# def is_dark_theme():
#     try:
#         registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
#         key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
#         # 0 = Dark, 1 = Light
#         value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
#         winreg.CloseKey(key)
#         return value == 0
#     except Exception as e:
#         print("Error reading system theme:", e)
#         return False  # Default to light if error

class CurrencyLineEdit(QLineEdit):
    def __init__(self, symbol='₹'):
        super().__init__()
        self.symbol = symbol
        self.setAlignment(Qt.AlignRight)
        self.setPlaceholderText("Enter amount")
        self.setText(self.symbol)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key in (Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
                   Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_Period):
            cursor_pos = self.cursorPosition()
            current_text = self.text().replace(self.symbol, "")
            new_text = current_text[:cursor_pos] + event.text() + current_text[cursor_pos:]
            self.setText(new_text + self.symbol)
            self.setCursorPosition(cursor_pos + 1)
        elif key == Qt.Key_Backspace:
            cursor_pos = self.cursorPosition()
            current_text = self.text().replace(self.symbol, "")
            if cursor_pos > 0:
                new_text = current_text[:cursor_pos - 1] + current_text[cursor_pos:]
                self.setText(new_text + self.symbol)
                self.setCursorPosition(cursor_pos - 1)
        elif key == Qt.Key_Delete:
            cursor_pos = self.cursorPosition()
            current_text = self.text().replace(self.symbol, "")
            if cursor_pos < len(current_text):
                new_text = current_text[:cursor_pos] + current_text[cursor_pos + 1:]
                self.setText(new_text + self.symbol)
                self.setCursorPosition(cursor_pos)
        elif key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
            super().keyPressEvent(event)  # Let normal cursor movement work
        else:
            event.ignore()  # Ignore other keys

    def value(self):
        """Returns the numeric value as float"""
        try:
            return float(self.text().replace(self.symbol, '').strip())
        except ValueError:
            return 0.0


class tableformat():
    def __init__(self):
        # self.columns = ["പേര്", "നക്ഷത്രം ", "പൂജകൾ","വില"," "]
        if not os.path.exists(DATAFILE):
    # Create the file with default data
            with open(DATAFILE, "w") as f:
                json.dump(default_table, f, indent=4)
            print("File created with default data.")    
        with open(DATAFILE, "r") as f:
            self.tabledata = json.load(f)
        print("Read JSON:", self.tabledata)
        self.columns = self.tabledata["columns"]
        self.nakshatram_m = self.tabledata["nakshatram_m"]
        self.nakshatram_l = self.tabledata["nakshatram_l"]
    def save(self):
        with open(DATAFILE, "w") as f:
            json.dump(self.tabledata, f, indent=4)

        print("Updated JSON:", self.tabledata)

# class 
tableformat = tableformat()
class tableformatGUI(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("tableformater.ui", self)
        self.ADD.clicked.connect(self.ADDproperties)
        self.SAVEB.clicked.connect(self.Save)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for x,y in tableformat.tabledata["poojas"].items():
            # print()
            self.ADDexistingproperties(x,y)




    def ADDproperties(self):
        row_index = self.tableWidget.rowCount()
        fontsize = 20
        self.tableWidget.insertRow(row_index)
        pooja = QLineEdit()

        pooja.setStyleSheet(f"""
            color:#ffffff;
            font-size:{fontsize}px;
            """)
        pooja.setPlaceholderText("type..")
        # pooja.setLayoutDirection(Qt.RightToLeft)
        pooja.setAlignment(Qt.AlignRight)

        currency_input = CurrencyLineEdit('₹')

        currency_input.setStyleSheet(f"""
            color:#fcba03;
            font-size:{fontsize}px;
            """)
        # currency_input.setPlaceholderText("type..")
        self.tableWidget.setCellWidget(row_index, 0, pooja)
        self.tableWidget.setCellWidget(row_index, 1, currency_input)

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 40) 
    def ADDexistingproperties(self,name,value):
        row_index = self.tableWidget.rowCount()
        fontsize = 20
        self.tableWidget.insertRow(row_index)
        pooja = QLineEdit(name)

        pooja.setStyleSheet(f"""
            color:#ffffff;
            font-size:{fontsize}px;
            """)
        pooja.setPlaceholderText("type..")
        # pooja.setLayoutDirection(Qt.RightToLeft)
        pooja.setAlignment(Qt.AlignRight)

        currency_input = CurrencyLineEdit('₹')
        currency_input.setText(value)
        currency_input.setStyleSheet(f"""
            color:#fcba03;
            font-size:{fontsize}px;
            """)
        # currency_input.setPlaceholderText("type..")
        self.tableWidget.setCellWidget(row_index, 0, pooja)
        self.tableWidget.setCellWidget(row_index, 1, currency_input)

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 40) 
       
        

        
        
        
    def Save(self):
        row = self.tableWidget.rowCount()
        dic =tableformat.tabledata["poojas"]
        print(dic)
        s = 0
        self.hide()
        for x in range(row):
            t = self.tableWidget.cellWidget(x, 0)
            a = self.tableWidget.cellWidget(x, 1)
            dic.update({t.text():a.text()})
            print(t.text())            


        tableformat.tabledata["poojas"] = dic
        tableformat.save()
        print(dic)
        
        
        
        
        



class TabM(QWidget):
    def __init__(self):
        super().__init__()

        # tableformat =tableformat()
        fontsize = 0




        scroll_style = """
/* Scroll Area Background */
QScrollArea {
    background-color: #1c1c1e;
    border: 1px solid #3a3a3c;
    border-radius: 8px;
    padding: 4px;
}

/* Vertical Scrollbar */
QScrollBar:vertical {
    background: transparent;
    width: 12px;
    margin: 2px 0 2px 0;
}

QScrollBar::handle:vertical {
    background: #5c5c5c;
    min-height: 30px;
    border-radius: 6px;
    border: 2px solid #3a3a3c;
}

QScrollBar::handle:vertical:hover {
    background: #888;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

/* Horizontal Scrollbar */
QScrollBar:horizontal {
    background: transparent;
    height: 12px;
    margin: 0 2px 0 2px;
}

QScrollBar::handle:horizontal {
    background: #5c5c5c;
    min-width: 30px;
    border-radius: 6px;
    border: 2px solid #3a3a3c;
}

QScrollBar::handle:horizontal:hover {
    background: #888;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}


"""



        table_style= f"""
QTableWidget {{
    background-color: #1e1e1e;
    color: #ffffff;
    gridline-color: #3a3a3a;
    font-size: {17+fontsize}px;
    border: 1px solid #333;
    selection-background-color: #3a81c3;
    selection-color: white;
}}
QTableCornerButton::section {{
    background-color: #2c2c2c;  /* Match your header color */
    border: 1px solid #444;
    font-size: {14+fontsize}px;
}}
QHeaderView::section {{
    background-color: #2c2c2c;
    color:#fcba03;
    padding: 6px;
    border: 1px solid #444;
    font-weight: bold;
    font-size: {14+fontsize}px;
}}
QTableWidget::item:hover {{
    background-color: #2a2a2a;
    color:#ffffff;
}}

"""
        self.setStyleSheet(scroll_style)




        self.layout = QVBoxLayout(self)



        self.addcustomer = QPushButton("+")
        self.addcustomer.setStyleSheet(f"""
            background:green;
            border: 15px soild green;
            border-radius:25%;
            font: 75 {34+fontsize}pt "Microsoft Tai Le";
            """)
        self.addcustomer.setFixedSize(50,50)
        self.addcustomer.clicked.connect(self.addframe)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setContentsMargins(0, 0, 0, 0)




        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.scroll)
        


        # self.scroll.setSpacing(0)

        
        self.scroll_content = QWidget()
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        # tableformat =tableformat()

        # print(len(tableformat.columns))
        self.table = QTableWidget(0, len(tableformat.columns))
        self.table.setStyleSheet(table_style)
        self.table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # self.table.setHorizontalHeaderLabels(["Name", "nakshatram ", "poojas","price"," "])
        # print(tableformat.columns)
        self.table.setHorizontalHeaderLabels(tableformat.columns)
        # self.table.setHorizontalHeaderLabels()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 16) 



        self.scroll.setWidget(self.scroll_content)
        self.scroll_layout.addWidget(self.table)
        # self.scroll_layout.addWidget()
        self.TC = QLabel("Total:0$")
        self.TC.setStyleSheet("font-size:15px;color:white")
        # self.scroll_layout.addItem(self.spacer)
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.frame = QFrame()
        self.frame_layout = QHBoxLayout()
        self.frame.setLayout(self.frame_layout)
        self.frame_layout.addWidget(self.addcustomer)
        self.frame_layout.addItem(self.spacer)
        self.frame_layout.addWidget(self.TC)
        self.scroll_layout.addWidget(self.frame)
    def addframe(self):
        row_index = self.table.rowCount()

        self.table.insertRow(row_index)
        line_edit = QLineEdit()
        # line_edit.setLayoutDirection(Qt.RightToLeft)
        # line_edit.setAlignment(Qt.AlignRight)
        line_edit.setStyleSheet("""
            color:#ffffff;
            """)
        line_edit.setPlaceholderText("Name")
        combo = QComboBox()
        combo.setStyleSheet("""
            color:#ffffff;
            font-size:20px""")
        combo.addItems(["--"]+[x for x in tableformat.nakshatram_m])
        check_box = QCheckBox()
        check_box.setStyleSheet("""
            color:#ffffff;
            """)
        combo_1 = QComboBox()
        combo_1.setStyleSheet("""
            color:#ffffff;
            """)
        combo_1.addItems(["---"]+[x for x in tableformat.tabledata["poojas"].keys()])
        combo_1.currentTextChanged.connect(self.on_dropdown_change)
        check_box.setChecked(True)
        delete = QPushButton()
        delete.setIcon(QIcon("img/delete.png"))
        delete.setStyleSheet("""
            border:none""")
        self.p = QTableWidgetItem("0"+"$")
        self.p.setTextAlignment(Qt.AlignRight)
        self.p.setFlags(self.p.flags() & ~Qt.ItemIsEditable)
        # self.p.setFont(QtGui.)


        # self.p = QLabel("0$")
        # self.p.setStyleSheet("font-size:15self.px;color:white")
        delete.clicked.connect(self.delete_selected_row)
        self.table.setCellWidget(row_index, 0, line_edit)
        self.table.setCellWidget(row_index, 1, combo)
        self.table.setCellWidget(row_index, 2, combo_1)
        self.table.setItem(row_index, 3, self.p)
        self.table.setCellWidget(row_index, 4, delete)
        self.updateTotal()

    def on_dropdown_change(self, text):
        t =tableformat.tabledata["poojas"][text]
        self.p.setText(f"{t}")
        # print("Dropdown changed to:", text)
        # frame = QFrame()
        # frame.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Fixed)
        # frame.setMinimumHeight(50)
        # frame.setStyleSheet("background: red; border: 1px solid black;")
        # self.scroll_layout.addWidget(frame)
        # self.scroll_layout.removeItem(self.spacer)
        # self.spacer = None
        # self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.scroll_layout.addItem(self.spacer)
    def updateTotal(self):
        row = self.table.rowCount()
        print(row)
        s = 0
        for x in range(row):
            t = self.table.item(x, 3)
            print()
            
            t_ = t.text()
            print(t_[:-1])
            s+=int(t_[:-1])
        self.TC.setText("Total: "+str(s)+"$")
                
        
       
    def delete_selected_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
class DateEditPopup(QDialog):
    date_post = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Date")
        self.resize(250, 120)

        layout = QVBoxLayout()

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.show_selected_date)
        self.show()
        layout.addWidget(QLabel("Choose a date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def show_selected_date(self):
        date = self.date_edit.date()
        date_str = date.toString("dd MMMM yyyy")
        QMessageBox.information(self, "Selected Date", f"You chose: {date_str}")
        self.date_post.emit(date_str)
        self.accept()





class gui_Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("app.ui", self)
        self.show()
        self.setWindowTitle("PROJECT SURYA")
        # print(is_dark_theme())
        self.ADDTAB.clicked.connect(self.getdate_)
        # self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tableformatGUI = tableformatGUI()
        self.TableFormater.clicked.connect(self.tableformatGUI.show)


    def close_tab(self, index):
        self.tabWidget.removeTab(index)

    def getdate_(self):
        self.getdate =DateEditPopup()

        self.getdate.date_post.connect(self.addnewtab)
    def addnewtab(self,date):
        tab = TabM()

        # self.getdate.show_selected_date()
        # self.getdate.show()
        print(date)
        self.tabWidget.addTab(tab, date)

if __name__ == "__main__":
    MainApp = QtWidgets.QApplication(sys.argv)
    App = gui_Window()
    sys.exit(MainApp.exec_())
    app = QApplication(sys.argv)






app.setApplicationName("project SURYA")


window = MainWindow()


app.exec_()