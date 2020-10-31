import sys

import requests
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from geopy.geocoders import Nominatim

api_key = "d2c5f120418926301fd81f6589e2531d"
lat = ""
lon = ""

geolocator = Nominatim(user_agent="Location")


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("BestWeather.py")
        self.thread = Worker()
        self.l1 = QLabel()
        self.l1.setText("Weather App")
        self.labelctemp = QLabel()
        self.labelctemp.setText("ctemp")
        self.labelcfeeltemp = QLabel()
        self.labelcfeeltemp.setText("ftemp")
        self.labelpressure = QLabel()
        self.labelpressure.setText("pressure")
        self.labelhumidity = QLabel()
        self.labelhumidity.setText("humidity")
        self.labeldewpoint = QLabel()
        self.labeldewpoint.setText("dewpoint")
        self.labeluvi = QLabel()
        self.labeluvi.setText("UV Index")
        self.labelmw = QLabel()
        self.labelmw.setText("MainWeather")
        self.labeldes = QLabel()
        self.labeldes.setText("Description")
        self.town = QLabel()
        self.town.setText("Your Town")
        self.tests = QLabel()
        self.buttonStart = QPushButton("Enter City Name")
        self.textbox = QLineEdit(self)
        self.textbox.resize(300, 45)
        self.picture = QLabel(self)
        self.pixmap = QPixmap("none.png")
        self.pixmap = self.pixmap.scaled(100, 100)
        self.picture.setPixmap(self.pixmap)

        layout = QGridLayout(self)
        layout.addWidget(self.l1, 0, 2)
        layout.addWidget(self.town, 1, 0)
        layout.addWidget(self.picture, 1, 3)
        layout.addWidget(self.labelctemp, 2, 0)
        layout.addWidget(self.labelcfeeltemp, 3, 0)
        layout.addWidget(self.labelpressure, 4, 0)
        layout.addWidget(self.labelhumidity, 5, 0)
        layout.addWidget(self.labeldewpoint, 6, 0)
        layout.addWidget(self.labeluvi, 7, 0)
        layout.addWidget(self.labelmw, 8, 0)
        layout.addWidget(self.labeldes, 9, 0)
        layout.addWidget(self.textbox, 10, 0)
        layout.addWidget(self.buttonStart, 11, 0)

        self.buttonStart.clicked.connect(self.start)
        self.thread.temp.connect(self.currenttemp)
        self.thread.feeltemp.connect(self.feeltemp)
        self.thread.pressure.connect(self.pressure)
        self.thread.humidity.connect(self.humidity)
        self.thread.dewpoint.connect(self.dewpoint)
        self.thread.uvi.connect(self.uvindex)
        self.thread.mw.connect(self.mainweather)
        self.thread.wdes.connect(self.description)

    def start(self):
        global lat, lon
        locationinput = self.textbox.text()
        location = geolocator.geocode(locationinput)
        address = location.address
        self.town.setText(address)
        lat = location.latitude
        lon = location.longitude
        self.buttonStart.setEnabled(False)
        self.thread.start()

    def currenttemp(self, val):
        val = str(val)
        self.labelctemp.setText("Temperature: " + val)

    def feeltemp(self, val):
        val = str(val)
        self.labelcfeeltemp.setText("Feels like: " + val)

    def pressure(self, val):
        val = str(val)
        self.labelpressure.setText("Pressure: " + val)

    def humidity(self, val):
        val = str(val)
        self.labelhumidity.setText("Humidity: " + val)

    def dewpoint(self, val):
        val = str(val)
        self.labeldewpoint.setText("Dewpoint: " + val)

    def uvindex(self, val):
        val = str(val)
        self.labeluvi.setText("UV-Index: " + val)

    def mainweather(self, val):
        val = str(val)
        if val == "Clouds":
            self.pixmap = QPixmap("cloudy.png")
            self.pixmap = self.pixmap.scaled(100, 100)
            self.picture.setPixmap(self.pixmap)

        self.labelmw.setText("Current weather: " + val)

    def description(self, val):
        val = str(val)
        self.labeldes.setText("Description: " + val)


class Worker(QThread):
    temp = pyqtSignal(int)
    feeltemp = pyqtSignal(int)
    pressure = pyqtSignal(int)
    humidity = pyqtSignal(int)
    dewpoint = pyqtSignal(int)
    uvi = pyqtSignal(float)
    mw = pyqtSignal(str)
    wdes = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working:
            url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
                lat, lon, api_key)
            response = requests.get(url)
            data = json.loads(response.text)
            currentweather = data["current"]
            currentweather2 = data["current"]["weather"]
            ctemp = currentweather["temp"]
            cfeeltemp = currentweather["feels_like"]
            cpressure = currentweather["pressure"]
            chumidity = currentweather["humidity"]
            cdewpoint = currentweather["dew_point"]
            uiv = currentweather["uvi"]
            cw = currentweather2[0]
            mainweather = cw['main']
            description = cw['description']
            ctemp = round(ctemp)
            cfeeltemp = round(cfeeltemp)
            cpressure = round(cpressure)
            chumidity = round(chumidity)
            cdewpoint = round(cdewpoint)

            self.temp.emit(ctemp)
            self.feeltemp.emit(cfeeltemp)
            self.pressure.emit(cpressure)
            self.humidity.emit(chumidity)
            self.dewpoint.emit(cdewpoint)
            self.uvi.emit(uiv)
            self.mw.emit(mainweather)
            self.wdes.emit(description)
            self.working = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())
