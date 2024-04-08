from abc import abstractmethod
from PySide6 import QtWidgets
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from datetime import datetime


def error_message(name, text):
    err = QtWidgets.QDialog()
    err.setWindowTitle(name)
    err.resize(200, 50)
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(QtWidgets.QLabel(text))
    err.setLayout(layout)
    err.exec()


class CategoriesTree(QtWidgets.QTreeWidget):
    def __init__(self, id_list, *args, **kwargs):
        self.id_list = id_list
        super().__init__(*args, **kwargs)


class ExpenseTable(QtWidgets.QTableWidget):
    def __init__(self, cols, rows_number, id_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_list = id_list
        self.setColumnCount(len(cols))
        self.selected_row = 0
        self.setRowCount(rows_number)
        self.setHorizontalHeaderLabels(cols)
        self.vbox = QtWidgets.QVBoxLayout()
        self.header = self.horizontalHeader()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(len(cols)):
            self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().hide()


class BudgetMenu(QtWidgets.QWidget):
    categories_tree: CategoriesTree
    cat_repo: SQLiteRepository[Category]
    budget_repo: SQLiteRepository[Budget]
    exp_repo: SQLiteRepository[Expense]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.cat_repo = cat_repo
        # self.categories_tree = fill_categories_tree(cat_repo)
        self.categories_tree.setHeaderLabels(['category'])
        self.categories_tree.itemClicked.connect(self.count_total)
        self.selected_cat_id = 0
        self.budget_table1 = QtWidgets.QTableWidget()
        self.budget_table1.setColumnCount(1)
        self.budget_table1.setRowCount(3)
        self.budget_table1.setHorizontalHeaderLabels(['total'])
        self.budget_table1.setVerticalHeaderLabels(['day', 'week', 'month'])
        self.budget_table1.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.budget_table1.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.budget_table1.verticalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.budget_table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.budget_table1.setItem(0, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table1.setItem(1, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table1.setItem(2, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table2 = QtWidgets.QTableWidget()
        self.budget_table2.setColumnCount(1)
        self.budget_table2.setRowCount(3)
        self.budget_table2.setHorizontalHeaderLabels(['budget'])
        self.budget_table2.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.budget_table2.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.budget_table2.verticalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.budget_table2.setItem(0, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table2.setItem(1, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table2.setItem(2, 0, QtWidgets.QTableWidgetItem('0'))
        self.budget_table2.verticalHeader().hide()
        self.budget_table2.cellChanged.connect(
            self.change_budget)  # (ПЕРЕДЕЛАТЬ!!!)подавать сигнал при вводе суммы в таблицу бюджета
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.budget_table1)
        self.hbox.addWidget(self.budget_table2)
        self.hbox.addWidget(self.categories_tree)
        self.setLayout(self.hbox)

    @abstractmethod
    def count_total(self, val):
        """
        подсчитать суммы за периоды с помощью метода категорий get_last_children
        """

    @abstractmethod
    def change_budget(self, val):
        """
        получить новое значение бюджета
        """


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, name, text='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(name)
        self.input = QtWidgets.QLineEdit(text)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)


class Buttons(QtWidgets.QWidget):
    def __init__(self, repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_repo = repo
        self.selected_item_id = 0
        self.edit_expenses_button = QtWidgets.QPushButton('edit expenses')
        self.edit_cats_button = QtWidgets.QPushButton('edit categories')
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.edit_cats_button)
        self.vbox.addWidget(self.edit_expenses_button)
        self.setLayout(self.vbox)


class MainWindow(QtWidgets.QWidget):
    expense_table: ExpenseTable
    budget_menu: BudgetMenu
    buttons: Buttons

    def __init__(self, size, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(name)
        self.resize(size[0], size[1])
        # self.expense_table = fill_expense_table(exp_repo, cat_repo)
        self.expense_table.itemClicked.connect(self.cell_pressed)
        self.buttons.edit_expenses_button.clicked.connect(self.edit_expenses)
        self.buttons.edit_cats_button.clicked.connect(self.edit_cats)
        # self.budget_menu = Budget_Menu(cat_repo)
        # self.buttons = Buttons(cat_repo)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.expense_table)
        self.layout.addWidget(self.budget_menu)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    @abstractmethod
    def edit_expenses(self):
        """
        редактировать расход
        """

    @abstractmethod
    def edit_cats(self):
        """
        редактировать категории
        """

    @abstractmethod
    def cell_pressed(self, val: QtWidgets.QTableWidgetItem):
        """
        Сохранить id выбранной транзакции в атрибуте selected_item_id класса Buttons
        """


class EditCategories(QtWidgets.QDialog):
    categories_tree: CategoriesTree
    cat_repo: SQLiteRepository[Category]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.categories_tree = fill_categories_tree(repo)
        self.categories_tree.setHeaderLabels(['category'])
        self.add_child_button = QtWidgets.QPushButton('select category to add to')
        self.add_child_button.clicked.connect(self.add_cat_child)
        self.add_new_button = QtWidgets.QPushButton('add new category')
        self.add_new_button.clicked.connect(self.add_cat)
        self.update_button = QtWidgets.QPushButton('select category to update')
        self.update_button.clicked.connect(self.update_cat)
        self.delete_button = QtWidgets.QPushButton('select category to delete')
        self.delete_button.clicked.connect(self.delete_cat)
        self.processing_name = ''
        self.processing_cat_id = 0
        self.categories_tree.itemClicked.connect(self.show_pressed)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.categories_tree)
        self.vbox.addWidget(self.add_new_button)
        self.vbox.addWidget(self.add_child_button)
        self.vbox.addWidget(self.update_button)
        self.vbox.addWidget(self.delete_button)
        self.setLayout(self.vbox)

    def show_pressed(self, val: QtWidgets.QTreeWidgetItem):
        self.processing_name = val.text(0)
        self.processing_cat_id = self.cat_repo.get_all({'name': self.processing_name})[0].pk
        self.delete_button.setText(f"delete '{self.processing_name}'")
        self.update_button.setText(f"update '{self.processing_name}'")
        self.add_child_button.setText(f"add subcategory to '{self.processing_name}'")

    @abstractmethod
    def add_cat_child(self):
        """
        октрыть меню добавления подкатегорий
        """

    @abstractmethod
    def add_cat(self):
        """
        октрыть меню добавления категорий без родителя
        """

    @abstractmethod
    def update_cat(self):
        """
         октрыть меню обновления категорий
         """

    @abstractmethod
    def delete_cat(self):
        """
         октрыть меню удаления категорий
         """


class AddCat(QtWidgets.QDialog):

    def __init__(self, processing_name, processing_cat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_cat_id = processing_cat_id
        self.processing_name = processing_name
        self.name_text = LabeledInput('category name: ')
        if processing_name != '':
            self.add_button = QtWidgets.QPushButton(f"add to '{processing_name}'")
        else:
            self.add_button = QtWidgets.QPushButton('add')
        self.add_button.clicked.connect(self.add_this_cat)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.name_text)
        self.vbox.addWidget(self.add_button)
        self.setLayout(self.vbox)

    @abstractmethod
    def add_this_cat(self):  # дописать функционал добавления
        """
         добавить категорию
         """


class UpdateCat(QtWidgets.QDialog):

    def __init__(self, processing_name, processing_cat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_name = processing_name
        self.processing_cat_id = processing_cat_id
        self.name_text = LabeledInput('new category name: ')
        self.update_button = QtWidgets.QPushButton(f"update '{processing_name}'")
        self.update_button.clicked.connect(self.update_this_cat)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.name_text)
        self.vbox.addWidget(self.update_button)
        self.setLayout(self.vbox)

    @abstractmethod
    def update_this_cat(self):  # дописать функционал обновления
        """
         обновить категорию
         """


class DeleteCat(QtWidgets.QDialog):

    def __init__(self, processing_cat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_cat_id = processing_cat_id
        self.yes = QtWidgets.QPushButton('yes')
        self.no = QtWidgets.QPushButton('no')
        self.yes.clicked.connect(self.delete_subcategories)
        self.no.clicked.connect(self.save_subcategories)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(QtWidgets.QLabel('Delete subcategories?'))
        self.vbox.addWidget(self.yes)
        self.vbox.addWidget(self.no)
        self.setLayout(self.vbox)

    @abstractmethod
    def delete_subcategories(self):
        """
         удалить категорию вместе с подкатегориями
         """

    @abstractmethod
    def save_subcategories(self):
        """
         удалить категорию, но сохранить подкатегории
         """


class EditExpenses(QtWidgets.QDialog):
    cat_repo: SQLiteRepository[Category]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_item_id = 0

        self.add_button = QtWidgets.QPushButton('add new expense')
        self.add_button.clicked.connect(self.add_expense)
        self.update_button = QtWidgets.QPushButton('update selected expense')
        self.update_button.clicked.connect(self.update_expense)
        self.delete_button = QtWidgets.QPushButton('delete selected expense')
        self.delete_button.clicked.connect(self.delete_expense)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.add_button)
        self.vbox.addWidget(self.update_button)
        self.vbox.addWidget(self.delete_button)
        self.setLayout(self.vbox)

    @abstractmethod
    def add_expense(self):
        """
        октрыть меню добавления расхода
        """

    @abstractmethod
    def update_expense(self):
        """
        октрыть меню обновления расхода
        """

    @abstractmethod
    def delete_expense(self):
        """
        удалить расход
        """


class AddExpense(QtWidgets.QDialog):
    categories_tree: CategoriesTree

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.categories_tree = fill_categories_tree(repo)
        self.selected_category = 0
        self.categories_tree.setHeaderLabels(['category'])
        self.categories_tree.itemClicked.connect(self.select_category)
        self.amount_text = LabeledInput('amount: ')
        self.date_text = LabeledInput('date: ')
        self.comment_text = LabeledInput('comment: ')
        self.add_button = QtWidgets.QPushButton('add this expense')
        self.add_button.clicked.connect(self.add_this_expense)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.amount_text)
        self.vbox.addWidget(self.date_text)
        self.vbox.addWidget(self.comment_text)
        self.vbox.addWidget(self.categories_tree)
        self.vbox.addWidget(self.add_button)
        self.setLayout(self.vbox)

    def select_category(self, val):
        self.selected_category = int(val.text(1))

    @abstractmethod
    def add_this_expense(self):  # дописать функционал добавления
        self.close()


class UpdateExpense(QtWidgets.QDialog):
    categories_tree: CategoriesTree
    selected_item_id: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.categories_tree = fill_categories_tree(cat_repo)
        self.categories_tree.setHeaderLabels(['category'])
        self.categories_tree.itemClicked.connect(self.select_category)
        self.amount_text = LabeledInput('amount: ')
        self.date_text = LabeledInput('date: ')
        self.comment_text = LabeledInput('comment: ')
        self.update_button = QtWidgets.QPushButton('update this expense')
        self.update_button.clicked.connect(self.update_this_expense)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.amount_text)
        self.vbox.addWidget(self.date_text)
        self.vbox.addWidget(self.comment_text)
        self.vbox.addWidget(self.categories_tree)
        self.vbox.addWidget(self.update_button)
        self.setLayout(self.vbox)

    def select_category(self, val):
        self.selected_category = int(val.text(1))

    @abstractmethod
    def update_this_expense(self):  # дописать функционал обновления
        self.close()
