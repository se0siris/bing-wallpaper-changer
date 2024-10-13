from xml.etree import ElementTree

from PyQt5.QtCore import QObject, pyqtSignal, QDate, QUrl, QTimer, pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class ImageDownloader(QObject):

    TYPE_META = 1000
    ATTEMPTS = 1001

    # Signals.
    download_finished = pyqtSignal(QImage, QDate, str)
    download_failed = pyqtSignal(str)
    thumbnail_download_finished = pyqtSignal(QImage, QDate, str, int)
    status_text = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ImageDownloader, self).__init__(parent)
        self.resolution = '1920x1200'
        self.last_image_url = None
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.reply_finished)

    def set_resolution(self, resolution):
        """
        Set the image resolution.

        @param resolution: 1024x768, 1280x720, 1366x768, 1920x1200
        @type: str
        """
        self.resolution = resolution

    def _get_url(self, url_string, request_type=None, request_metadata=None):
        url = QUrl(url_string)
        request = QNetworkRequest(QUrl(url))
        if request_type is not None:
            request.setAttribute(self.TYPE_META, (request_type, request_metadata))
        self.manager.get(request)

    def get_full_wallpaper(self, day_index=0):
        self.status_text.emit('Checking for wallpaper update...')
        xml_url = f'https://www.bing.com/HPImageArchive.aspx?format=xml&idx={day_index}&n=1&mkt=en-ww'
        self._get_url(xml_url, 0)

    def get_history_thumbs(self, day_index=0):
        xml_url = f'https://www.bing.com/HPImageArchive.aspx?format=xml&idx={day_index}&n=8&mkt=en-ww'
        self._get_url(xml_url, 3, day_index)

    def parse_daily_xml(self, xml_data, full_image=False, day_index=0):
        root = ElementTree.fromstring(xml_data)

        if full_image:
            base_url = 'https://www.bing.com' + root[0].find('urlBase').text
            start_date = QDate.fromString(root[0].find('startdate').text, 'yyyyMMdd')
            copyright_info = root[0].find('copyright').text

            image_url = '{}_{}.jpg'.format(base_url, self.resolution)
            print(image_url)
            if image_url == self.last_image_url:
                print(f'Image is the same as last downloaded image. ({image_url})')
                self.download_finished.emit(QImage(), QDate(), '')
                return
            self.status_text.emit('Downloading image...')
            self.last_image_url = image_url
            self._get_url(image_url, 1, (start_date, copyright_info))
        else:
            for image_number in range(len(root) - 1):
                image_day_index = image_number + day_index
                url = 'https://www.bing.com' + root[image_number].find('url').text
                image_date = QDate.fromString(root[image_number].find('startdate').text, 'yyyyMMdd')
                copyright_info = root[image_number].find('copyright').text
                self._get_url(url, 4, (image_date, copyright_info, image_day_index))

    @pyqtSlot(QNetworkReply)
    def reply_finished(self, reply: QNetworkReply):
        url = reply.url()
        request = reply.request()
        print('URL Downloaded:', str(url.toEncoded()))
        if reply.error():
            attempts = request.attribute(self.ATTEMPTS)
            attempts = 0 if attempts is None else attempts
            if attempts <= 10:
                request.setAttribute(self.ATTEMPTS, attempts + 1)
                print('Network not available. Trying again in 5 seconds...', self.manager.networkAccessible())
                QTimer.singleShot(5000, lambda: self.manager.get(request))
                return

            error_message = str(reply.errorString())
            self.download_failed.emit(error_message)
            print(f'Download of {str(url.toEncoded()):s} failed: {error_message:s}')
        else:
            # print 'Mime-type:', str(reply.header(QNetworkRequest.ContentTypeHeader).toString())
            data = reply.readAll()
            attribute = request.attribute(self.TYPE_META)

            try:
                request_type, request_metadata = attribute
            except (IndexError, TypeError):
                return

            if request_type == 0:  # Daily wallpaper XML.
                self.parse_daily_xml(data, True)
            elif request_type == 1:
                start_date, copyright_info = request_metadata
                wallpaper_image = QImage.fromData(data)
                self.download_finished.emit(wallpaper_image, start_date, copyright_info)
            if request_type == 3:  # History thumbnails.
                day_index = request_metadata
                self.parse_daily_xml(data, False, day_index)
            elif request_type == 4:
                image_date, copyright_info, image_day_index = request_metadata
                wallpaper_image = QImage.fromData(data)
                self.thumbnail_download_finished.emit(wallpaper_image, image_date, copyright_info, image_day_index)