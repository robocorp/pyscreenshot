import logging

from PIL import Image
from pyscreenshot.plugins.backend import CBackend
from pyscreenshot.util import py2

if py2():
    import StringIO

    BytesIO = StringIO.StringIO
else:
    import io

    BytesIO = io.BytesIO


log = logging.getLogger(__name__)

# based on qt4 backend

app = None


class Qt5GrabWindow(CBackend):
    name = "pyqt5"
    childprocess = False
    apply_childprocess = True

    def __init__(self):
        pass

    def grab_to_buffer(self, buff, file_type="png"):
        import PyQt5
        from PyQt5 import QtWidgets

        QApplication = QtWidgets.QApplication
        QBuffer = PyQt5.Qt.QBuffer
        QIODevice = PyQt5.Qt.QIODevice
        QScreen = PyQt5.QtGui.QScreen

        global app
        if not app:
            app = QApplication([])
        qbuffer = QBuffer()
        qbuffer.open(QIODevice.ReadWrite)
        QScreen.grabWindow(
            QApplication.primaryScreen(), QApplication.desktop().winId()
        ).save(qbuffer, file_type)
        buff.write(qbuffer.data())
        qbuffer.close()

    def grab(self, bbox=None):
        strio = BytesIO()
        self.grab_to_buffer(strio)
        strio.seek(0)
        im = Image.open(strio)
        if bbox:
            im = im.crop(bbox)
        return im

    def backend_version(self):
        from PyQt5 import Qt

        return Qt.PYQT_VERSION_STR
