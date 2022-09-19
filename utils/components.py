from PySide6.QtWidgets import QMessageBox

def show_message(container, title, message):
    return QMessageBox.information(container, title, message)

def error_message(container, message):
    return QMessageBox.information(container, 'ERRO', message)

def question_message(container, message):
    response = QMessageBox.question(container, 'CONFIRMAR', message)

    if response == QMessageBox.Yes:
        return True
    else:
        return False
