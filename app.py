from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ovlot.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

import jwt, datetime, hashlib

@app.route('/login')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################


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

    print(id_receive,pw_receive,pw_check_receive,gender_receive,nick_receive)

    db.users.insert_one({'id': id_receive, 'pw': pw_receive, 'pw_check': pw_check_receive,
                         'gender': gender_receive, 'nick': nick_receive})
    return jsonify({'result': 'success', 'msg': '회원가입을 완료했습니다.'})

@app.route("/gyms", methods=["POST"])
def web_mars_post():
    id_receive = request.form['id_give']


    doc = {

    }

    db.gyms.insert_one(doc)

    return jsonify({'msg': '설정 완료'})

@app.route("/gyms", methods=["GET"])
def web_mars_get():
    order_list = list(db.mars.find({}, {'_id': False}))
    return jsonify({'orders': order_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)