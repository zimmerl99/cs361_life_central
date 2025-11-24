from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QCheckBox, QScrollArea, QFrame, QDateEdit, QTimeEdit, QStackedLayout, QSizePolicy,
    QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QPixmap
import sys
import requests


class LifeCentral(QWidget):
    def __init__(self):
        # setup the window
        super().__init__()
        self.setWindowTitle("LIFE CENTRAL")
        self.setGeometry(200, 200, 900, 500)
        self.setStyleSheet("""QWidget { background-color: #b3d9ff;} 
                              QToolTip {background-color: #ffe1c2; color: black; font-size: 12px; }""")

        # allows for both pages on top of each other
        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        # build both pages
        self.home_page = self.build_home_page()
        self.new_life_page = self.build_new_life_page()

        # add pages to stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.new_life_page)

        # start on Home Page
        #self.stack.setCurrentWidget(self.new_life_page)
        self.stack.setCurrentWidget(self.home_page)

        self.lifes = []
        self.quote = None
        self.load_lifes_from_database()
        self.load_inspirational_quote()

    # -----------------------------------------------------------------
    # build the home page
    # -----------------------------------------------------------------
    def build_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(20, 0, 20, 0)

        # build the title
        title = QLabel("LIFE CENTRAL")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet(""" font-size: 40px; font-weight: bold; color: black; """)
        top_bar.addWidget(title)

        # add the color wheel image
        color_wheel = QLabel()
        pixmap = QPixmap("./pinwheel.png")
        pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        color_wheel.setPixmap(pixmap)
        color_wheel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(color_wheel)

        top_bar.addStretch()

        # New life button
        new_life_btn = QPushButton("+ New LIFE")
        new_life_btn.setFixedSize(200, 40)
        new_life_btn.setStyleSheet("""QPushButton {background-color: #ffb7c5; color: black; font-weight: bold;
                                        font-size: 24px; border-radius: 8px; padding: 8px 16px; border: 2px solid black;}
                                      QPushButton:hover { background-color: #cc929d; }""")
        new_life_btn.setToolTip("Press Here to add a new LIFE!")
        new_life_btn.clicked.connect(self.show_new_life_page)
        top_bar.addWidget(new_life_btn)

        layout.addLayout(top_bar)

        # Horizontal Line below the top bar
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setFixedHeight(3)
        h_line.setStyleSheet("background-color: #000000; border: none;")
        layout.addWidget(h_line)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(8, 0, 0, 0)

        # Create a sidebar layout with top alignment
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(0, 8, 0, 0)  # Add some top padding

        # calendar button
        #calendar_btn = QPushButton("Calendar")
        #calendar_btn.setFixedSize(100, 80)
        #calendar_btn.setStyleSheet("""QPushButton {background-color: #cd7ff4; color: black; font-weight: bold;
                                        #font-size: 14px; border-radius: 32px; padding: 2px 2px; border: 2px solid black;}
                                      #QPushButton:hover { background-color: #541e6f; }""")
        #sidebar_layout.addWidget(calendar_btn)

        # Sidebar tip
        sidebar_tip = QLabel("LIFE: Any task, event, meeting, goal, or note you want to keep that makes up your life")
        sidebar_tip.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_tip.setStyleSheet(""" font-size: 20px; font-weight: bold; color: black; """)
        sidebar_tip.setWordWrap(True)
        sidebar_tip.setMaximumWidth(120)
        sidebar_layout.addWidget(sidebar_tip)

        sidebar_layout.addStretch()
        content_layout.addLayout(sidebar_layout)

        # Vertical Line to create the side bar
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFixedWidth(3)
        v_line.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        v_line.setStyleSheet("background-color: #000000; border: none;")
        content_layout.addWidget(v_line)


        # main content area
        self.life_box = QVBoxLayout()
        self.life_box.setContentsMargins(20,10,20,10)

        # title for life list
        life_title = QLabel("LIFEs")
        life_title.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        life_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.life_box.addWidget(life_title)

        # Scroll area for LIFE list
        life_list = QScrollArea()
        life_list.setWidgetResizable(True)
        life_list.setStyleSheet(""" border: 3px solid black; border-radius: 8px; background-color: white; """)
        self.list_content = QFrame()
        self.life_layout = QVBoxLayout(self.list_content)
        self.life_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        life_list.setWidget(self.list_content)
        self.life_box.addWidget(life_list)
        #self.life_box.addStretch()
        content_layout.addLayout(self.life_box)        

        layout.addLayout(content_layout)

        return page

    # -----------------------------------------------------------------
    # Build the new life page
    # -----------------------------------------------------------------
    def build_new_life_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(80,10,80,10)

        # title of the page
        title = QLabel("What's New?")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(""" font-size: 40px; font-weight: bold; color: white; """)
        layout.addWidget(title)

        # label for title of the life
        self.life_title = QLabel("Title: ")
        self.life_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.life_title.setStyleSheet(""" font-size: 20px; font-weight: bold; color: white; """)
        layout.addWidget(self.life_title)

        # title entry box
        self.life_title_entry = QLineEdit()
        self.life_title_entry.setStyleSheet("background: white; color: black;")
        self.life_title_entry.setPlaceholderText("Title of LIFE (e.g. Lunch with Mom)")
        layout.addWidget(self.life_title_entry)

        # label for date
        date_title = QLabel("Date: ")
        date_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        date_title.setStyleSheet(""" font-size: 20px; font-weight: bold; color: white; """)
        layout.addWidget(date_title)

        # date entry
        self.date_entry = QDateEdit()
        self.date_entry.setStyleSheet("background: white; color: black;")
        self.date_entry.setMinimumDate(QDate(2025, 1, 1))
        self.date_entry.setDate(QDate(2025, 1, 1))
        self.date_entry.setCalendarPopup(True)
        self.date_entry.setSpecialValueText("--/--/----")
        
        self.date_entry.setMaximumWidth(100)
        layout.addWidget(self.date_entry)

        # label for time
        time_title = QLabel("Time: ")
        time_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        time_title.setStyleSheet(""" font-size: 20px; font-weight: bold; color: white; """)
        layout.addWidget(time_title)

        #time entry
        self.time_entry = QTimeEdit()
        self.time_entry.setStyleSheet("background: white; color: black;")
        self.time_entry.setTime(QTime(0, 0))
        self.time_entry.setSpecialValueText("--:--")
        self.time_entry.setMaximumWidth(100)
        layout.addWidget(self.time_entry)

        # label for time until
        time_until_title = QLabel("until (optional):")
        time_until_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        time_until_title.setStyleSheet(""" font-size: 13px; font-weight: bold; color: white; """)
        layout.addWidget(time_until_title)

        #until time entry
        self.time_until_entry = QTimeEdit()
        self.time_until_entry.setStyleSheet("background: white; color: black;")
        self.time_until_entry.setTime(QTime(0, 0))  # Set to midnight (minimum)
        self.time_until_entry.setSpecialValueText("--:--")
        self.time_until_entry.setMaximumWidth(100)
        layout.addWidget(self.time_until_entry)

        # color entry
        color_layout = QHBoxLayout()
        colors = ["#FF0000", "#FF7300", "#FFCC00", "#007A00", "#0080FF", "#3700FF", "#9000FF", "#FFA7F8"]
        self.color_buttons = []
        self.selected_color = colors[0]  # Default color

        for color in colors:
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"""
                QPushButton {{background-color: {color}; border: 2px solid black; border-radius: 20px;}}
                QPushButton:hover {{border: 3px solid white;}}
                QPushButton:checked {{border: 4px solid white;}}""")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=color: self.select_color(c))
            self.color_buttons.append(btn)
            color_layout.addWidget(btn)

        self.color_buttons[0].setChecked(True)
        color_layout.addStretch()
        layout.addLayout(color_layout)


        # label for notes
        notes_title = QLabel("Notes: ")
        notes_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        notes_title.setStyleSheet(""" font-size: 20px; font-weight: bold; color: white; """)
        layout.addWidget(notes_title)

        # notes entry box
        self.notes_entry = QTextEdit()
        self.notes_entry.setStyleSheet("background: white; color: black;")
        self.notes_entry.setPlaceholderText("Notes...")
        layout.addWidget(self.notes_entry)

        #back and save button setup
        buttons = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setFixedSize(200, 40)
        back_btn.setStyleSheet("""QPushButton {background-color: #ff3737; color: black; font-weight: bold;
                                        font-size: 24px; border-radius: 4px; padding: 8px 16px; border: 1px solid black;}
                                      QPushButton:hover { background-color: #b00f0f; }""")
        back_btn.clicked.connect(self.show_home_page)
        buttons.addWidget(back_btn)

        save_btn = QPushButton("Save")
        save_btn.setFixedSize(200, 40)
        save_btn.setStyleSheet("""QPushButton {background-color: #00a611; color: black; font-weight: bold;
                                        font-size: 24px; border-radius: 4px; padding: 8px 16px; border: 1px solid black;}
                                      QPushButton:hover { background-color: #3b7f1d; }""")
        save_btn.clicked.connect(self.save_life)
        buttons.addWidget(save_btn)

        layout.addLayout(buttons)

        return page

    # -----------------------------------------------------------------
    # page switch functions
    # -----------------------------------------------------------------
    def show_new_life_page(self):
        self.stack.setCurrentWidget(self.new_life_page)
        return
    def show_home_page(self):
        self.stack.setCurrentWidget(self.home_page)
        self.load_lifes_from_database()
        self.load_inspirational_quote()
        return
    
    # -----------------------------------------------------------------
    # extra functions
    # -----------------------------------------------------------------
    def select_color(self, color):
        self.selected_color = color
        # Uncheck all other buttons
        for btn in self.color_buttons:
            btn.setChecked(False)
        # Check the clicked button
        for btn in self.color_buttons:
            if btn.styleSheet().find(color) != -1:
                btn.setChecked(True)
                break

    def save_life(self):
        import requests
        
        title = self.life_title_entry.text().strip()   # removes whitespace
        if not title:
            return                                    # title is required so it will not save wihtout it

        # convert the entry values to strings
        date = self.date_entry.date().toString("yyyy-MM-dd")        
        time = self.time_entry.time().toString("HH:mm")                 #uses military time atm
        time_until = self.time_until_entry.time().toString("HH:mm")
        
        # colors mapped to a number 1-8
        colors = ["#FF0000", "#FF7300", "#FFCC00", "#007A00", "#0080FF", "#3700FF", "#9000FF", "#FFA7F8"]
        if self.selected_color in colors:
            color_num = colors.index(self.selected_color) + 1               # plus 1 cause its an index
        else:
            color_num = 1                                               # defaults to red
        
        # Prepare data to send to API
        life_data = {
            "title": title,                                                 #required
            "date": date if date != "2025-01-01" else None,                 #optional
            "time": time if time != "00:00" else None,                      #optional
            "time_till": time_until if time_until != "00:00" else None,     #optional
            "color": color_num                                              #autoselected so has to be 1 (of 8)
        }
        
        try:
            # send POST request
            response = requests.post("http://127.0.0.1:8000/lifes", json=life_data)
            
            # if success reload all lifes from database
            if response.status_code == 200:
                self.load_lifes_from_database()
            else:
                print("Error saving life to database")
        
        except Exception:
            print("Error connecting to API:")
        
        # Clear fields and return to home
        self.life_title_entry.clear()
        self.notes_entry.clear()
        self.date_entry.setDate(QDate(2025, 1, 1))
        self.time_entry.setTime(QTime(0, 0))
        self.time_until_entry.setTime(QTime(0, 0))
        self.show_home_page()

    def load_lifes_from_database(self):
        
        try:
            # GET REQUEST all lifes from database
            response = requests.get("http://127.0.0.1:8000/lifes")
            
            if response.status_code == 200:
                data = response.json()
                
                # Clear existing lifes from display
                for i in reversed(range(self.life_layout.count())):         # for every layout
                    layout_item = self.life_layout.itemAt(i)                # get the item at that layout
                    
                    if layout_item.layout():  # It's a QHBoxLayout
                        inner_layout = layout_item.layout()
                        for j in reversed(range(inner_layout.count())):
                            inner_layout.itemAt(j).widget().setParent(None)
                        # Remove the layout itself
                        self.life_layout.removeItem(layout_item)

                self.lifes = []
                date_strings = []

                for life in data['data']:
                    if life.get('date'):                    # get the date of any life
                        date_strings.append(life['date'])

                # Sort the dates if there are any
                if date_strings:
                    sort_request = {"dates": date_strings}
                    #request the date sorting api
                    sort_response = requests.post("http://127.0.0.1:8002/dates", json=sort_request)
                    
                    if sort_response.status_code == 200:
                        sorted_data = sort_response.json()
                        sorted_dates = sorted_data['sorted_dates']
                        
                        # Create a mapping of dates to life objects
                        date_to_life = {life['date']: life for life in data['data'] if life.get('date')}
                        
                        # Display lifes in sorted order
                        for date in sorted_dates:
                            if date in date_to_life:
                                self.display_life(date_to_life[date])
                        
                        # Display lifes without dates at the end
                        for life in data['data']:
                            if not life.get('date'):
                                self.display_life(life)
                    else:
                        print(f"Error: Status code {sort_response.status_code}")
                else:
                    # No dates to sort, just display all lifes
                    for life in data['data']:
                        self.display_life(life)
            
        except Exception:
            print("Error loading lifes")

    def load_inspirational_quote(self):
        if self.quote is not None:
            self.quote.setParent(None)
            self.quote = None

        try:
            # GET REQUEST a quote
            response = requests.get("http://127.0.0.1:8001/quotes")
            
            if response.status_code == 200:
                data = response.json()
                quote_string = data['data']

                # title for life list
                self.quote = QLabel(quote_string)
                self.quote.setStyleSheet("font-size: 24px; font-weight: italic; color: black;")
                self.quote.setAlignment(Qt.AlignmentFlag.AlignRight)
                self.quote.setWordWrap(True)
                self.life_box.addWidget(self.quote)

        except Exception:
            print("Error loading quote")


    def display_life(self, life):
        life_id = life['life_id']
        title = life['title']
        date = life.get('date', '')             #returns a default null value if date doesnt exist
        time = life.get('time', '')
        time_till = life.get('time_till', '')
        color_num = life.get('color', 1)            #default red
        
        # Map color number back to hex
        colors = ["#FF0000", "#FF7300", "#FFCC00", "#007A00", "#0080FF", "#3700FF", "#9000FF", "#FFA7F8"]
        if 1 <= color_num <= 8:
            color = colors[color_num - 1]
        else:
            colors[0]
        
        # build display text
        display_text = title
        if date:
            display_text += f" — {date}"
        if time and time_till:
            display_text += f" @ {time} to {time_till}"
        elif time:
            display_text += f" @ {time}"
        elif time_till:
            display_text += f" until {time_till}"

        item_row = QHBoxLayout()
        
        checkbox = QCheckBox(display_text)                  #remove border and outline to bring back black boxes
        checkbox.setStyleSheet(f"""
            QCheckBox {{font-size: 18px; color: {color}; padding: 5px; spacing: 10px; font-weight: bold; border: none; outline: none;}}
            QCheckBox::indicator {{ width: 20px; height: 20px; border: 2px solid black; background-color: white;}}
            QCheckBox::indicator:checked {{background-color: {color};border: 2px solid black;}}""")
        item_row.addWidget(checkbox)

        # Create delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedSize(40, 20)
        delete_btn.setStyleSheet("""QPushButton {background-color: #ff4444; color: white; font-weight: bold; font-size: 8px;
                                    border-radius: 4px; border: 1px red;}
                                    QPushButton:hover {background-color: #cc0000;}""")
        
        def delete_this_life():
            reply = QMessageBox.question(
                self, "Confirm Deletion", f"Are you sure you want to delete '{title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    response = requests.delete(f"http://127.0.0.1:8000/lifes/{life_id}")
                    if response.status_code == 200:
                        self.load_lifes_from_database()
                    else:
                        print(f"Error deleting item with id {life_id}")
                except Exception:
                    print(f"Error in deletion")
        delete_btn.clicked.connect(delete_this_life)

        item_row.addWidget(delete_btn)
        self.life_layout.addLayout(item_row)
        self.lifes.append(checkbox)        
    

# -----------------------------------------------------------------
# enter app
# -----------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LifeCentral()
    window.show()
    sys.exit(app.exec())
