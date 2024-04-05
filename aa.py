import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

form_class = uic.loadUiType("ui/weatherUi.ui")[0]


# ui 폴더 내의 디자인된 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")

        self.search_btn.clicked.connect(self.weather_search)

    def weather_search(self):
        inputArea = self.area_input.text()  # 사용자가 입력한 지역명 텍스트 가져오기

        weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
        # 네이버에서 한남동날씨로 검색한 결과 html 파일 가져오기
        # print(weatherHtml.text)

        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
        # print(weatherSoup)

        areaText = weatherSoup.find("h2", {"class": "title"}).text  # 날씨 지역 이름 가져오기
        areaText = areaText.strip()  # 양쪽 공백 제거
        print(f"지역이름 : {areaText}")

        todayTempText = weatherSoup.find("div", {"class": "temperature_text"}).text  # 현재온도 가져오기
        todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
        print(f"현재온도 : {todayTempText}")

        # yesterdayTempText = weatherSoup.find("span", {"class":"temperature"}).text  #어제와의 날씨 비교
        # yesterdayTempText.strip()
        yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text  # 어제와의 날씨 비교
        yesterdayTempText = yesterdayTempText[:15].strip()
        print(f"어제날씨비교 : {yesterdayTempText}")

        todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text  # 오늘 날씨 텍스트
        todayWeatherText = todayWeatherText.strip()
        print(f"오늘날씨 : {todayWeatherText}")

        senseTempText = weatherSoup.find("dd", {"class": "desc"}).text  # 현재 체감온도
        senseTempText = senseTempText.strip()
        print(f"체감온도 : {senseTempText}")

        todayInfoText = weatherSoup.select("ul.today_chart_list>li")  # 미세먼지, 초미세먼지, 자외선, 일몰
        # print(todayInfoText)
        # print("-------------------------------")
        # print(todayInfoText[0])
        dust1Info = todayInfoText[0].find("span", {"class": "txt"}).text  # 미세먼지 정보
        dust1Info = dust1Info.strip()
        print(f"미세먼지 : {dust1Info}")
        dust2Info = todayInfoText[1].find("span", {"class": "txt"}).text  # 초미세먼지 정보
        dust2Info = dust2Info.strip()
        print(f"초미세먼지 : {dust2Info}")

        # 크롤링한 날씨정보 텍스트를 준비된 UI에 출력하기
        self.area_title.setText(areaText)
        self.weather_img.setText(todayWeatherText)
        self.now_temper.setText(todayTempText)
        self.yester_temper.setText(yesterdayTempText)
        self.sense_temper.setText(senseTempText)
        self.dust1_info.setText(dust1Info)
        self.dust2_info.setText(dust2Info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())