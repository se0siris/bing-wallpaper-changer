from PyQt4.QtCore import QSize, QDate, Qt, QRect
from PyQt4.QtGui import QLabel, QSystemTrayIcon, QMenu, QApplication, QListWidgetItem, QListWidget, QPixmap, QPainter, \
    QIcon

__author__ = 'Gary'


def text_to_date(text):
    text = '{} {}'.format(str(text), str(QDate.currentDate().year()))
    return QDate.fromString(text, 'dddd dd MMMM yyyy')


class ImageLabel(QLabel):
    """
    Custom label with hardcoded sizeHint() to prevent weird resizing issues.
    """

    def sizeHint(self):
        return QSize(0, 0)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.settings_action = menu.addAction('&Settings')
        self.exit_action = menu.addAction('E&xit')

        self.settings_action.triggered.connect(self.show_settings)
        self.exit_action.triggered.connect(self.close_application)
        self.setContextMenu(menu)
        self.setToolTip(QApplication.instance().applicationName())

    def show_settings(self):
        self.parent().tabWidget.setCurrentIndex(1)
        self.parent().show()
        self.parent().setFocus()

    def close_application(self):
        self.parent().close()


class ListWidgetItem(QListWidgetItem):
    """
    Custom QListWidgetItem to provide custom sorting for items with a QDate.
    """

    def __le__(self, b):
        return b.image_date <= self.image_date

    def __lt__(self, b):
        return b.image_date < self.image_date

    def __gt__(self, b):
        return b.image_date > self.image_date

    def __ge__(self, b):
        return b.image_date >= self.image_date

    def __eq__(self, b):
        return b.image_date == self.image_date

    def __ne__(self, b):
        return b.image_date != self.image_date


class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.added_dates = set()
        self.pixmap_hd = QPixmap(':/icons/ui/drive-harddisk.svg').scaledToWidth(25, Qt.SmoothTransformation)

    def clear(self):
        """
        Sub-classed clear() method to also clear the self.added_dates set.
        """
        super(ListWidget, self).clear()
        self.added_dates.clear()

    def add_item(self, thumbnail_image, date, info, day_index=-1, archive_path=None):
        """

        @param thumbnail_image: Image to be used in thumbnail
        @param date: Date of image
        @param info: Copyright info for image
        @param day_index: Day index of image
        @param archive_path: Path to the local file, or None if image source is the RSS feed.

        @type thumbnail_image: QImage
        @type date: QDate
        @type info: str
        @type day_index: int
        @type archive_path: unicode or None
        """
        if date.year() == QDate.currentDate().year():
            date_label = str(date.toString('dddd dd MMMM'))
        else:
            date_label = str(date.toString('dddd dd MMMM, yyyy'))
        if date_label in self.added_dates:
            # This date has already been added. Don't bother adding it again.
            print 'Ignored', date_label
            return
        if archive_path:
            pixmap = QPixmap.fromImage(thumbnail_image)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            circle_area = QRect(pixmap.width() - 35, pixmap.height() - 35, 25, 25)
            painter.setOpacity(0.7)
            painter.setPen(Qt.lightGray)
            painter.setBrush(Qt.lightGray)
            painter.drawEllipse(circle_area)
            painter.drawPixmap(circle_area.topLeft(), self.pixmap_hd)
            painter.end()
        else:
            pixmap = QPixmap.fromImage(
                thumbnail_image.scaled(QSize(200, 125), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        icon = QIcon(pixmap)
        widget_item = ListWidgetItem(icon, date_label, self)
        widget_item.setToolTip(info)
        widget_item.image_day_index = day_index
        widget_item.archive_path = archive_path
        widget_item.image_date = date
        self.added_dates.add(date_label)
