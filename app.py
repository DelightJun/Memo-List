from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# import requests
# from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_memo():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.memos.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'memos': result})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_memo():
	# 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
	# 2. meta tag를 스크래핑하기
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(title_receive, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')

    memo = {'title':title_receive, 'comment':comment_receive}
	# 3. mongoDB에 데이터 넣기
    db.memos.insert_one(memo)

    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_memo():
    # 1. 클라이언트가 전달한 title_give를 name_receive 변수에 넣습니다.
    title_receive = request.form['title_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.memos.delete_one({'title': title_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})

# @app.route('/api/modify', methods=['POST'])
# def modify_memo():
#     title_receive = request.form['title_give']
#     comment_receive = request.form['comment_give']

#     memo = {'title':title_receive, 'comment':comment_receive}

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)