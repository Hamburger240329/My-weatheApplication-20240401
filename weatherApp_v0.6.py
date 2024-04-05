import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

form_class = uic.loadUiType("ui/weatherUi.ui")[0]
# ui 폴더 내의 디자인된 ui 불러오기 - 디자인 폼 이라고 함

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 여기까지는 모든 앱이 동일하다(13줄 ~ 16줄)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("img/weather_icon.png"))
        self.statusBar().showMessage("WEATHER SEARCH APP VER 0.6")

        self.search_btn.clicked.connect(self.weather_search)

    def weather_search(self):
        inputArea = self.area_input.text()  # 사용자가 입력한 지역명 텍스트 가져오기


        weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
        # 네이버에서 한남동 날씨로 검색한 결과 html 파일 가져오기
        # print(weatherHtml.text)

        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
        # print(weatherSoup)
        try:
            areaText = weatherSoup.find("h2",{"class":"title"}).text  # 날씨 지역 이름 가져오기
            areaText = areaText.strip()  # 양쪽 공백 제거
            print(f"지역이름 : {areaText}")

            todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text  # 현재온도
            # todayTempText = todayTempText[6:12]
            todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
            print(f"현재온도 : {todayTempText}")

            yesterdayTempText = weatherSoup.find("span", {"class":"temperature"}).text  # 어제와의 날씨 비교
            yesterdayTempText.strip()
            yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text  # 어제와의 날씨 비교
            yesterdayTempText = yesterdayTempText[:15].strip()
            print(f"어제날씨비교 : {yesterdayTempText}")


            todayWeatherText = weatherSoup.find("span", {"class":"weather before_slash"}).text  # 오늘 날씨 맑음
            todayWeatherText = todayWeatherText.strip()
            # todayWeatherText.strip()  # ???
            print(f"오늘날씨 : {todayWeatherText}")

            senseTempText = weatherSoup.find("dd", {"class":"desc"}).text
            senseTempText = senseTempText.strip()
            print(f"체감온도 : {senseTempText}")

            todayInfoText = weatherSoup.select("ul.today_chart_list>li")  # 미세먼지, 초미세먼지, 자외선, 일몰
            # ul.today_chart_list 안에 있는 li 태그 들을 몽땅 가지고와라
            # select : 하나 더 위에 있는 것을 잡을 때 사용
            # print(todayInfoText)
            # print("--------------------------------------------")
            # print(todayInfoText[0])
            dust1Info = todayInfoText[0].find("span", {"class" : "txt"}).text  # 미세먼지 정보
            dust1Info = dust1Info.strip()
            print(f"미세먼지 : {dust1Info}")

            dust2Info = todayInfoText[1].find("span", {"class" : "txt"}).text  # 초미세먼지 정보
            dust1Info = dust1Info.strip()
            print(f"초미세먼지 : {dust2Info}")

            # 크롤링한 날씨정보 텍스트를 준비된 UI에 출력하기
            self.area_title.setText(areaText)
            # self.weather_img.setText(todayWeatherText)

            self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출
            self.now_temper.setText(todayTempText)
            self.yester_temper.setText(yesterdayTempText)
            self.sense_temper.setText(senseTempText)
            self.dust1_info.setText(dust1Info)
            self.dust2_info.setText(dust2Info)

        except:
            try:
                # 해외날씨 처리 구문
                areaText = weatherSoup.find("h2", {"class" : "title"}).text  # 날씨 지역 이름 가져오기

                areaText = areaText.strip()
                todayTempAllText = weatherSoup.find("div", {"class":"temperature_text"}).text
                todayTempAllText = todayTempAllText.strip()
                print(todayTempAllText)

                todayTempText = todayTempAllText[6:9].strip()  # 해외 도시 현재 온도
                todayWeatherText = todayTempAllText[10:12].strip()  # 해외 도시 날씨 테스트
                senseTempText = todayTempAllText[18:].strip()  # 해외 도시 체감 온도
                self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출


                self.area_title.setText(areaText)
                self.now_temper.setText(todayTempText)
                self.sense_temper.setText(senseTempText)

                self.yester_temper.setText("")  # 해외도시 어제와 날씨 비교 정보 없음 빈공간 출력
                self.dust1_info.setText("-")
                self.dust2_info.setText("-")

            except:
                self.area_title.setText("입력된 지역명 오류")
                self.setWeatherImage("")  # 날씨 이미지 출력 함수 호출
                self.now_temper.setText("")
                self.yester_temper.setText(f"{inputArea} 지역은 존재하지 않습니다")
                self.sense_temper.setText("-")
                self.dust1_info.setText("-")
                self.dust2_info.setText("-")

    def setWeatherImage(self, weatherText):  # 날씨에 따른 이미지 출력 함수
        if weatherText == "맑음":
            weatherImage = QPixmap("img/sun.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
            # ui에 준비된 label 이름에 이미지 출력하기
        elif weatherText == "구름많음":
            weatherImage = QPixmap("img/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "흐림":
            weatherImage = QPixmap("img/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "비":
            weatherImage = QPixmap("img/rain.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "눈":
            weatherImage = QPixmap("img/snow.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_img.setText(weatherText)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())


