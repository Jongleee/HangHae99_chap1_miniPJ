from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('mongodb+srv://test:sparta@cluster0.lce4j.mongodb.net/Cluster0?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:sparta@cluster0.rv5esal.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

import jwt, datetime, hashlib


@app.route('/')
def home():
    gym_card = list(db.scgym.find({'gunum':1}, {'_id': False}).limit(30))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('main.html', gym_card=gym_card)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/1')
def home1():
    gym_card = list(db.scgym.find({'gunum':1}, {'_id': False}).limit(30))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('main.html', gym_card=gym_card)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/2')
def home2():
    gym_card = list(db.scgym.find({'gunum':2}, {'_id': False}).limit(30))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('main.html', gym_card=gym_card)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/3')
def home3():
    gym_card = list(db.scgym.find({'gunum':3}, {'_id': False}).limit(30))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('main.html', gym_card=gym_card)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']}, {"_id": False})
        nick = user_info["nick"]
        return render_template('main.html', nickname=nick, gym_card=gym_card)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# DB 데이터 가져오기(메인페이지-헬스장 리스트) : jinja2로 index.html에서 나타내기
@app.route('/listing', methods=['GET'])
def listing1():
    gym_card = list(db.scgym.find({}).limit(30))
    for card in gym_card:
        card['_id'] = str(card['_id'])
    return jsonify({'gym_card': gym_card})


#
# @app.route('/main_sh', methods=['GET'])
# def main_get_nick():
#     token_receive = request.cookies.get('mytoken')
#
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"id": payload['id']})
#         return jsonify({'result': 'success', 'nickname': user_info['nick']})
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#


# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_check_receive = request.form['pw_check_give']
    gender_receive = request.form['gender_give']
    nick_receive = request.form['nick_give']

    print(id_receive, pw_receive, pw_check_receive, gender_receive, nick_receive)

    if id_receive == '':
        return jsonify({'result': 'empty', 'msg': '아이디를 입력해주세요.'})
    elif pw_receive == '':
        return jsonify({'result': 'empty', 'msg': '비밀번호를 입력해주세요.'})
    elif pw_check_receive == '':
        return jsonify({'result': 'empty', 'msg': '비밀번호를 입력해주세요'})
    elif gender_receive == '':
        return jsonify({'result': 'empty', 'msg': '성별을 선택해주세요'})
    elif nick_receive == '':
        return jsonify({'result': 'empty', 'msg': '닉네임을 입력해주세요'})
    else:
        if pw_receive != pw_check_receive:
            return jsonify({'result': 'empty', 'msg': '비밀번호가 서로 다릅니다.'})
        else:
            pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

            id_result = db.users.find_one({'id': id_receive})
            nick_result = db.users.find_one({'id': nick_receive})

            if id_result is not None:
                return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다.'})
            elif nick_result is not None:
                return jsonify({'result': 'fail', 'msg': '중복된 닉네임이 있습니다.'})
            else:
                db.users.insert_one(
                    {'id': id_receive, 'pw': pw_hash, 'nick': nick_receive, 'gender': gender_receive})
                return jsonify({'result': 'success', 'msg': '회원가입을 완료했습니다.'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if id_receive == '':
        return jsonify({'result': 'fail_id', 'msg': '아이디를 입력해주세요'})
    elif pw_receive == '':
        return jsonify({'result': 'fail_pw', 'msg': '비밀번호를 입력해주세요'})
    elif result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디와 비밀번호를 확인해주세요'})


# [ID_Check]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/register/id_check', methods=['POST'])
def register_id_check():
    checkid_receive = request.form['id_give']

    result_id = db.users.find_one({'id': checkid_receive})

    if checkid_receive == '':
        return jsonify({'result': 'empty', 'msg': '아이디를 입력해주세요.'})
    elif result_id is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다.'})
    else:
        return jsonify({'id': checkid_receive, 'result': 'success', 'msg': '사용 가능한 아이디입니다.'})


@app.route('/api/register/nick_check', methods=['POST'])
def register_nick_check():
    checknick_receive = request.form['nick_give']

    result_id = db.users.find_one({'nick': checknick_receive})

    if checknick_receive == '':
        return jsonify({'result': 'empty', 'msg': '닉네임을 입력해주세요.'})
    elif result_id is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 닉네임이 있습니다.'})
    else:
        return jsonify({'id': checknick_receive, 'result': 'success', 'msg': '사용 가능한 닉네임입니다.'})


# 데이터 입력용 rest api키
# import requests
#
# searching = '강남구 헬스장'
# url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
# headers = {
#     "Authorization": "KakaoAK 264e01f5ee4957795f4b1518a3c2e783"
# }
# places = requests.get(url, headers = headers).json()['documents']
#
# for i in range(15):
#     doc={
#         'gymn':places[i]['place_name'],
#         'gyma':places[i]['address_name'],
#         'gcate':places[i]['category_name'],
#         'gphone':places[i]['phone'],
#         'gurl':places[i]['place_url'],
#         'gra':places[i]['road_address_name'],
#         'gx':places[i]['x'],
#         'gy':places[i]['y'],
#         'gunum':1
#     }
#     db.scgym.insert_one(doc)


@app.route('/detail/<keyword>/')
def detail(keyword):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']}, {"_id": False})
        nick = user_info["nick"]
        scgym = db.scgym.find_one({"gymn": keyword}, {"_id": False})
        return render_template('detail.html', nickname=nick, gym=keyword, scgym=scgym)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 회원별 운동 시설 평가 기능: 평가, 회원의 닉네임 가져오기
@app.route('/detail/<keyword>/review', methods=['POST'])
def post_review(keyword):
    gym_receive = request.form['gym_give']
    nick_receive = request.form['nick_give']
    comment_receive = request.form['comment_give']
    doc = {
        'gym': gym_receive,
        'nick_receive': nick_receive,
        'comment_receive': comment_receive
    }
    db.review_comment.insert_one(doc)
    return jsonify({'msg': '나만의 리뷰를 등록 완료.'})


@app.route('/detail/<keyword>/review', methods=['GET'])
def get_review(keyword):
    gym = keyword
    review_list = list(db.review_comment.find({'gym': gym}, {'_id': False}))
    if (len(review_list) == 0):
        return jsonify({'result': 'empty', 'msg': 'There is no review in this gym. Sorry...'})
    else:
        return jsonify({'result': 'success', 'review_list': review_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
