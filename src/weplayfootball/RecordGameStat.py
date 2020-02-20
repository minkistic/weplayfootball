# 메모장을 위한 서버를 만드는 과정입니다.
# 서버시작: mongod --dbpath ~/data/db

# HTML을 주는 API: 기본 실행
# HTML을 주는 API: HTML 파일 불러오기 -> render_template

from flask import Flask, render_template, jsonify, request

from pymongo import MongoClient  # pymongo를 임포트 하기

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbgamestat  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


@app.route('/gamestats')
def gamestat():
    return render_template('shoot_record2.html')


@app.route('/gamestat', methods=['POST'])
def event_post():
    #  db에 저장한다.
    try:  # 이걸 시도해봐 우선
        eventType = request.form['eventType']
        team = request.form['team']
        score = request.form['score']
        shoot = request.form['shoot']

        # 4. 그래서 그걸로 doc 을 만들자
        doc = {
            'eventType': eventType,
            'team': team,
            'score': score,
            'shoot': shoot,
        }
        db.gamestat.insert_one(doc)
    except:  # 시도한게 안되면 이걸해
        return jsonify({'result': 'fail', 'msg': '이 요청은 POST!'})

    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/gamestat', methods=['GET'])
def event_get():
    # db에서 읽어온다.
    gamestats = list(db.gamestat.find({}))  # db.bookmarks에서 가져와서 리스트로 만들어라,자동으로 들어가는 _id는 가져오지마라 제이슨으로 못만드니깐
    return jsonify(gamestats)  # 제이슨 형식으로 만들어라


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
