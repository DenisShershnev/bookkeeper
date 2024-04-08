import bookkeeper.view.view as view
import bookkeeper.presenter as presenter
import sys
from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository

from datetime import datetime, timedelta, date, time

exp_repo = SQLiteRepository[Expense]('bookkeeper.db', Expense)
cat_repo = SQLiteRepository[Category]('bookkeeper.db', Category)
budget_repo = SQLiteRepository[Budget]('bookkeeper.db', Budget)

app = QtWidgets.QApplication(sys.argv)
window = presenter.MainWindow([1000, 500], 'app', exp_repo, cat_repo, budget_repo)
window.show()
sys.exit(app.exec())
