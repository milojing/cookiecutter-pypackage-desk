# -*- coding: utf-8 -*-
import sys

from PySide import QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_ui()

    def setup_ui(self):

        self.button = QtGui.QPushButton('Begin coding! Have fun!', self)
        self.button.clicked.connect(
            lambda: sys.stdout.write(
                "Start coding for {{cookiecutter.repo_name}}!\n"))
        self.setCentralWidget(self.button)
        self.create_menus()
        self.resize(400, 200)
        self.setWindowTitle('{{cookiecutter.repo_name}}')
        self.center()
        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def about(self):
        QtGui.QMessageBox.about(
            self, "About {{cookiecutter.repo_name}}",
            "The <b>{{cookiecutter.repo_name}}</b> example is a start example "
            "create by cookiecutter template of Milo with modern GUI"
            "applications using Qt. Its purpose is just to show how to create"
            "a pyside GUI application with template. Feel free to change it!")

    def create_menus(self):
        self.menuBar().addSeparator()

        self.help_menu = self.menuBar().addMenu("&Help")
        about = QtGui.QAction("&About", self,
                              statusTip="Show the application's About box",
                              triggered=self.about)
        self.help_menu.addAction(about)


def main():
    """The very first basic pyside main function. Feel free to change it.
    """
    app = QtGui.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
