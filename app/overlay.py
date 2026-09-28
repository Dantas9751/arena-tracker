from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizeGrip, QVBoxLayout, QWidget


class AppSignals(QObject):
    show_overlay = pyqtSignal()
    hide_overlay = pyqtSignal()
    update_items = pyqtSignal(set)


class ArenaOverlay(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

        self.signals.show_overlay.connect(self.show)
        self.signals.hide_overlay.connect(self.hide)
        self.signals.update_items.connect(self.update_seen_items)

        self.old_pos = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(50, 50, 320, 250)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 23, 42, 0.90);
                border: 2px solid #38bdf8;
                border-radius: 10px;
            }
        """)
        container_layout = QVBoxLayout(self.container)

        title = QLabel("PRISMÁTICOS JÁ VISTOS")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #38bdf8; padding-bottom: 5px; border: none;")

        self.label_items = QLabel("- (Nenhum item visto ainda)")
        self.label_items.setFont(QFont("Arial", 10))
        self.label_items.setStyleSheet("color: #f8fafc; border: none;")
        self.label_items.setAlignment(Qt.AlignmentFlag.AlignTop)

        container_layout.addWidget(title)
        container_layout.addWidget(self.label_items)
        container_layout.addStretch()

        grip_layout = QHBoxLayout()
        grip_layout.setContentsMargins(0, 0, 0, 0)
        grip_layout.addStretch()

        size_grip = QSizeGrip(self.container)
        size_grip.setStyleSheet("background-color: transparent; border: none;")
        grip_layout.addWidget(size_grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        container_layout.addLayout(grip_layout)
        main_layout.addWidget(self.container)

        self.hide()

    def update_seen_items(self, items_set):
        if not items_set:
            self.label_items.setText("- (Nenhum item visto ainda)")
            return

        formatted_list = "\n".join([f"• {item}" for item in sorted(items_set)])
        self.label_items.setText(formatted_list)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
