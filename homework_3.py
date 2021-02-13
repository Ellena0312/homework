import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.info > a')
    if a_tag is not None:
        title = a_tag.text.strip()
        artist = tr.select_one('td.info > a:nth-child(2)').text
        rank_before = tr.select_one('td.number').text.split()
        rank_after = rank_before[0]
        print(rank_after, title, artist)

        doc = {
            'title': title,
            'artist': artist,
            'rank': rank_after
        }
        db.music_chart.insert_one(doc)
