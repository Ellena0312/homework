from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/order_list', methods=['POST'])
def write_order_list():
    name_receive = request.form['name_give']
    number_receive = request.form['number_give']
    phone_num_receive = request.form['phone_num_give']
    address_receive = request.form['address_give']

	# 2. DB에 정보 삽입하기
    doc = {
        'name': name_receive,
        'number': number_receive,
        'phone_num': phone_num_receive,
        'address': address_receive
    }
    db.order_list.insert_one(doc)

	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문 내역 작성 완료!'})


@app.route('/order_list', methods=['GET'])
def read_order_list():
    order_lists = list(db.order_list.find({}, {'_id': False}))
    print(order_lists)
    return jsonify({'result': 'success', 'data': order_lists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)