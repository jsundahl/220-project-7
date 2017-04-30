""" An example gui that displays reports based on database queries.
    It used classes from PyQt including a model/view pair as well as a database accessor module.
"""
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel)
from PyQt5.QtWidgets import QTableView, QComboBox
from dbaccessor import DBAccessor
import report_model


class ReportExample(QWidget):
    def __init__(self):
        super().__init__()
        self.__db = None

        self.initUI()

    def initUI(self):
        # create the accessor for queries
        self.__db = DBAccessor('test.db')
        # create buttons and their event handler
        allCustBtn = QPushButton('All Customers', self)
        allCustBtn.setCheckable(True)
        allCustBtn.move(10, 10)
        allCustBtn.clicked[bool].connect(self.handleBtn)

        allGenresBtn = QPushButton('Genres', self)
        allGenresBtn.setCheckable(True)
        allGenresBtn.move(10, 60)
        allGenresBtn.clicked[bool].connect(self.handleBtn)

        clearBtn = QPushButton('Clear', self)
        clearBtn.setCheckable(True)
        clearBtn.move(10, 110)
        clearBtn.clicked[bool].connect(self.handleBtn)

        # The label that displays the choice of genres in the database
        self.default_genre = "Metal"
        self.genreLbl = QLabel(self.default_genre, self)
        self.genreLbl.move(200, 60)
        # the layout that contains the table and combo box
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # the table view to display the reports
        self.my_table = QTableView()
        vbox.addWidget(self.my_table)
        # combo box to select genre
        self.combo = QComboBox()
        # load combo with genres
        # TODO: make the calls to run the appropriate query and get the model
        model = report_model.get_table_report(self.__db.all_genres())
        self.combo.setModel(model)
        vbox.addWidget(self.combo)
        self.combo.activated[str].connect(self.onActivated)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Reports')
        self.show()

    def handleBtn(self):

        source = self.sender()

        if source.text() == "All Customers":
            # TODO: make the calls to run the appropriate query and get the model
            model = report_model.get_table_report(self.__db.all_customer_report())
            self.my_table.setModel(model)
            self.my_table.show()

        if source.text() == "Genres":
            # TODO: make the calls to run the appropriate query and get the model
            current_genre = self.combo.currentText()
            model = report_model.get_table_report(self.__db.track_info_by_genre(current_genre))
            self.my_table.setModel(model)
            self.my_table.show()

        elif source.text() == "Clear":
            self.my_table.model().clear()
            self.genreLbl.setText(self.default_genre)
            self.genreLbl.adjustSize()

    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())
