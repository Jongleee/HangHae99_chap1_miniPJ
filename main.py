from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/api/main', methods=['GET'])
def show_diary():
	sample_receive = request.args.get('sample_give')
	print(sample_receive)
	return jsonify({'msg': 'GET 연결 완료!'})

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EA%B0%95%EB%82%A8%EA%B5%AC+%ED%97%AC%EC%8A%A4%EC%9E%A5"
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

req = data.text
soup = BeautifulSoup(req, 'html.parser')

gyms = soup.select('#loc-main-section-root > section > div > ul')

for gym in gyms:
	gymTitle = gym.select('div._3ZU00._1rBq3 > a:nth-child(1) > div._2w9xx > div > span.place_bluelink._3Apve')
	gymAdd = gym.select('div._3ZU00._1rBq3 > div._1B9G6 > div > span > a > span._2Po-x')

	for gymT in gymTitle:
		gym_title = gymT.text
		print(gym_title)
	for gymA in gymAdd:
		gym_address = gymA.text
		print(gym_address)

@app.route('/')
def home():
	return render_template('main.html')


if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)
