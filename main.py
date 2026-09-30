import sys
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout



# EINSTELLUNGEN

MONITOR_INDEX = 0       # 0 = linker/erster, 1 = zweiter Monitor
TRIGGER_MINUTE = 20     # Jede Stunde bei xx:20
ANZEIGE_DAUER = 15      # Sekunden



# ERINNERUNGS-GUI

class Reminder(QWidget):

    def __init__(self, screen):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setGeometry(screen.geometry())

        self.setStyleSheet("""
            QWidget {
                background-color: #1A1A1E;
                color: #F1C40F;
            }

            QLabel {
                font-size: 50px;
                font-weight: bold;
            }
        """)

        text = QLabel(
            "‼️ JOB-LIMIT ERINNERUNG ‼️\n\n"
            "Shadow, mach dein Limit, yallah!\n"
            "Liebe Grüße, dein imaginärer Tino."
        )

        text.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(text)

        self.setLayout(layout)

        # Nach X Sekunden automatisch schließen
        QTimer.singleShot(
            ANZEIGE_DAUER * 1000,
            self.close
        )


# ZEITPRÜFUNG

class App:

    def __init__(self, app):

        self.app = app
        self.reminder = None
        self.last_trigger = None

        screens = app.screens()

        if MONITOR_INDEX >= len(screens):
            print("Der ausgewählte Monitor wurde nicht gefunden.")
            sys.exit()

        self.screen = screens[MONITOR_INDEX]

        # Jede Sekunde prüfen
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)

    def check_time(self):

        now = datetime.now()

        # Beispiel: 2026-09-26-19
        current_hour = now.strftime("%Y-%m-%d-%H")

        if now.minute == TRIGGER_MINUTE:

            # Nur einmal pro Stunde
            if self.last_trigger != current_hour:

                self.last_trigger = current_hour

                self.reminder = Reminder(self.screen)

                self.reminder.showFullScreen()
                self.reminder.raise_()
                self.reminder.activateWindow()



# START

app = QApplication(sys.argv)
program = App(app)

print("========================================")
print(" GommeHD Job-Limit Erinnerung V1")
print(" Erfolgreich gestartet!")
print(f" Erinnerung: Jede Stunde bei xx:{TRIGGER_MINUTE:02d}")
print(f" Monitor: {MONITOR_INDEX}")
print("========================================")

sys.exit(app.exec())

# Code is AI-generated but proved as safe from ShadowDev09
# Copyright (c) 2026 ShadowDev09