import requests  # pip install requests

from bs4 import BeautifulSoup  # pip install beautifulSoup

weatherHtml = requests.get("https://search.naver.com/search.naver?&query=한남동날씨")
# 네이버에서 한남동남시로 검색한 결과 html 파일 가져오기
# print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
# print(weatherSoup)

areaText = weatherSoup.find("h2",{"class":"title"}).text  # 날씨 지역 이름 가져오기
areaText = areaText.strip()  # 양쪽 공백 제거
print(areaText)

todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text
# todayTempText = todayTempText[6:12]
todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
print(todayTempText)







