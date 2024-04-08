# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(628, 630)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.global_layout = QVBoxLayout()
        self.global_layout.setObjectName(u"global_layout")
        self.expence_table_layout = QVBoxLayout()
        self.expence_table_layout.setObjectName(u"expence_table_layout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.expence_table_layout.addWidget(self.label)

        self.table = QTableView(self.centralwidget)
        self.table.setObjectName(u"table")

        self.expence_table_layout.addWidget(self.table)


        self.global_layout.addLayout(self.expence_table_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.budget_layout = QVBoxLayout()
        self.budget_layout.setObjectName(u"budget_layout")
        self.budget_label_2 = QLabel(self.centralwidget)
        self.budget_label_2.setObjectName(u"budget_label_2")

        self.budget_layout.addWidget(self.budget_label_2)

        self.budget_table_layout = QHBoxLayout()
        self.budget_table_layout.setObjectName(u"budget_table_layout")
        self.title_layout = QVBoxLayout()
        self.title_layout.setObjectName(u"title_layout")
        self.empty_label = QLabel(self.centralwidget)
        self.empty_label.setObjectName(u"empty_label")

        self.title_layout.addWidget(self.empty_label)

        self.day_3 = QLabel(self.centralwidget)
        self.day_3.setObjectName(u"day_3")

        self.title_layout.addWidget(self.day_3)

        self.week_3 = QLabel(self.centralwidget)
        self.week_3.setObjectName(u"week_3")

        self.title_layout.addWidget(self.week_3)

        self.month_3 = QLabel(self.centralwidget)
        self.month_3.setObjectName(u"month_3")

        self.title_layout.addWidget(self.month_3)


        self.budget_table_layout.addLayout(self.title_layout)

        self.summ = QVBoxLayout()
        self.summ.setObjectName(u"summ")
        self.summ_label = QLabel(self.centralwidget)
        self.summ_label.setObjectName(u"summ_label")

        self.summ.addWidget(self.summ_label)

        self.day_2 = QLabel(self.centralwidget)
        self.day_2.setObjectName(u"day_2")

        self.summ.addWidget(self.day_2)

        self.week_2 = QLabel(self.centralwidget)
        self.week_2.setObjectName(u"week_2")

        self.summ.addWidget(self.week_2)

        self.month_2 = QLabel(self.centralwidget)
        self.month_2.setObjectName(u"month_2")

        self.summ.addWidget(self.month_2)


        self.budget_table_layout.addLayout(self.summ)

        self.budget_layout_2 = QVBoxLayout()
        self.budget_layout_2.setObjectName(u"budget_layout_2")
        self.budget_label = QLabel(self.centralwidget)
        self.budget_label.setObjectName(u"budget_label")

        self.budget_layout_2.addWidget(self.budget_label)

        self.day = QLabel(self.centralwidget)
        self.day.setObjectName(u"day")

        self.budget_layout_2.addWidget(self.day)

        self.week = QLabel(self.centralwidget)
        self.week.setObjectName(u"week")

        self.budget_layout_2.addWidget(self.week)

        self.month = QLabel(self.centralwidget)
        self.month.setObjectName(u"month")

        self.budget_layout_2.addWidget(self.month)


        self.budget_table_layout.addLayout(self.budget_layout_2)


        self.budget_layout.addLayout(self.budget_table_layout)


        self.bottom_layout.addLayout(self.budget_layout)

        self.expence_editor_layout = QVBoxLayout()
        self.expence_editor_layout.setObjectName(u"expence_editor_layout")
        self.expence_editor_label = QLabel(self.centralwidget)
        self.expence_editor_label.setObjectName(u"expence_editor_label")

        self.expence_editor_layout.addWidget(self.expence_editor_label)

        self.add_expence_button = QPushButton(self.centralwidget)
        self.add_expence_button.setObjectName(u"add_expence_button")

        self.expence_editor_layout.addWidget(self.add_expence_button)

        self.edit_expence_button = QPushButton(self.centralwidget)
        self.edit_expence_button.setObjectName(u"edit_expence_button")

        self.expence_editor_layout.addWidget(self.edit_expence_button)

        self.delete_expence_button = QPushButton(self.centralwidget)
        self.delete_expence_button.setObjectName(u"delete_expence_button")

        self.expence_editor_layout.addWidget(self.delete_expence_button)


        self.bottom_layout.addLayout(self.expence_editor_layout)


        self.global_layout.addLayout(self.bottom_layout)


        self.horizontalLayout_3.addLayout(self.global_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0445\u043e\u0434\u044b", None))
        self.budget_label_2.setText(QCoreApplication.translate("MainWindow", u"\u0411\u044e\u0434\u0436\u0435\u0442", None))
        self.empty_label.setText("")
        self.day_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0435\u043d\u044c", None))
        self.week_3.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u0434\u0435\u043b\u044f", None))
        self.month_3.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.summ_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0443\u043c\u043c\u0430", None))
        self.day_2.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.week_2.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.month_2.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.budget_label.setText(QCoreApplication.translate("MainWindow", u"\u0411\u044e\u0434\u0436\u0435\u0442", None))
        self.day.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.week.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.month.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.expence_editor_label.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0445\u043e\u0434", None))
        self.add_expence_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.edit_expence_button.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.delete_expence_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
    # retranslateUi

