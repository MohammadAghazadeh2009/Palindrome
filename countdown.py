import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpinBox, QSizePolicy
)
from PySide6.QtCore import QTimer, QTime, Qt

class CountdownTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تایمر معکوس")
        self.setGeometry(200, 200, 400, 300) 
        self.total_seconds = 60 
        self.remaining_seconds = self.total_seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()
        self.update_display()

    def init_ui(self):
        layout = QVBoxLayout()

        
        self.welcome_label = QLabel("Welcome!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; color: #555; margin-bottom: 20px;")
        layout.addWidget(self.welcome_label)

        
        self.time_label = QLabel("01:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 60px; color: #007bff; font-weight: bold;")
        layout.addWidget(self.time_label)

        
        time_setting_layout = QHBoxLayout()
        time_setting_layout.addStretch() 

        self.hour_spinbox = QSpinBox()
        self.hour_spinbox.setRange(0, 23)
        self.hour_spinbox.setSuffix(" H")
        self.hour_spinbox.setStyleSheet("font-size: 16px; padding: 5px;")
        self.hour_spinbox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.hour_spinbox.valueChanged.connect(self.set_time_from_spinboxes)

        self.minute_spinbox = QSpinBox()
        self.minute_spinbox.setRange(0, 59)
        self.minute_spinbox.setSuffix(" M")
        self.minute_spinbox.setStyleSheet("font-size: 16px; padding: 5px;")
        self.minute_spinbox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.minute_spinbox.valueChanged.connect(self.set_time_from_spinboxes)

        self.second_spinbox = QSpinBox()
        self.second_spinbox.setRange(0, 59)
        self.second_spinbox.setSuffix(" S")
        self.second_spinbox.setStyleSheet("font-size: 16px; padding: 5px;")
        self.second_spinbox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.second_spinbox.valueChanged.connect(self.set_time_from_spinboxes)

        time_setting_layout.addWidget(self.hour_spinbox)
        time_setting_layout.addWidget(self.minute_spinbox)
        time_setting_layout.addWidget(self.second_spinbox)
        time_setting_layout.addStretch() 
        layout.addLayout(time_setting_layout)

        
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setStyleSheet("padding: 15px 30px; font-size: 18px; background-color: #28a745; color: white; border-radius: 5px;")

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setStyleSheet("padding: 15px 30px; font-size: 18px; background-color: #dc3545; color: white; border-radius: 5px;")
        self.stop_button.setEnabled(False) 

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_display(self):
        
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_string)

        
        self.hour_spinbox.setValue(self.remaining_seconds // 3600)
        self.minute_spinbox.setValue((self.remaining_seconds % 3600) // 60)
        self.second_spinbox.setValue(self.remaining_seconds % 60)

    def set_time_from_spinboxes(self):
        h = self.hour_spinbox.value()
        m = self.minute_spinbox.value()
        s = self.second_spinbox.value()
        self.remaining_seconds = h * 3600 + m * 60 + s
        self.update_display() 

    def start_timer(self):
        if self.remaining_seconds <= 0:
            return

        self.timer.start(1000) 
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        self.hour_spinbox.setEnabled(False)
        self.minute_spinbox.setEnabled(False)
        self.second_spinbox.setEnabled(False)

    def stop_timer(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        self.hour_spinbox.setEnabled(True)
        self.minute_spinbox.setEnabled(True)
        self.second_spinbox.setEnabled(True)


    def update_timer(self):
        self.remaining_seconds -= 1
        self.update_display()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.time_label.setStyleSheet("font-size: 60px; color: #dc3545; font-weight: bold;")
            print("Time's up!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownTimerApp()
    window.show()
    sys.exit(app.exec())
