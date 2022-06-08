import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import humanize
import pafy

import os
import os.path
import urllib.request
from PyQt5.uic import loadUiType

ui, _ = loadUiType("main.ui")

class Main(QMainWindow, ui):
    def __init__(self,parent =None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.aqua_theme()
        self.handle_buttons()
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)
        self.progressBar_3.setValue(0)

    def init_ui(self):
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.pushButton_2.clicked.connect(self.open_home)
        self.pushButton_6.clicked.connect(self.open_download)
        self.pushButton_10.clicked.connect(self.open_youtube)
        self.pushButton_11.clicked.connect(self.open_settings)

        self.pushButton.clicked.connect(self.download)
        self.pushButton_8.clicked.connect(self.handle_browse)
        self.pushButton_3.clicked.connect(self.save_browse)

        self.pushButton_5.clicked.connect(self.get_video_data)
        self.pushButton_4.clicked.connect(self.download_video)

        self.pushButton_7.clicked.connect(self.playlist_download)
        self.pushButton_9.clicked.connect(self.playlist_save_browse)

        self.pushButton_12.clicked.connect(self.qdark_theme)
        self.pushButton_13.clicked.connect(self.dark_blue_theme)
        self.pushButton_14.clicked.connect(self.dark_orange_theme)
        self.pushButton_15.clicked.connect(self.aqua_theme)


    def handle_progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percent = readed_data*100/totalsize
            self.progressBar.setValue(int(download_percent))
            QApplication.processEvents()

    def handle_browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_2.setText(str(save_location[0]))

    def download(self):
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.handle_progress)
            except Exception:
                QMessageBox.warning(self, "Download Error","provide a valid URL or save location")
                return
            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def save_browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_4.setText(str(save_location[0]))

    def get_video_data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "provide a valid video URL")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)


    def download_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid video URL or save location")

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath = save_location, callback = self.video_progress)

    def video_progress(self,total,received,ratio,rate,time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(float(download_percentage))
            remaining_time = round(time/60, 2)

            self.label_5.setText(str('{} minute remaining'.format(remaining_time)))
            QApplication.processEvents()

    def playlist_download(self):
        playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()

        QApplication.processEvents()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.playlist_progress)
            QApplication.processEvents()

            current_video_in_download += 1

    def playlist_progress(self,total,received,ratio,rate,time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(float(download_percentage))
            remaining_time = round(time / 60, 2)

            self.label_6.setText(str('{} minute remaining'.format(remaining_time)))
            QApplication.processEvents()

    def playlist_save_browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self,"select download directory")
        self.lineEdit_6.setText(playlist_save_location)

    def open_home(self):
        self.tabWidget.setCurrentIndex(0)

    def open_download(self):
        self.tabWidget.setCurrentIndex(1)

    def open_youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings(self):
        self.tabWidget.setCurrentIndex(3)

    def dark_blue_theme(self):
        style = open('themes/dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def aqua_theme(self):
        style = open('themes/Aqua.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes/dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qdark_theme(self):
        style = open('themes/Ubuntu.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

