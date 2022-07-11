from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.rv5esal.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

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