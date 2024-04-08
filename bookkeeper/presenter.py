import bookkeeper.view.view as view
from PySide6 import QtWidgets
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository

from datetime import datetime, timedelta, date, time


def fill_expense_table(exp_repo: SQLiteRepository,
                       cat_repo: SQLiteRepository) -> view.ExpenseTable:
    data = exp_repo.get_all()
    if data == []:
        table = view.ExpenseTable([n for n in exp_repo.fields], 0, [])
        return table
    id_list = []
    c = 0
    while len(id_list) < len(data):
        id_list.append(getattr(data[-1 - c], 'pk'))
        c = c + 1
    table = view.ExpenseTable([n for n in exp_repo.fields], len(data), id_list)
    for i in range(len(data)):
        c = 0
        try:
            cat = cat_repo.get(int(getattr(data[-i - 1], 'category'))).name
        except:
            pass
        else:
            for j in exp_repo.fields:
                if j == 'category':
                    table.setItem(i, c, QtWidgets.QTableWidgetItem(cat))
                else:
                    table.setItem(i, c, QtWidgets.QTableWidgetItem(str(getattr(data[-i - 1], j))))
                c = c + 1
    return table


def fill_categories_tree(repo: SQLiteRepository[Category]) -> view.CategoriesTree:
    cat_list = repo.get_all()
    id_list = []
    c = 0
    while len(id_list) < len(cat_list):
        id_list.append(getattr(cat_list[-1 - c], 'pk'))
        c = c + 1
    cat_tree = view.CategoriesTree(id_list)
    cat_tree_elements = dict()
    cat_dict = Category.tree_from_repo(repo)
    i = 0
    for x in cat_dict:
        if cat_dict[x] is None or cat_dict[x] == '':
            cat_tree_elements[x] = QtWidgets.QTreeWidgetItem(cat_tree,
                                                             [str(getattr(cat_list[i], 'name')), str(id_list[-1 - i])])
        else:
            cat_tree_elements[x] = QtWidgets.QTreeWidgetItem(cat_tree_elements[cat_dict[x]],
                                                             [str(getattr(cat_list[i], 'name')), str(id_list[-1 - i])])
        i = i + 1
    return cat_tree


def fill_budget_table(repo: AbstractRepository[Budget], cat_id: int) -> QtWidgets.QTableWidget:
    data = repo.get_all()
    table = QtWidgets.QTableWidget()
    table.setColumnCount(1)
    table.setRowCount(3)
    if data == []:
        table.setItem(0, 0, QtWidgets.QTableWidgetItem('0'))
        table.setItem(1, 0, QtWidgets.QTableWidgetItem('0'))
        table.setItem(2, 0, QtWidgets.QTableWidgetItem('0'))
        return table

    try:
        [int(getattr(data[i], 'category')) for i in range(len(data))].index(cat_id)
    except:
        table.setItem(0, 0, QtWidgets.QTableWidgetItem('0'))
        table.setItem(1, 0, QtWidgets.QTableWidgetItem('0'))
        table.setItem(2, 0, QtWidgets.QTableWidgetItem('0'))
        return table

    j = [getattr(data[i], 'category') for i in range(len(data))].index(cat_id)
    table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(getattr(data[j], 'summa'))))
    table.setItem(1, 0, QtWidgets.QTableWidgetItem(str(7 * float(getattr(data[j], 'summa')))))
    table.setItem(2, 0, QtWidgets.QTableWidgetItem(str(30 * float(getattr(data[j], 'summa')))))
    return table


def create_total_repo(exp_repo: SQLiteRepository[Expense],
                      cat_repo: SQLiteRepository[Category],
                      time: datetime.date) -> \
                    MemoryRepository[Budget]:
    total_repo = MemoryRepository[Budget]()
    for i in cat_repo.get_all():
        s = 0
        c = [x for x in i.get_subcategories(cat_repo)]
        for j in exp_repo.get_all():
            if (int(i.pk) == int(j.category) or [int(x.pk) for x in c].count(
                    int(j.category)) > 0) and j.expense_date > time:
                s = s + float(j.amount)

        total_repo.add(Budget(int(i.pk), s, datetime.now()))
    return total_repo


def fill_total_table(repos: [AbstractRepository[Budget]], cat_id: int) -> QtWidgets.QTableWidget:
    table = QtWidgets.QTableWidget()
    table.setColumnCount(1)
    table.setRowCount(3)
    for i in range(3):
        data = repos[i].get_all()
        j = [getattr(data[x], 'category') for x in range(len(data))].index(cat_id)
        table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(getattr(data[j], 'summa'))))
    return table


class CategoriesTree(view.CategoriesTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExpenseTable(view.ExpenseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainWindow(view.MainWindow):
    def __init__(self, size, name, exp_repo, cat_repo, budget_repo, *args, **kwargs):
        self.expense_table = fill_expense_table(exp_repo, cat_repo)
        self.budget_menu = BudgetMenu(budget_repo, cat_repo, exp_repo)
        self.buttons = Buttons(self.expense_table, cat_repo)
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        super().__init__(size, name, *args, **kwargs)

    def cell_pressed(self, val: QtWidgets.QTableWidgetItem):
        self.buttons.selected_item_id = self.expense_table.id_list[val.row()]

    def edit_expenses(self):
        self.new_window = EditExpenses(self.buttons.cat_repo, self.exp_repo)
        self.new_window.selected_item_id = self.buttons.selected_item_id
        self.new_window.setWindowTitle('edit expenses')
        self.new_window.resize(200, 100)
        self.new_window.exec()
        self.exp_repo = self.new_window.exp_repo
        new_expense_table = fill_expense_table(self.exp_repo, self.cat_repo)
        self.layout.replaceWidget(self.expense_table, new_expense_table)
        self.expense_table = new_expense_table
        self.expense_table.itemClicked.connect(self.cell_pressed)

    def edit_cats(self):
        self.new_window = EditCategories(self.cat_repo, self.exp_repo, self.budget_menu.budget_repo)
        self.new_window.setWindowTitle('edit categories')
        self.new_window.resize(250, 500)
        self.new_window.exec()
        self.cat_repo = self.new_window.cat_repo
        new_cat_tree = fill_categories_tree(self.cat_repo)
        self.budget_menu.budget_repo = self.new_window.budget_repo
        self.budget_menu.hbox.replaceWidget(self.budget_menu.categories_tree, new_cat_tree)
        self.budget_menu.cat_repo = self.cat_repo
        self.budget_menu.categories_tree = new_cat_tree
        self.budget_menu.categories_tree.setHeaderLabels(['category'])
        self.budget_menu.categories_tree.itemClicked.connect(self.budget_menu.count_total)
        self.exp_repo = self.new_window.exp_repo
        new_expense_table = fill_expense_table(self.exp_repo, self.cat_repo)
        self.layout.replaceWidget(self.expense_table, new_expense_table)
        self.expense_table = new_expense_table
        self.expense_table.itemClicked.connect(self.cell_pressed)


class BudgetMenu(view.BudgetMenu):

    def __init__(self, budget_repo, cat_repo, exp_repo, *args, **kwargs):
        self.categories_tree = fill_categories_tree(cat_repo)
        self.cat_repo = cat_repo
        self.budget_repo = budget_repo
        self.exp_repo = exp_repo
        super().__init__(*args, **kwargs)

    def count_total(self, val):
        self.selected_cat_id = int(val.text(1))
        t = []
        today = datetime.now()
        t.append(
            create_total_repo(self.exp_repo, self.cat_repo, datetime(today.year, today.month, today.day, 0, 0, 0, 0)))
        t.append(create_total_repo(self.exp_repo, self.cat_repo, today - timedelta(today.weekday() + 1)))
        t.append(create_total_repo(self.exp_repo, self.cat_repo,
                                   datetime.combine(date(today.year, today.month, 1) - timedelta(1), time(0, 0, 0, 0))))

        t1 = fill_total_table(t, self.selected_cat_id)
        t2 = fill_budget_table(self.budget_repo, self.selected_cat_id)
        self.budget_table1.item(0, 0).setText(t1.item(0, 0).text())
        self.budget_table1.item(1, 0).setText(t1.item(1, 0).text())
        self.budget_table1.item(2, 0).setText(t1.item(2, 0).text())
        self.budget_table2.item(0, 0).setText(t2.item(0, 0).text())
        self.budget_table2.item(1, 0).setText(t2.item(1, 0).text())
        self.budget_table2.item(2, 0).setText(t2.item(2, 0).text())

    def change_budget(self, val):
        try:
            float(self.budget_table2.item(val, 0).text())
        except:
            self.budget_table2.item(val, 0).setText('0')
            return
        if self.selected_cat_id == 0:
            self.budget_table2.item(0, 0).setText('0')
            self.budget_table2.item(1, 0).setText('0')
            self.budget_table2.item(2, 0).setText('0')
            return
        if float(self.budget_table2.item(val, 0).text()) < 0:
            self.budget_table2.item(0, 0).setText(str(-float(self.budget_table2.item(val, 0).text())))

        blist = self.budget_repo.get_all()
        for i in range(len(blist)):
            if blist[i].category == self.selected_cat_id:
                bnew = blist[i]
                if val == 0:
                    bnew.summa = float(self.budget_table2.item(0, 0).text())
                if val == 1:
                    bnew.summa = float(self.budget_table2.item(1, 0).text()) / 7
                if val == 2:
                    bnew.summa = float(self.budget_table2.item(2, 0).text()) / 30
                self.budget_repo.update(bnew)
                break
        t = fill_budget_table(self.budget_repo, self.selected_cat_id)
        self.budget_table2.item(0, 0).setText(t.item(0, 0).text())
        self.budget_table2.item(1, 0).setText(t.item(1, 0).text())
        self.budget_table2.item(2, 0).setText(t.item(2, 0).text())


class LabeledInput(view.LabeledInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Buttons(view.Buttons):

    def __init__(self, expense_table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expense_table = expense_table


class EditCategories(view.EditCategories):

    def __init__(self, cat_repo, exp_repo, budget_repo, *args, **kwargs):
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.budget_repo = budget_repo
        self.categories_tree = fill_categories_tree(cat_repo)
        super().__init__(*args, **kwargs)

    def add_cat_child(self):
        if self.processing_name == '':
            view.error_message('error', 'No category selected!')
        else:
            self.new_window = AddCat(self.cat_repo, self.budget_repo, self.processing_name, self.processing_cat_id)
            self.new_window.setWindowTitle('add')
            self.new_window.resize(200, 100)
            self.new_window.exec()
            self.cat_repo = self.new_window.cat_repo
            new_categories_tree = fill_categories_tree(self.cat_repo)
            self.vbox.replaceWidget(self.categories_tree, new_categories_tree)
            self.categories_tree = new_categories_tree
            self.categories_tree.setHeaderLabels(['category'])
            self.categories_tree.itemClicked.connect(self.show_pressed)

    def add_cat(self):
        self.new_window = AddCat(self.cat_repo, self.budget_repo, '', 0)
        self.new_window.setWindowTitle('add')
        self.new_window.resize(200, 100)
        self.new_window.exec()
        self.cat_repo = self.new_window.cat_repo
        new_categories_tree = fill_categories_tree(self.cat_repo)
        self.vbox.replaceWidget(self.categories_tree, new_categories_tree)
        self.categories_tree = new_categories_tree
        self.categories_tree.setHeaderLabels(['category'])
        self.categories_tree.itemClicked.connect(self.show_pressed)

    def update_cat(self):
        if self.processing_name == '':
            view.error_message('error', 'No category selected!')
        else:
            self.new_window = UpdateCat(self.cat_repo, self.budget_repo, self.processing_name, self.processing_cat_id)
            self.new_window.setWindowTitle('update')
            self.new_window.resize(200, 100)
            self.new_window.exec()
            new_categories_tree = fill_categories_tree(self.cat_repo)
            self.vbox.replaceWidget(self.categories_tree, new_categories_tree)
            self.categories_tree = new_categories_tree
            self.categories_tree.setHeaderLabels(['category'])
            self.categories_tree.itemClicked.connect(self.show_pressed)

    def delete_cat(self):  # дописать функционал удаления
        if self.processing_name == '':
            view.error_message('error', 'No category selected!')
        else:
            self.new_window = DeleteCat(self.cat_repo, self.exp_repo, self.budget_repo, self.processing_cat_id)
            self.new_window.setWindowTitle('delete')
            self.new_window.resize(200, 50)
            self.new_window.exec()
            self.exp_repo = self.new_window.exp_repo
            new_categories_tree = fill_categories_tree(self.cat_repo)
            self.vbox.replaceWidget(self.categories_tree, new_categories_tree)
            self.categories_tree = new_categories_tree
            self.categories_tree.setHeaderLabels(['category'])
            self.categories_tree.itemClicked.connect(self.show_pressed)


class AddCat(view.AddCat):

    def __init__(self, cat_repo: SQLiteRepository[Category], budget_repo: SQLiteRepository[Budget], *args, **kwargs):
        self.cat_repo = cat_repo
        self.budget_repo = budget_repo
        super().__init__(*args, **kwargs)

    def add_this_cat(self):  # дописать функционал добавления

        if self.cat_repo.get_all({'name': self.name_text.input.text()}) != []:
            view.error_message('name error', 'category with this name already exists!')
            return
        if self.processing_cat_id == 0:
            self.cat_repo.add(Category(self.name_text.input.text(), None))
        else:
            self.cat_repo.add(Category(self.name_text.input.text(), self.processing_cat_id))
        x = self.cat_repo.get_all({'name': self.name_text.input.text()})[0].pk
        self.budget_repo.add(Budget(x, 0, datetime.now()))
        self.close()


class UpdateCat(view.UpdateCat):

    def __init__(self, cat_repo: SQLiteRepository[Category], budget_repo: SQLiteRepository[Budget], *args, **kwargs):
        self.cat_repo = cat_repo
        self.budget_repo = budget_repo
        super().__init__(*args, **kwargs)

    def update_this_cat(self):  # дописать функционал обновления
        if self.cat_repo.get_all({'name': self.name_text.input.text()}) != []:
            view.error_message('name error', 'category with this name already exists!')
            return
        old_cat_parent = getattr(self.cat_repo.get(self.processing_cat_id), 'parent')
        old_cat_id = getattr(self.cat_repo.get(self.processing_cat_id), 'pk')
        self.cat_repo.update(Category(self.name_text.input.text(), old_cat_parent, self.processing_cat_id))
        x = self.budget_repo.get_all({'category': old_cat_id})[0].pk
        self.budget_repo.update(Budget(old_cat_id, self.budget_repo.get(x).summa, datetime.now()))
        self.close()


class DeleteCat(view.DeleteCat):

    def __init__(self, cat_repo: SQLiteRepository[Category], exp_repo: SQLiteRepository[Expense],
                 budget_repo: SQLiteRepository[Budget], *args, **kwargs):
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.budget_repo = budget_repo
        super().__init__(*args, **kwargs)

    def delete_subcategories(self):
        cat_pk = getattr(self.cat_repo.get(self.processing_cat_id), 'pk')
        deleted_cats = self.cat_repo.get(self.processing_cat_id).get_subcategories(self.cat_repo)

        for x in deleted_cats:
            for y in self.exp_repo.get_all({'category': x.pk}):
                self.exp_repo.delete(y.pk)
            z = self.budget_repo.get_all({'category': x.pk})[0].pk
            self.budget_repo.delete(z)
            self.cat_repo.delete(x.pk)
        for x in self.exp_repo.get_all({'category': self.processing_cat_id}):
            self.exp_repo.delete(x.pk)
        z = self.budget_repo.get_all({'category': self.processing_cat_id})[0].pk
        self.budget_repo.delete(z)
        self.cat_repo.delete(self.processing_cat_id)
        self.close()

    def save_subcategories(self):
        cat_pk = getattr(self.cat_repo.get(self.processing_cat_id), 'pk')
        new_id = getattr(self.cat_repo.get(self.processing_cat_id), 'parent')
        saved_cats = self.cat_repo.get_all({'parent': self.processing_cat_id})
        z = self.budget_repo.get_all({'category': self.processing_cat_id})[0].pk
        self.budget_repo.delete(z)
        for x in self.exp_repo.get_all({'category': self.processing_cat_id}):
            self.exp_repo.delete(x.pk)
        self.cat_repo.delete(self.processing_cat_id)
        for x in saved_cats:
            y = x
            y.parent = new_id
            self.cat_repo.update(y)
        self.close()


class EditExpenses(view.EditExpenses):

    def __init__(self, cat_repo, exp_repo, *args, **kwargs):
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        super().__init__(*args, **kwargs)

    def add_expense(self):
        self.new_window = AddExpense(self.cat_repo, self.exp_repo)
        self.new_window.setWindowTitle('add new expense')
        self.new_window.resize(200, 500)
        self.new_window.exec()
        self.exp_repo = self.new_window.exp_repo
        self.close()

    def update_expense(self):
        if self.selected_item_id == 0:
            view.error_message('error', 'No expense selected!')
        else:
            self.new_window = UpdateExpense(self.cat_repo, self.exp_repo, self.selected_item_id)
            self.new_window.setWindowTitle('update selected expense')
            self.new_window.resize(200, 500)
            self.new_window.exec()
            self.exp_repo = self.new_window.exp_repo
            self.close()

    def delete_expense(self):  # дописать функционал удаления
        if self.selected_item_id == 0:
            view.error_message('error', 'No expense selected!')
        else:
            self.exp_repo.delete(self.selected_item_id)
            self.close()


class AddExpense(view.AddExpense):

    def __init__(self, cat_repo, exp_repo, *args, **kwargs):
        self.categories_tree = fill_categories_tree(cat_repo)
        self.exp_repo = exp_repo
        super().__init__(*args, **kwargs)

    def add_this_expense(self):  # дописать функционал добавления
        try:
            amount = float(self.amount_text.input.text())
            if float(self.amount_text.input.text()) <= 0:
                raise ValueError
        except:
            view.error_message('data error', 'amount should be positive float number')
            return

        try:
            date = datetime.strptime(self.date_text.input.text(), '%Y-%m-%d %H:%M:%S')
        except:
            view.error_message('data error', 'date should have format YYYY-MM-DD hh:mm:ss')
            return
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 1)
        comment = self.comment_text.input.text()

        if self.selected_category == 0:
            view.error_message('data error', 'no category selected')
            return
        self.exp_repo.add(Expense(amount, self.selected_category, date, datetime.now(), comment))
        self.close()


class UpdateExpense(view.UpdateExpense):

    def __init__(self, cat_repo, exp_repo, selected_item_id, *args, **kwargs):
        self.categories_tree = fill_categories_tree(cat_repo)
        self.exp_repo = exp_repo
        self.selected_item_id = selected_item_id
        super().__init__(*args, **kwargs)

    def update_this_expense(self):  # дописать функционал обновления
        try:
            amount = float(self.amount_text.input.text())
            if float(self.amount_text.input.text()) <= 0:
                raise ValueError
        except:
            view.error_message('data error', 'amount should be positive float number')
            return

        try:
            date = datetime.strptime(self.date_text.input.text(), '%Y-%m-%d %H:%M:%S')
        except:
            view.error_message('data error', 'date should have format YYYY-MM-DD hh:mm:ss')
            return
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 1)
        comment = self.comment_text.input.text()

        if self.selected_category == 0:
            view.error_message('data error', 'no category selected')
            return
        updated_expense = Expense(amount, self.selected_category, date, datetime.now(), comment, self.selected_item_id)
        self.exp_repo.update(updated_expense)
        self.close()
