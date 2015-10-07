import os
from PyQt4.QtCore import QObject, pyqtSignal, QString
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

__author__ = 'Gary'


class CopyrightDatabase(QObject):
    """
    Database wrapper for SQLite 3 databases.
    """

    # Signals
    error = pyqtSignal(QString, QString)

    def __init__(self, parent=None):
        super(CopyrightDatabase, self).__init__(parent)
        settings_folder = str(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        db_path = os.path.join(settings_folder, 'copyright.db')

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        """@type : QSqlDatabase"""
        self.db.setDatabaseName(db_path)

        self.db.open()

        if not 'copyright' in self.db.tables():
            self.create_copyright_table()

    def create_copyright_table(self):
        query = QSqlQuery(self.db)
        query.prepare('''
            CREATE TABLE copyright (
                image_date DATE PRIMARY KEY
                                UNIQUE,
                copyright_info  TEXT
            );
        ''')
        if not query.exec_():
            self.error.emit('Error creating copyright table', query.lastError().text())
            return False
        return True

    def set_info(self, image_date, info):
        query = QSqlQuery(self.db)
        query.prepare('INSERT INTO copyright (image_date, copyright_info) VALUES (?, ?);')
        query.addBindValue(image_date)
        query.addBindValue(info)
        if not query.exec_():
            self.error.emit('Error adding copyright info', query.lastError().text())
            return False
        return True

    def get_info(self, image_date):
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        query.prepare('SELECT copyright_info FROM copyright WHERE image_date = ?;')
        query.addBindValue(image_date)
        if not query.exec_():
            self.error.emit('Error getting copyright info', query.lastError().text())
            return ''
        query.first()
        copyright_info = query.value(0).toString()
        return copyright_info

    def get_all_info(self):
        info = {}
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        query.prepare('SELECT image_date, copyright_info FROM copyright;')
        if not query.exec_():
            self.error.emit('Error getting all copyright info', query.lastError().text())
            return info
        while query.next():
            image_date = str(query.value(0).toString())
            copyright_info = unicode(query.value(1).toString())
            info[image_date] = copyright_info
        return info
