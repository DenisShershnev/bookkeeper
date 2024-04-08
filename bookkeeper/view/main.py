import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlTableModel

from main_window import Ui_MainWindow
from dialog_window import Ui_Dialog
from connection import Data


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super(ExpenseTracker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = Data()
        self.view_data()
        self.reload_data()

        self.ui.add_expence_button.clicked.connect(self.open_new_transaction_window)
        self.ui.edit_expence_button.clicked.connect(self.open_new_transaction_window)
        self.ui.delete_expence_button.clicked.connect(self.delete_current_transaction)

    def reload_data(self):
        pass
        '''
        self.ui.current_balance.setText(self.conn.total_balance())
        self.ui.income_balance.setText(self.conn.total_income())
        self.ui.outcome_balance.setText(self.conn.total_outcome())
        self.ui.total_groceries.setText(self.conn.total_groceries())
        self.ui.total_auto.setText(self.conn.total_auto())
        self.ui.total_entertainment.setText(self.conn.total_entertainment())
        self.ui.total_other.setText(self.conn.total_other())
        '''

    def view_data(self):
        self.model = QSqlTableModel(self)
        self.model.setTable('expense')
        self.model.select()
        self.ui.table.setModel(self.model)

    def open_new_transaction_window(self):

        self.new_window = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        sender = self.sender()
        if sender.text() == "New transaction":
            self.ui_window.add_expence_button.clicked.connect(self.add_new_transaction)
        else:
            self.ui_window.add_expence_button.clicked.connect(self.edit_current_transaction)

    def add_new_transaction(self):
        date = self.ui_window.date_time.text()
        category = self.ui_window.category.currentText()
        description = self.ui_window.comment.text()
        balance = self.ui_window.summ.text()
        status = self.ui_window.status.currentText()

        self.conn.add_new_transaction_query(date, category, description, balance, status)
        self.view_data()
        self.reload_data()
        self.new_window.close()

    def edit_current_transaction(self):
        index = self.ui.table.selectedIndexes()[0]
        id = str(self.ui.table.model().data(index))

        date = self.ui_window.date_time.text()
        category = self.ui_window.category.currentText()
        description = self.ui_window.comment.text()
        balance = self.ui_window.summ.text()
        status = self.ui_window.status.currentText()

        self.conn.update_transaction_query(date, category, description, balance, status, id)
        self.view_data()
        self.reload_data()
        self.new_window.close()

    def delete_current_transaction(self):
        index = self.ui.table.selectedIndexes()[0]
        id = str(self.ui.table.model().data(index))

        self.conn.delete_transaction_query(id)
        self.view_data()
        self.reload_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()

    sys.exit(app.exec())