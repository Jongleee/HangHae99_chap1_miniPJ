from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:saprta@cluster0.ci3ishc.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
	return render_template('main.html')

@app.route('/detail')
def home():
	return render_template('detail.html')

# @app.route("/main", methods=["POST"])
# def movie_post():
# 	url_receive = request.form['url_give']
# 	star_receive = request.form['star_give']
# 	comment_receive = request.form['comment_give']

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EA%B0%95%EB%82%A8%EA%B5%AC+%ED%97%AC%EC%8A%A4%EC%9E%A5", headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
gym_title = soup.select_one('#loc-main-section-root > section > div > ul > li:nth-child(1) > div._3ZU00._1rBq3 > a:nth-child(1) > div._2w9xx > div > span.place_bluelink._3Apve').text
print(gym_title)
#loc-main-section-root > section > div > ul > li:nth-child(4) > div._3ZU00._1rBq3 > a:nth-child(1) > div > div > span.place_bluelink._3Apve
#loc-main-section-root > section > div > ul > li:nth-child(3) > div._3ZU00._1rBq3 > a:nth-child(1) > div > div > span.place_bluelink._3Apve

gym = soup.select('#loc-main-section-root > section > div > ul')
# print(gym)
 # > li:nth-child(1) > div._3ZU00._1rBq3 > a:nth-child(1) > div._2w9xx > div > span.place_bluelink._3Apve
 # > li:nth-child(2) > div._3ZU00._1rBq3 > a:nth-child(1) > div._2w9xx > div > span.place_bluelink._3Apve

gym2 = soup.select_one('#loc-main-section-root > section > div > ul > li:nth-child(3) > div._3ZU00._1rBq3 > a:nth-child(1) > div > div > span.place_bluelink._3Apve')
print(gym2)

# gyms = soup.select('span')
# songs = soup.select("#frm > div > table > tbody > tr")

	# for song in songs:
	# 	title = song.select_one("td > div > div.wrap_song_info > div.rank01 > span > a").text
	# 	artist = song.select_one("td > div > div.wrap_song_info > div.rank02 > span > a").text
	# 	likes = song.select_one("td > div > button.like > span.cnt").text
	# 	print(title, artist, likes)

# @app.route("/movie", methods=["GET"])
# def movie_get():
# 	movie_list = list(db.movies.find({}, {'_id': False}))
# 	return jsonify({'movies': movie_list})

if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)

