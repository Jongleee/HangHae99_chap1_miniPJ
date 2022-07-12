from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.lce4j.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.project  # mongodb atlas 내 프로젝트명

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/detail/<keyword>')
def detail(keyword):
    return render_template("reply.html", gym=keyword,nickname='nick')

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