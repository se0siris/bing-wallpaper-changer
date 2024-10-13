from typing import Any

from PyQt5.QtCore import QModelIndex, Qt, QDate, QRect, QSize, QAbstractTableModel
from PyQt5.QtGui import QPixmap, QPainter, QImageReader, QPixmapCache, QImage


class HistoryListModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super(HistoryListModel, self).__init__(parent)
        self._data = []
        self._added_dates = set()

        self._pixmap_hd = QPixmap(
            ':/icons/ui/drive-harddisk.svg'
        ).scaledToWidth(
            25,
            Qt.SmoothTransformation
        )

        self._image_reader = QImageReader()
        QPixmapCache.setCacheLimit(1024000)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.EditRole) -> Any:
        # [date_label, info, thumbnail_image, archive_path, day_index]
        row = index.row()

        if role == Qt.DisplayRole:
            return self._data[row][0]
        elif role == Qt.ToolTipRole:
            return self._data[row][1]
        elif role == Qt.DecorationRole:
            row_str = f'Row_{row:05d}'
            cached_pixmap = QPixmapCache.find(row_str)
            # print(f'Cached: {row_str} {str(cached_pixmap)}')
            if cached_pixmap:
                return cached_pixmap
            archive_path = self._data[row][3]
            if archive_path:
                # Load the image from the archive_path using QImageReader.
                self._image_reader.setFileName(archive_path)
                self._image_reader.setScaledSize(QSize(200, 125))
                pixmap = QPixmap.fromImageReader(self._image_reader)

                # Add the hard disk icon to the bottom right corner of the image.
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                circle_area = QRect(pixmap.width() - 35, pixmap.height() - 35, 25, 25)
                painter.setOpacity(0.7)
                painter.setPen(Qt.lightGray)
                painter.setBrush(Qt.lightGray)
                painter.drawEllipse(circle_area)
                painter.drawPixmap(circle_area.topLeft(), self._pixmap_hd)
                painter.end()
            else:
                # Create a pixmap from the QImage in self._data.
                thumbnail_image = self._data[row][2]
                pixmap = QPixmap.fromImage(
                    thumbnail_image.scaled(
                        QSize(200, 125), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                    )
                )

            # Cache the pixmap for future use.
            QPixmapCache.insert(row_str, pixmap)
            return pixmap

        return None

    def clear(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()

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
        # Create a label for the date, including the year if it is not the current year.
        if date.year() == QDate.currentDate().year():
            date_label = date.toString('ddd dd MMM')
        else:
            date_label = date.toString('ddd dd MMM, yyyy')

        if date_label in self._added_dates:
            # This date has already been added. Don't bother adding it again.
            print('Ignored', date_label)
            return

        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count)
        self._data.append(
            [date_label, info, thumbnail_image, archive_path, day_index]
        )
        self.endInsertRows()
        return
