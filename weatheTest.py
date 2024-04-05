import requests  # pip install requests

from bs4 import BeautifulSoup  # pip install beautifulSoup

inputArea = input("날씨를 조회하려는 지역을 입력하세요 :")

weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
# 네이버에서 한남동 날씨로 검색한 결과 html 파일 가져오기
# print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
# print(weatherSoup)

areaText = weatherSoup.find("h2",{"class":"title"}).text  # 날씨 지역 이름 가져오기
areaText = areaText.strip()  # 양쪽 공백 제거
print(f"지역이름 : {areaText}")

todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text  # 현재온도
# todayTempText = todayTempText[6:12]
todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
print(f"현재온도 : {todayTempText}")

yesterdatTempText = weatherSoup.find("span", {"class":"temperature"}).text  # 어제와의 날씨 비교
yesterdatTempText.strip()
yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text  # 어제와의 날씨 비교
yesterdayTempText = yesterdayTempText[:15].strip()
print(f"어제날씨비교 : {yesterdatTempText}")

todayWeatherText = weatherSoup.find("span", {"class":"weather before_slash"}).text  # 오늘 날씨 맑음
todayWeatherText.strip()
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


# print(f'{areaText} 온도는 {todayTempText} 입니다')





