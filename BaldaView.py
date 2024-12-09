import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsTextItem, QMessageBox, QPushButton, QVBoxLayout, QLabel, QWidget, QGraphicsObject
)
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

from BaldaModel import BaldaModel


class BaldaCell(QGraphicsObject):
    cellClicked = pyqtSignal(int, int)

    def __init__(self, x, y, rect_x, rect_y, width, height, parent=None):
        super().__init__(parent)
        self.column = x
        self.row = y
        self.rect = QRectF(rect_x, rect_y, width, height)
        self.brush = QBrush(QColor("white"))
        self.pen_color = QColor("black")

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen_color)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        self.cellClicked.emit(self.column, self.row)
        super().mousePressEvent(event)


class BaldaSceneView(QGraphicsView):
    def __init__(self, model, update_status_callback):
        super().__init__()
        self.model = model
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.update_status_callback = update_status_callback
        self.init_ui()
        self.editing_text_item = None

    def init_ui(self):
        self.setFixedSize(502, 502)
        self.scene.setSceneRect(0, 0, 500, 500)

        self.cells = []
        for y in range(self.model.size):
            row = []
            for x in range(self.model.size):
                cell = BaldaCell(x, y, x * 100, y * 100, 100, 100)
                cell.cellClicked.connect(self.handle_cell_click)
                self.scene.addItem(cell)

                text_item = QGraphicsTextItem(self.model.grid[y][x])
                text_item.setDefaultTextColor(Qt.black)
                text_item.setPos(x * 100 + 40, y * 100 + 40)
                if self.model.grid[y][x]:
                    text_item.setPlainText(self.model.grid[y][x])
                else:
                    text_item.setTextInteractionFlags(Qt.NoTextInteraction)
                self.scene.addItem(text_item)

                row.append((cell, text_item))
            self.cells.append(row)

    def handle_cell_click(self, x, y):
        if self.model.grid[y][x] == "":
            self.start_text_editing(x, y)
        else:
            QMessageBox.warning(self, "Ошибка", "Эта клетка уже занята.")

    def start_text_editing(self, x, y):
        cell, text_item = self.cells[y][x]
        if self.editing_text_item:
            self.finish_text_editing()
            return

        text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        text_item.setFocus()
        self.editing_text_item = (x, y, text_item)

    def finish_text_editing(self):
        if not self.editing_text_item:
            return

        x, y, text_item = self.editing_text_item
        letter = text_item.toPlainText().strip().upper()

        if len(letter) != 1 or not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод! Введите одну букву.")
            text_item.setPlainText("")
        else:
            success = self.model.add_letter(y, x, letter)
            if not success:
                QMessageBox.warning(self, "Ошибка", f"Невозможно добавить букву '{letter}' в позицию ({y+1}, {x+1}).")
                text_item.setPlainText("")
            else:
                text_item.setPlainText(letter)
                self.update_status_callback()

        text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.editing_text_item = None

    def refresh_board(self):
        self.scene.clear()
        self.init_ui()


class BaldaGame(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Балда")
        self.scene_view = BaldaSceneView(self.model, self.update_status)

        self.status_label = QLabel(f"Текущий игрок: {self.model.get_current_player()}")
        self.pass_button = QPushButton("Пас")
        self.pass_button.clicked.connect(self.pass_turn)

        self.reset_button = QPushButton("Сбросить игру")
        self.reset_button.clicked.connect(self.reset_game)

        layout = QVBoxLayout()
        layout.addWidget(self.scene_view)
        layout.addWidget(self.status_label)
        layout.addWidget(self.pass_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def pass_turn(self):
        self.model.pass_turn()
        self.scene_view.refresh_board()
        self.update_status()
        if self.model.is_game_over():
            QMessageBox.information(self, "Игра окончена", "Игра завершена после двух пасов.")
            self.close()

    def reset_game(self):
        self.model.reset_game()
        self.scene_view.refresh_board()
        self.update_status()

    def update_status(self):
        self.status_label.setText(f"Текущий игрок: {self.model.get_current_player()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = BaldaModel()  # Assume your model is implemented elsewhere
    game = BaldaGame(model)
    game.show()
    sys.exit(app.exec_())
