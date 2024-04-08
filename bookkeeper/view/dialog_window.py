# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QDialog,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTreeView, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(676, 511)
        self.horizontalLayout_5 = QHBoxLayout(Dialog)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.global_layout = QHBoxLayout()
        self.global_layout.setObjectName(u"global_layout")
        self.left_layout = QVBoxLayout()
        self.left_layout.setObjectName(u"left_layout")
        self.transaction_label = QLabel(Dialog)
        self.transaction_label.setObjectName(u"transaction_label")
        self.transaction_label.setEnabled(True)

        self.left_layout.addWidget(self.transaction_label)

        self.date_time_layout = QHBoxLayout()
        self.date_time_layout.setObjectName(u"date_time_layout")
        self.date_time_label = QLabel(Dialog)
        self.date_time_label.setObjectName(u"date_time_label")

        self.date_time_layout.addWidget(self.date_time_label)

        self.date_time = QDateTimeEdit(Dialog)
        self.date_time.setObjectName(u"date_time")

        self.date_time_layout.addWidget(self.date_time)


        self.left_layout.addLayout(self.date_time_layout)

        self.summ_layout = QHBoxLayout()
        self.summ_layout.setObjectName(u"summ_layout")
        self.summ_label = QLabel(Dialog)
        self.summ_label.setObjectName(u"summ_label")

        self.summ_layout.addWidget(self.summ_label)

        self.summ = QLineEdit(Dialog)
        self.summ.setObjectName(u"summ")

        self.summ_layout.addWidget(self.summ)


        self.left_layout.addLayout(self.summ_layout)

        self.category_layout = QHBoxLayout()
        self.category_layout.setObjectName(u"category_layout")
        self.category_label = QLabel(Dialog)
        self.category_label.setObjectName(u"category_label")

        self.category_layout.addWidget(self.category_label)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")

        self.category_layout.addWidget(self.comboBox)


        self.left_layout.addLayout(self.category_layout)

        self.comment_layout = QVBoxLayout()
        self.comment_layout.setObjectName(u"comment_layout")
        self.comment_label = QLabel(Dialog)
        self.comment_label.setObjectName(u"comment_label")

        self.comment_layout.addWidget(self.comment_label)

        self.comment = QLineEdit(Dialog)
        self.comment.setObjectName(u"comment")

        self.comment_layout.addWidget(self.comment)

        self.finish_button = QPushButton(Dialog)
        self.finish_button.setObjectName(u"finish_button")

        self.comment_layout.addWidget(self.finish_button)


        self.left_layout.addLayout(self.comment_layout)


        self.global_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setObjectName(u"right_layout")
        self.categoty_tree_layout = QVBoxLayout()
        self.categoty_tree_layout.setObjectName(u"categoty_tree_layout")
        self.category_tree_label = QLabel(Dialog)
        self.category_tree_label.setObjectName(u"category_tree_label")

        self.categoty_tree_layout.addWidget(self.category_tree_label)

        self.category_tree = QTreeView(Dialog)
        self.category_tree.setObjectName(u"category_tree")

        self.categoty_tree_layout.addWidget(self.category_tree)


        self.right_layout.addLayout(self.categoty_tree_layout)

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(Dialog)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton(Dialog)
        self.edit_button.setObjectName(u"edit_button")

        self.buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton(Dialog)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)


        self.right_layout.addLayout(self.buttons_layout)


        self.global_layout.addLayout(self.right_layout)


        self.horizontalLayout_5.addLayout(self.global_layout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.transaction_label.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u0432\u0430\u044f \u0442\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f", None))
        self.date_time_label.setText(QCoreApplication.translate("Dialog", u"\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f", None))
        self.summ_label.setText(QCoreApplication.translate("Dialog", u"\u0421\u0443\u043c\u043c\u0430     ", None))
        self.category_label.setText(QCoreApplication.translate("Dialog", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.comment_label.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439", None))
        self.finish_button.setText(QCoreApplication.translate("Dialog", u"\u0433\u043e\u0442\u043e\u0432\u043e", None))
        self.category_tree_label.setText(QCoreApplication.translate("Dialog", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438", None))
        self.add_button.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.edit_button.setText(QCoreApplication.translate("Dialog", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.delete_button.setText(QCoreApplication.translate("Dialog", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
    # retranslateUi

