from PySide6.QtWidgets import QMessageBox

def show_message(container, title, message):
    return QMessageBox.information(container, title, message)

def error_message(container, message):
    return QMessageBox.information(container, 'ERRO', message)