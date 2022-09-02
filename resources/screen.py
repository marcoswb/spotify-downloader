from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject
)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget
)

class UiMainWindow(object):

    def setup_ui(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(1092, 594)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.textbox__playlist_link = QLineEdit(self.centralwidget)
        self.textbox__playlist_link.setObjectName(u"textbox__playlist_link")

        self.verticalLayout_7.addWidget(self.textbox__playlist_link)

        self.listview__downloaded_music = QListWidget(self.centralwidget)
        self.listview__downloaded_music.setObjectName(u"listview__downloaded_music")

        self.verticalLayout_7.addWidget(self.listview__downloaded_music)

        self.button__download = QPushButton(self.centralwidget)
        self.button__download.setObjectName(u"button__download")

        self.verticalLayout_7.addWidget(self.button__download)

        self.progressbar__status_download = QProgressBar(self.centralwidget)
        self.progressbar__status_download.setObjectName(u"progressbar__status_download")
        self.progressbar__status_download.setValue(24)

        self.verticalLayout_7.addWidget(self.progressbar__status_download)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslate_ui(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Spotify Downloader", None))
        self.textbox__playlist_link.setPlaceholderText(QCoreApplication.translate("MainWindow", "Informe o link da playlist", None))
        self.button__download.setText(QCoreApplication.translate("MainWindow", u"DOWNLOAD", None))

